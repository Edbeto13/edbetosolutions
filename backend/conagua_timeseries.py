#!/usr/bin/env python3
"""
Extensión del collector de CONAGUA para almacenar series temporales
Permite crear gráficas históricas sincronizadas con el cron de 75 minutos
Author: EdbETO Solutions Team
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any

class ConaguaTimeseriesCollector:
    """Extensión para almacenar datos históricos con series temporales"""

    def __init__(self, timeseries_file='weather_timeseries.json', max_history_hours=72):
        self.timeseries_file = timeseries_file
        self.max_history_hours = max_history_hours  # 72 horas = 3 días de historial
        self.timeseries_data = {}
        self.load_timeseries()

    def load_timeseries(self):
        """Cargar datos históricos desde archivo"""
        try:
            if os.path.exists(self.timeseries_file):
                with open(self.timeseries_file, 'r', encoding='utf-8') as f:
                    self.timeseries_data = json.load(f)
                print(f"📈 Timeseries cargadas: {len(self.timeseries_data)} alcaldías")
            else:
                self.timeseries_data = {}
                print("📊 Creando nuevo archivo de timeseries")
        except Exception as e:
            print(f"⚠️ Error cargando timeseries: {e}")
            self.timeseries_data = {}

    def save_timeseries(self):
        """Guardar datos históricos con limpieza automática"""
        try:
            # Limpiar datos antiguos antes de guardar
            self.cleanup_old_data()

            with open(self.timeseries_file, 'w', encoding='utf-8') as f:
                json.dump(self.timeseries_data, f, indent=2, ensure_ascii=False)

            total_points = sum(len(series.get('series', [])) for series in self.timeseries_data.values())
            print(f"💾 Timeseries guardadas: {len(self.timeseries_data)} alcaldías, {total_points} puntos")
        except Exception as e:
            print(f"❌ Error guardando timeseries: {e}")

    def add_weather_point(self, alcaldia: str, weather_data: Dict[str, Any]):
        """Agregar punto de datos meteorológicos a la serie temporal"""
        try:
            # Extraer temperatura y precipitación numérica
            temp_str = weather_data.get('temperatura', '0°C')
            temp = float(temp_str.replace('°C', '').replace('°', ''))

            precip_str = weather_data.get('precipitacion', '0 mm')
            precip = float(precip_str.replace(' mm', '').replace('mm', ''))

            timestamp = weather_data.get('timestamp', datetime.now().isoformat())

            # Crear punto de datos
            point = {
                't': timestamp,
                'temp': temp,
                'pp': precip,
                'humedad': int(weather_data.get('humedad', '0%').replace('%', '')),
                'viento': int(weather_data.get('viento', '0 km/h').split()[0]),
                'presion': int(weather_data.get('presion', '1013 hPa').split()[0]),
                'desc': weather_data.get('pronostico', [{}])[0].get('condicion', 'Sin datos'),
                'source': weather_data.get('source', 'unknown')
            }

            # Inicializar alcaldía si no existe
            if alcaldia not in self.timeseries_data:
                self.timeseries_data[alcaldia] = {
                    'municipio': alcaldia.replace('-', ' ').title(),
                    'lastUpdate': timestamp,
                    'series': []
                }

            # Agregar punto evitando duplicados
            series = self.timeseries_data[alcaldia]['series']

            # Verificar si ya existe un punto muy reciente (último 30 minutos)
            if series:
                last_point_time = datetime.fromisoformat(series[-1]['t'])
                current_time = datetime.fromisoformat(timestamp)
                if (current_time - last_point_time).total_seconds() < 1800:  # 30 minutos
                    print(f"⚠️ Punto muy reciente para {alcaldia}, actualizando en lugar de agregar")
                    series[-1] = point
                else:
                    series.append(point)
            else:
                series.append(point)

            # Actualizar metadata
            self.timeseries_data[alcaldia]['lastUpdate'] = timestamp

            print(f"📊 Punto agregado para {alcaldia}: {temp}°C, {precip}mm")

        except Exception as e:
            print(f"❌ Error agregando punto para {alcaldia}: {e}")

    def cleanup_old_data(self):
        """Limpiar datos anteriores al período de retención"""
        cutoff_time = datetime.now() - timedelta(hours=self.max_history_hours)

        for alcaldia in self.timeseries_data:
            series = self.timeseries_data[alcaldia]['series']
            original_count = len(series)

            # Filtrar puntos dentro del período de retención
            self.timeseries_data[alcaldia]['series'] = [
                point for point in series
                if datetime.fromisoformat(point['t']) > cutoff_time
            ]

            cleaned_count = len(self.timeseries_data[alcaldia]['series'])
            if original_count > cleaned_count:
                print(f"🧹 {alcaldia}: {original_count} → {cleaned_count} puntos (limpieza {self.max_history_hours}h)")

    def get_timeseries_for_alcaldia(self, alcaldia: str) -> Dict[str, Any]:
        """Obtener serie temporal para una alcaldía específica"""
        if alcaldia not in self.timeseries_data:
            return {
                'municipio': alcaldia.replace('-', ' ').title(),
                'lastUpdate': datetime.now().isoformat(),
                'series': [],
                'error': 'No data available'
            }

        return self.timeseries_data[alcaldia].copy()

    def get_all_timeseries(self) -> Dict[str, Any]:
        """Obtener todas las series temporales"""
        return self.timeseries_data.copy()

    def get_next_update_info(self) -> Dict[str, Any]:
        """Calcular información sobre la próxima actualización del cron"""
        try:
            # Buscar la última actualización más reciente
            latest_update = None
            for alcaldia_data in self.timeseries_data.values():
                update_time = datetime.fromisoformat(alcaldia_data['lastUpdate'])
                if not latest_update or update_time > latest_update:
                    latest_update = update_time

            if not latest_update:
                return {'error': 'No previous updates found'}

            now = datetime.now()
            elapsed_minutes = (now - latest_update).total_seconds() / 60
            next_update = latest_update + timedelta(minutes=75)
            remaining_minutes = max(0, 75 - elapsed_minutes)

            return {
                'lastUpdate': latest_update.isoformat(),
                'nextUpdate': next_update.isoformat(),
                'elapsedMinutes': round(elapsed_minutes, 1),
                'remainingMinutes': round(remaining_minutes, 1),
                'needsUpdate': elapsed_minutes >= 75,
                'cronPeriodMs': 75 * 60 * 1000,  # Para el frontend
                'status': 'pending' if elapsed_minutes >= 75 else 'waiting'
            }

        except Exception as e:
            return {'error': f'Error calculating next update: {e}'}

    def batch_update_from_cache(self, cache_data: Dict[str, Any]):
        """Actualizar todas las series temporales desde el caché principal"""
        try:
            updated_count = 0

            for alcaldia, weather_data in cache_data.items():
                self.add_weather_point(alcaldia, weather_data)
                updated_count += 1

            self.save_timeseries()
            print(f"🔄 Batch update completado: {updated_count} alcaldías actualizadas")
            return updated_count

        except Exception as e:
            print(f"❌ Error en batch update: {e}")
            return 0

    def get_statistics(self) -> Dict[str, Any]:
        """Obtener estadísticas del sistema de timeseries"""
        total_points = 0
        oldest_point = None
        newest_point = None

        for alcaldia_data in self.timeseries_data.values():
            series = alcaldia_data.get('series', [])
            total_points += len(series)

            for point in series:
                point_time = datetime.fromisoformat(point['t'])
                if not oldest_point or point_time < oldest_point:
                    oldest_point = point_time
                if not newest_point or point_time > newest_point:
                    newest_point = point_time

        return {
            'total_alcaldias': len(self.timeseries_data),
            'total_points': total_points,
            'average_points_per_alcaldia': round(total_points / max(1, len(self.timeseries_data)), 1),
            'oldest_point': oldest_point.isoformat() if oldest_point else None,
            'newest_point': newest_point.isoformat() if newest_point else None,
            'retention_hours': self.max_history_hours,
            'file_size_mb': round(os.path.getsize(self.timeseries_file) / 1024 / 1024, 2) if os.path.exists(self.timeseries_file) else 0
        }

# Instancia global del collector de timeseries
timeseries_collector = ConaguaTimeseriesCollector()

# Funciones helper para usar en el API server
def add_weather_to_timeseries(alcaldia: str, weather_data: Dict[str, Any]):
    """Agregar datos meteorológicos a las series temporales"""
    timeseries_collector.add_weather_point(alcaldia, weather_data)

def get_timeseries(alcaldia: str) -> Dict[str, Any]:
    """Obtener serie temporal para una alcaldía"""
    return timeseries_collector.get_timeseries_for_alcaldia(alcaldia)

def get_cron_info() -> Dict[str, Any]:
    """Obtener información del cron de 75 minutos"""
    return timeseries_collector.get_next_update_info()

def batch_update_timeseries(cache_data: Dict[str, Any]) -> int:
    """Actualizar todas las timeseries desde el caché"""
    return timeseries_collector.batch_update_from_cache(cache_data)

def get_timeseries_stats() -> Dict[str, Any]:
    """Obtener estadísticas de las timeseries"""
    return timeseries_collector.get_statistics()

if __name__ == "__main__":
    # Prueba del módulo
    print("🧪 Probando sistema de timeseries...")

    # Simular datos de prueba
    test_data = {
        'temperatura': '22°C',
        'precipitacion': '1.5 mm',
        'humedad': '65%',
        'viento': '12 km/h',
        'presion': '1015 hPa',
        'timestamp': datetime.now().isoformat(),
        'source': 'Test Data',
        'pronostico': [{'condicion': 'Parcialmente nublado'}]
    }

    # Agregar punto de prueba
    timeseries_collector.add_weather_point('cdmx', test_data)
    timeseries_collector.save_timeseries()

    # Obtener datos
    series = get_timeseries('cdmx')
    print(f"📊 Serie CDMX: {len(series.get('series', []))} puntos")

    # Información del cron
    cron_info = get_cron_info()
    print(f"⏰ Próxima actualización en: {cron_info.get('remainingMinutes', 0)} min")

    # Estadísticas
    stats = get_timeseries_stats()
    print(f"📈 Total puntos: {stats['total_points']}")

    print("✅ Sistema de timeseries funcionando")
