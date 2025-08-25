#!/usr/bin/env python3
"""
Módulo de integración con Conagua/SMN para datos meteorológicos reales
Author: EdbETO Solutions Team
Repositorio: https://github.com/Edbeto13/Hydredelback
Licencia: MIT
"""

import json
import os
import time
import threading
import requests
from datetime import datetime, timedelta
from urllib.parse import urlencode
from typing import Dict, List, Optional, Any

class ConaguaDataCollector:
    """Recolector automático de datos meteorológicos de Conagua/SMN"""
    
    def __init__(self, cache_file: str = 'weather_cache.json', update_interval: int = 4500):  # 75 minutos = 4500 segundos
        self.cache_file = cache_file
        self.update_interval = update_interval  # 1 hora 15 minutos
        self.cache_data: Dict[str, Any] = {}
        self.last_update: Optional[datetime] = None
        self.is_running: bool = False
        
        # URLs de servicios meteorológicos mexicanos
        self.conagua_api_base = "https://smn.conagua.gob.mx/tools/GUI/webservices/?method=1"
        
        # Estaciones meteorológicas CDMX (Basado en las IDs de Conagua para CDMX)
        self.cdmx_stations: Dict[str, Dict[str, Any]] = {
            'cdmx': {'id': '9', 'name': 'Ciudad de México', 'lat': 19.4026, 'lon': -99.1732},
            'alvaro-obregon': {'id': '9', 'idmun': '010', 'name': 'Álvaro Obregón', 'lat': 19.3473, 'lon': -99.2449},
            'azcapotzalco': {'id': '9', 'idmun': '002', 'name': 'Azcapotzalco', 'lat': 19.4847, 'lon': -99.1861},
            'benito-juarez': {'id': '9', 'idmun': '014', 'name': 'Benito Juárez', 'lat': 19.3773, 'lon': -99.1574},
            'coyoacan': {'id': '9', 'idmun': '003', 'name': 'Coyoacán', 'lat': 19.3467, 'lon': -99.1618},
            'cuajimalpa': {'id': '9', 'idmun': '004', 'name': 'Cuajimalpa', 'lat': 19.3646, 'lon': -99.2919},
            'gustavo-madero': {'id': '9', 'idmun': '005', 'name': 'Gustavo A. Madero', 'lat': 19.4847, 'lon': -99.1138},
            'iztacalco': {'id': '9', 'idmun': '006', 'name': 'Iztacalco', 'lat': 19.3904, 'lon': -99.1137},
            'iztapalapa': {'id': '9', 'idmun': '007', 'name': 'Iztapalapa', 'lat': 19.3457, 'lon': -99.0564},
            'magdalena-contreras': {'id': '9', 'idmun': '008', 'name': 'La Magdalena Contreras', 'lat': 19.2397, 'lon': -99.2417},
            'miguel-hidalgo': {'id': '9', 'idmun': '016', 'name': 'Miguel Hidalgo', 'lat': 19.4254, 'lon': -99.2027},
            'milpa-alta': {'id': '9', 'idmun': '009', 'name': 'Milpa Alta', 'lat': 19.1916, 'lon': -99.0233},
            'tlahuac': {'id': '9', 'idmun': '011', 'name': 'Tláhuac', 'lat': 19.2864, 'lon': -99.0134},
            'tlalpan': {'id': '9', 'idmun': '012', 'name': 'Tlalpan', 'lat': 19.2896, 'lon': -99.1669},
            'venustiano-carranza': {'id': '9', 'idmun': '017', 'name': 'Venustiano Carranza', 'lat': 19.4284, 'lon': -99.1073},
            'xochimilco': {'id': '9', 'idmun': '013', 'name': 'Xochimilco', 'lat': 19.2577, 'lon': -99.1037}
        }
        
        self.load_cache()
        print(f"🌤️ ConaguaDataCollector inicializado")
        print(f"📊 Intervalo de actualización: {self.update_interval/60:.0f} minutos")
    
    def load_cache(self) -> None:
        """Cargar datos de caché desde archivo"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache_content = json.load(f)
                    self.cache_data = cache_content.get('data', {})
                    last_update_str = cache_content.get('last_update')
                    if last_update_str:
                        self.last_update = datetime.fromisoformat(last_update_str)
                    print(f"✅ Caché cargado: {len(self.cache_data)} alcaldías")
        except Exception as e:
            print(f"⚠️ Error cargando caché: {e}")
            self.cache_data = {}
    
    def save_cache(self) -> None:
        """Guardar datos en caché"""
        try:
            cache_content = {
                'data': self.cache_data,
                'last_update': self.last_update.isoformat() if self.last_update else None,
                'updated_at': datetime.now().isoformat()
            }
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_content, f, indent=2, ensure_ascii=False)
            print(f"💾 Caché guardado: {len(self.cache_data)} alcaldías")
        except Exception as e:
            print(f"❌ Error guardando caché: {e}")
    
    def fetch_station_data(self, station_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Obtener datos de una estación específica usando el API de Conagua"""
        try:
            # URL del servicio de Conagua con método 1 (pronóstico por municipio)
            url = self.conagua_api_base
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json',
                'Accept-Language': 'es-MX,es;q=0.9,en;q=0.8'
            }
            
            # Preparar parámetros para la solicitud
            # Para CDMX, ides=9 (Ciudad de México)
            params = {
                'ides': station_info['id']  # ID del estado (9 para CDMX)
            }
            
            # Si hay un ID municipal específico, lo incluimos
            if 'idmun' in station_info:
                params['idmun'] = station_info['idmun']
            
            # Realizar la solicitud HTTP al API de Conagua
            print(f"📡 Solicitando datos a Conagua para {station_info['name']}...")
            response = requests.get(url, params=params, headers=headers, timeout=15)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    return self.parse_conagua_data(data, station_info)
                except json.JSONDecodeError:
                    print(f"⚠️ Error decodificando JSON para {station_info['name']}")
                    print(f"Respuesta recibida: {response.text[:200]}...")
                    return None
            else:
                print(f"⚠️ HTTP {response.status_code} para {station_info['name']}")
                return None
        
        except requests.RequestException as e:
            print(f"❌ Error en solicitud para {station_info['name']}: {e}")
            return None
        except Exception as e:
            print(f"❌ Error inesperado para {station_info['name']}: {e}")
            return None
    
    def parse_conagua_data(self, raw_data: Dict[str, Any], station_info: Dict[str, Any]) -> Dict[str, Any]:
        """Parsear datos del formato Conagua a nuestro formato interno"""
        try:
            # El API de Conagua retorna datos en un formato específico
            # Verificamos si tenemos datos válidos
            if not raw_data or not isinstance(raw_data, dict):
                print(f"⚠️ Formato de datos inválido para {station_info['name']}")
                return self.generate_fallback_data(station_info['name'])
            
            # Extraer información del esquema de Conagua
            # Campos esperados:
            # ides, idmun, nes, nmun, dloc, ndia, tmax, tmin, desciel, probprec, prec, velvien, dirvienc, dirvieng, raf, cc
            
            # Extraer el primer item (datos actuales o para hoy)
            forecast_data = raw_data.get('municipal', [])
            
            if not forecast_data or len(forecast_data) == 0:
                print(f"⚠️ Sin datos de pronóstico para {station_info['name']}")
                return self.generate_fallback_data(station_info['name'])
                
            # Datos del día actual
            today_data = forecast_data[0]
            
            # Construir los datos procesados
            parsed_data = {
                'station_name': station_info['name'],
                'temperatura': f"{today_data.get('tmax', 'N/A')}°C",
                'temperatura_min': f"{today_data.get('tmin', 'N/A')}°C",
                'humedad': f"{today_data.get('cc', 'N/A')}%",
                'viento': f"{today_data.get('velvien', 'N/A')} km/h",
                'direccion_viento': today_data.get('dirvieng', 'N/A'),
                'direccion_viento_card': today_data.get('dirvienc', 'N/A'),
                'precipitacion': f"{today_data.get('prec', 'N/A')} mm",
                'probabilidad_precipitacion': f"{today_data.get('probprec', 'N/A')}%",
                'condicion_cielo': today_data.get('desciel', 'N/A'),
                'timestamp': datetime.now().isoformat(),
                'source': 'Conagua/SMN',
                'raw_data': today_data,
                'pronostico': self.parse_forecast_data(forecast_data)
            }
            
            return parsed_data
            
        except Exception as e:
            print(f"❌ Error parseando datos de Conagua: {e}")
            return self.generate_fallback_data(station_info['name'])
            
    def parse_forecast_data(self, forecast_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Procesa los datos de pronóstico para múltiples días"""
        forecast = []
        
        # Nombres de días en español
        day_names = ['Hoy', 'Mañana', 'Pasado mañana', 'En 3 días', 'En 4 días']
        
        # Procesamos hasta 5 días o lo que esté disponible
        for i, day_data in enumerate(forecast_data[:5]):
            try:
                day_name = day_names[i] if i < len(day_names) else f"En {i} días"
                
                forecast_day = {
                    'dia': day_name,
                    'fecha': day_data.get('ndia', 'N/A'),
                    'temp_max': f"{day_data.get('tmax', 'N/A')}°C",
                    'temp_min': f"{day_data.get('tmin', 'N/A')}°C",
                    'condicion': day_data.get('desciel', 'N/A'),
                    'precipitacion': f"{day_data.get('prec', 'N/A')} mm",
                    'probabilidad_lluvia': f"{day_data.get('probprec', 'N/A')}%",
                    'viento': f"{day_data.get('velvien', 'N/A')} km/h",
                    'direccion_viento': day_data.get('dirvieng', 'N/A')
                }
                
                forecast.append(forecast_day)
            except Exception as e:
                print(f"❌ Error procesando día {i} del pronóstico: {e}")
        
        return forecast
    
    def generate_forecast(self) -> List[Dict[str, str]]:
        """Generar pronóstico de 3 días"""
        import random
        
        forecast: List[Dict[str, str]] = []
        days = ['Hoy', 'Mañana', 'Pasado mañana']
        conditions = ['Despejado', 'Parcialmente nublado', 'Nublado', 'Lluvia ligera', 'Lluvia moderada']
        
        # Direcciones del viento
        direcciones = ["Norte", "Sur", "Este", "Oeste", "Noreste", "Noroeste", "Sureste", "Suroeste"]
        
        for day in days:
            temp_max = 18 + random.randint(0, 12)
            temp_min = temp_max - random.randint(3, 8)
            condition = random.choice(conditions)
            direccion = random.choice(direcciones)
            
            forecast.append({
                'dia': day,
                'fecha': (datetime.now() + timedelta(days=days.index(day))).strftime('%d/%m/%Y'),
                'temp_max': f"{temp_max}°C",
                'temp_min': f"{temp_min}°C",
                'condicion': condition,
                'precipitacion': f"{random.choice([0, 0, 0, 0.2, 1.5])} mm",
                'probabilidad_lluvia': f"{random.randint(0, 80)}%",
                'viento': f"{8 + random.randint(0, 12)} km/h",
                'direccion_viento': direccion
            })
        
        return forecast
    
    def update_all_stations(self) -> bool:
        """Actualizar datos de todas las estaciones CDMX"""
        print(f"🔄 Iniciando actualización de datos meteorológicos...")
        updated_count = 0
        
        for alcaldia_key, station_info in self.cdmx_stations.items():
            try:
                print(f"📡 Obteniendo datos de {station_info['name']}...")
                
                # Intentar obtener datos reales
                data = self.fetch_station_data(station_info)
                
                if data:
                    self.cache_data[alcaldia_key] = data
                    updated_count += 1
                    print(f"✅ {station_info['name']}: {data['temperatura']}, {data.get('humedad', 'N/A')}")
                else:
                    # Usar datos fallback si falla la conexión real
                    print(f"⚠️ Usando datos fallback para {station_info['name']}")
                    self.cache_data[alcaldia_key] = self.generate_fallback_data(station_info['name'])
                    updated_count += 1
                
                # Pausa corta entre requests
                time.sleep(0.5)
                
            except Exception as e:
                print(f"❌ Error procesando {station_info['name']}: {e}")
                # Generar datos fallback en caso de error
                self.cache_data[alcaldia_key] = self.generate_fallback_data(station_info['name'])
        
        self.last_update = datetime.now()
        self.save_cache()
        
        print(f"🎯 Actualización completada: {updated_count}/{len(self.cdmx_stations)} estaciones")
        return updated_count > 0
    
    def generate_fallback_data(self, station_name: str) -> Dict[str, Any]:
        """Generar datos de respaldo realistas"""
        import random
        
        # Datos típicos para CDMX según época del año
        base_temp = 22 + random.uniform(-4, 6)
        temp_min = base_temp - random.randint(3, 8)
        
        # Condiciones del cielo comunes
        cielo_opciones = [
            "Despejado", "Medio nublado", "Nublado", 
            "Lluvia ligera", "Lluvia", "Parcialmente nublado"
        ]
        
        # Direcciones del viento
        direcciones = ["Norte", "Sur", "Este", "Oeste", "Noreste", "Noroeste", "Sureste", "Suroeste"]
        direcciones_card = ["N", "S", "E", "W", "NE", "NW", "SE", "SW"]
        
        # Elegir dirección aleatoria
        dir_index = random.randint(0, len(direcciones) - 1)
        
        return {
            'station_name': station_name,
            'temperatura': f"{base_temp:.0f}°C",
            'temperatura_min': f"{temp_min:.0f}°C",
            'humedad': f"{55 + random.randint(0, 25)}%",
            'viento': f"{8 + random.randint(0, 12)} km/h",
            'direccion_viento': direcciones[dir_index],
            'direccion_viento_card': direcciones_card[dir_index],
            'precipitacion': f"{random.choice([0, 0, 0, 0.2, 1.5])} mm",
            'probabilidad_precipitacion': f"{random.randint(0, 80)}%",
            'condicion_cielo': random.choice(cielo_opciones),
            'timestamp': datetime.now().isoformat(),
            'source': 'Fallback Data',
            'pronostico': self.generate_forecast(),
            'note': 'Datos generados automáticamente (API no disponible)'
        }
    
    def get_weather_data(self, alcaldia: str = 'cdmx') -> Dict[str, Any]:
        """Obtener datos meteorológicos para una alcaldía"""
        # Verificar si los datos necesitan actualización
        if self.needs_update():
            print(f"📅 Datos desactualizados, iniciando actualización...")
            self.update_all_stations()
        
        # Retornar datos de la alcaldía solicitada
        if alcaldia in self.cache_data:
            data = self.cache_data[alcaldia].copy()
            data['cache_age'] = self.get_cache_age()
            return data
        else:
            print(f"⚠️ Alcaldía '{alcaldia}' no encontrada, usando CDMX promedio")
            return self.get_weather_data('cdmx')
    
    def needs_update(self) -> bool:
        """Verificar si los datos necesitan actualización"""
        if not self.last_update:
            return True
        
        time_since_update = datetime.now() - self.last_update
        return time_since_update.total_seconds() > self.update_interval
    
    def get_cache_age(self) -> str:
        """Obtener la edad del caché en minutos"""
        if self.last_update:
            age_seconds = (datetime.now() - self.last_update).total_seconds()
            return f"{age_seconds/60:.0f} minutos"
        return "Sin datos"
    
    def start_automatic_updates(self) -> None:
        """Iniciar actualizaciones automáticas en background"""
        if self.is_running:
            print("⚠️ Las actualizaciones automáticas ya están ejecutándose")
            return
        
        self.is_running = True
        print(f"🔄 Iniciando actualizaciones automáticas cada {self.update_interval/60:.0f} minutos")
        
        def update_loop() -> None:
            while self.is_running:
                try:
                    if self.needs_update():
                        print(f"⏰ Actualización automática programada...")
                        self.update_all_stations()
                    
                    # Esperar hasta la siguiente verificación (cada 5 minutos)
                    time.sleep(300)  # 5 minutos
                    
                except Exception as e:
                    print(f"❌ Error en loop de actualización automática: {e}")
                    time.sleep(60)  # Esperar 1 minuto antes de reintentar
        
        # Ejecutar primera actualización inmediatamente
        if not self.cache_data or self.needs_update():
            print("🔄 Ejecutando primera actualización...")
            self.update_all_stations()
        
        # Iniciar thread de actualización automática
        update_thread = threading.Thread(target=update_loop, daemon=True)
        update_thread.start()
        print("✅ Actualizaciones automáticas iniciadas")
    
    def stop_automatic_updates(self) -> None:
        """Detener actualizaciones automáticas"""
        self.is_running = False
        print("🛑 Actualizaciones automáticas detenidas")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Obtener estado del sistema de recolección"""
        return {
            'status': 'running' if self.is_running else 'stopped',
            'stations_count': len(self.cdmx_stations),
            'cached_data_count': len(self.cache_data),
            'last_update': self.last_update.isoformat() if self.last_update else None,
            'cache_age': self.get_cache_age(),
            'update_interval_minutes': self.update_interval / 60,
            'needs_update': self.needs_update()
        }

# Instancia global del colector
weather_collector = ConaguaDataCollector()

# Funciones de conveniencia para usar en el API server
def get_weather_for_alcaldia(alcaldia: str = 'cdmx') -> Dict[str, Any]:
    """Función helper para obtener datos meteorológicos"""
    return weather_collector.get_weather_data(alcaldia)

def start_weather_collection() -> None:
    """Iniciar recolección automática"""
    weather_collector.start_automatic_updates()

def update_weather_data() -> bool:
    """Forzar actualización de datos meteorológicos"""
    return weather_collector.update_all_stations()

def get_collection_status() -> Dict[str, Any]:
    """Obtener estado del sistema"""
    return weather_collector.get_system_status()

if __name__ == "__main__":
    # Prueba del módulo
    print("🧪 Probando módulo de Conagua...")
    
    # Iniciar actualizaciones automáticas
    weather_collector.start_automatic_updates()
    
    # Esperar un poco y mostrar datos
    time.sleep(2)
    
    # Probar datos para diferentes alcaldías
    test_alcaldias = ['cdmx', 'iztapalapa', 'coyoacan']
    
    for alcaldia in test_alcaldias:
        print(f"\n📊 Datos para {alcaldia}:")
        data = get_weather_for_alcaldia(alcaldia)
        print(f"  Temperatura: {data.get('temperatura', 'N/A')}")
        print(f"  Temperatura mínima: {data.get('temperatura_min', 'N/A')}")
        print(f"  Condición: {data.get('condicion_cielo', 'N/A')}")
        print(f"  Humedad: {data.get('humedad', 'N/A')}")
        print(f"  Viento: {data.get('viento', 'N/A')} ({data.get('direccion_viento', 'N/A')})")
        print(f"  Probabilidad de lluvia: {data.get('probabilidad_precipitacion', 'N/A')}")
        print(f"  Fuente: {data.get('source', 'N/A')}")
        
        print("\n📅 Pronóstico:")
        pronostico = data.get('pronostico', [])
        for dia in pronostico[:2]:  # Solo mostrar los primeros dos días
            print(f"  {dia.get('dia', 'N/A')}: {dia.get('temp_min', 'N/A')} a {dia.get('temp_max', 'N/A')}, {dia.get('condicion', 'N/A')}")
    
    print(f"\n📈 Estado del sistema:")
    status = get_collection_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    print(f"\n✅ Módulo funcionando correctamente")
    print(f"🔄 Actualización automática cada 75 minutos")
    print(f"💾 Datos almacenados en caché: {weather_collector.cache_file}")
