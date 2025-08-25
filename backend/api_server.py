#!/usr/bin/env python3
"""
Backend API Server para Clima CDMX con integración Conagua
Author: EdbETO Solutions Team
Repositorio: https://github.com/Edbeto13/Hydredelback
Licencia: MIT
"""

import json
import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import requests

# Importar módulo de Conagua
try:
    from conagua_collector import get_weather_for_alcaldia, start_weather_collection, get_collection_status
    CONAGUA_AVAILABLE = True
    print("✅ Módulo de Conagua cargado correctamente")
    
    # Intentar cargar el módulo de series de tiempo si Conagua está disponible
    try:
        from conagua_timeseries import ConaguaTimeseriesCollector
        TIMESERIES_AVAILABLE = True
        timeseries_collector = ConaguaTimeseriesCollector()
        print("✅ Módulo de series de tiempo cargado correctamente")
    except ImportError as e:
        print(f"⚠️ Módulo de series de tiempo no disponible: {e}")
        TIMESERIES_AVAILABLE = False
except ImportError as e:
    print(f"⚠️ Módulo de Conagua no disponible: {e}")
    CONAGUA_AVAILABLE = False
    TIMESERIES_AVAILABLE = False

# External Conagua proxy settings (example — sustituir por dominio real si aplica)
BASE_URL = "https://smn.conagua.gob.mx/"
RESOURCE = "tools/GUI/webservices/?method=1"

# Simple in-memory cache for pronostico responses: key -> (timestamp, data)
PRONOSTICO_CACHE = {}
CACHE_TTL = 75 * 60  # 75 minutes in seconds

def _cache_get(key):
    """Obtener valor de caché si existe y no ha expirado"""
    if key not in PRONOSTICO_CACHE:
        return None
    timestamp, data = PRONOSTICO_CACHE[key]
    if (datetime.now().timestamp() - timestamp) > CACHE_TTL:
        return None
    return data

def _cache_set(key, data):
    """Almacenar valor en caché con timestamp actual"""
    PRONOSTICO_CACHE[key] = (datetime.now().timestamp(), data)

def to_float(v):
    try:
        return float(str(v).replace(",", ".")) if v not in (None, "") else None
    except Exception:
        return None

def to_int(v):
    try:
        return int(float(v)) if v not in (None, "") else None
    except Exception:
        return None

def parse_dloc(s):
    if not s:
        return None
    digits = "".join(ch for ch in str(s) if ch.isdigit())
    try:
        return datetime.strptime(digits, "%Y%m%d%H%M").isoformat()
    except ValueError:
        try:
            return datetime.strptime(digits, "%Y%m%d%H").isoformat()
        except ValueError:
            return s

class ClimaCDMXHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        # Parse URL
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query = urllib.parse.parse_qs(parsed_path.query)
        
        # Routes
        if path == '/api/' or path == '/api':
            self.handle_api_status()
        elif path == '/api/weather':
            self.handle_weather_data(query)
        elif path == '/api/pronostico':
            self.handle_pronostico(query)
        elif path == '/api/weather/status':
            self.handle_weather_status()
        elif path == '/api/weather/timeseries':
            self.handle_timeseries(query)
        elif path == '/health':
            self.handle_health()
        else:
            self.handle_404()
    
    def do_POST(self):
        if self.path == '/api/chat':
            self.handle_chat()
        elif self.path == '/api/llm':
            self.handle_nvidia_api()
        else:
            self.handle_404()
    
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def handle_api_status(self):
        """Status del API con información de Conagua"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        response = {
            "status": "active",
            "service": "Clima CDMX API",
            "version": "2.0.0",
            "timestamp": datetime.now().isoformat(),
            "endpoints": ["/api/weather", "/api/weather/status", "/api/chat", "/health"],
            "conagua_integration": {
                "available": CONAGUA_AVAILABLE,
                "status": "collecting" if CONAGUA_AVAILABLE else "fallback_mode",
                "update_interval": "75 minutes" if CONAGUA_AVAILABLE else "N/A"
            }
        }
        self.wfile.write(json.dumps(response, indent=2, ensure_ascii=False).encode('utf-8'))
    
    def handle_weather_data(self, query):
        """Datos meteorológicos de Conagua/SMN"""
        alcaldia = query.get('alcaldia', ['cdmx'])[0]
        
        try:
            if CONAGUA_AVAILABLE:
                # Obtener datos reales de Conagua
                weather_data = get_weather_for_alcaldia(alcaldia)
                print(f"🌤️ Datos obtenidos de Conagua para {alcaldia}")
            else:
                # Fallback a datos simulados
                weather_data = self.get_simulated_data(alcaldia)
                print(f"📊 Usando datos simulados para {alcaldia}")
            
            # Formatear respuesta
            formatted_data = {
                "alcaldia": alcaldia,
                "temperatura": weather_data.get("temperatura", "22°C"),
                "humedad": weather_data.get("humedad", "65%"),
                "viento": weather_data.get("viento", "15 km/h"),
                "precipitacion": weather_data.get("precipitacion", "0 mm"),
                "presion": weather_data.get("presion", "1013 hPa"),
                "timestamp": weather_data.get("timestamp", datetime.now().isoformat()),
                "pronostico": weather_data.get("pronostico", self.get_default_forecast()),
                "source": weather_data.get("source", "SMN/Conagua"),
                "cache_age": weather_data.get("cache_age", "N/A"),
                "station_name": weather_data.get("station_name", f"Estación {alcaldia.title()}")
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(formatted_data, indent=2, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            print(f"❌ Error obteniendo datos meteorológicos: {e}")
            # Enviar datos de emergencia
            emergency_data = self.get_simulated_data(alcaldia)
            emergency_data["error"] = f"Error del sistema: {str(e)}"
            emergency_data["source"] = "Emergency Fallback"
            
            self.send_response(200)  # Enviar 200 para que el frontend no falle
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(emergency_data, indent=2, ensure_ascii=False).encode('utf-8'))
    
    def get_simulated_data(self, alcaldia):
        """Datos meteorológicos simulados como fallback"""
        import random
        
        # Generar datos realistas para CDMX
        base_temp = 20 + random.uniform(-3, 8)
        
        return {
            "alcaldia": alcaldia,
            "temperatura": f"{base_temp:.0f}°C",
            "humedad": f"{55 + random.randint(0, 25)}%",
            "viento": f"{8 + random.randint(0, 12)} km/h",
            "precipitacion": f"{random.choice([0, 0, 0, 0.5, 1.2, 2.8])} mm",
            "presion": f"{1013 + random.randint(-8, 8)} hPa",
            "timestamp": datetime.now().isoformat(),
            "pronostico": self.get_default_forecast(),
            "source": "Simulated Data",
            "station_name": f"Estación {alcaldia.title()}"
        }
    
    def get_default_forecast(self):
        """Pronóstico por defecto"""
        return [
            {"dia": "Hoy", "temp_max": "25°C", "temp_min": "18°C", "condicion": "Parcialmente nublado"},
            {"dia": "Mañana", "temp_max": "27°C", "temp_min": "19°C", "condicion": "Soleado"},
            {"dia": "Pasado mañana", "temp_max": "24°C", "temp_min": "17°C", "condicion": "Lluvioso"}
        ]
    
    def handle_weather_status(self):
        """Estado del sistema de recolección de datos"""
        try:
            if CONAGUA_AVAILABLE:
                status = get_collection_status()
                status["conagua_module"] = "available"
            else:
                status = {
                    "conagua_module": "not_available",
                    "status": "fallback_mode",
                    "message": "Using simulated data"
                }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(status, indent=2, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Error getting weather status: {e}")
    
    def handle_chat(self):
        """Chatbot responses"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode())
            question = data.get('question', '')
            
            # Simple chatbot logic
            response_text = self.generate_chat_response(question)
            
            response = {
                "response": response_text,
                "timestamp": datetime.now().isoformat(),
                "source": "backend_chatbot"
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        except Exception as e:
            self.send_error(400, f"Error processing chat: {e}")
    
    def generate_chat_response(self, question):
        """Genera respuestas del chatbot"""
        question_lower = question.lower()
        
        if 'temperatura' in question_lower or 'temp' in question_lower:
            return "La temperatura actual en CDMX es de 22°C con máxima de 25°C."
        elif 'lluvia' in question_lower or 'llover' in question_lower:
            return "No se esperan lluvias para hoy. Precipitación: 0 mm."
        elif 'viento' in question_lower:
            return "El viento actual es de 15 km/h del noreste."
        elif 'humedad' in question_lower:
            return "La humedad relativa es del 65%. "
        else:
            return f"Información sobre el clima en CDMX disponible. Pregunta sobre temperatura, lluvia, viento o humedad."
    
    def handle_health(self):
        """Health check endpoint"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        health = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "uptime": "running",
            "services": {
                "api": "active",
                "weather": "active",
                "chat": "active"
            },
            "conagua_integration": CONAGUA_AVAILABLE
        }
        self.wfile.write(json.dumps(health, indent=2).encode())
    
    def handle_nvidia_api(self):
        """NVIDIA FourCastNet integration"""
        self.send_response(501)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response = {
            "error": "NVIDIA API integration requires additional setup",
            "message": "Configure NGC_API_KEY environment variable",
            "fallback": "Using local weather data instead"
        }
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def handle_404(self):
        self.send_error(404, "Endpoint not found")

    def handle_timeseries(self, query):
        """Endpoint para obtener series temporales de datos meteorológicos"""
        if not TIMESERIES_AVAILABLE:
            self.send_response(501)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "error": "timeseries_not_available",
                "message": "El módulo de series temporales no está disponible",
                "status": "error"
            }
            self.wfile.write(json.dumps(response, indent=2, ensure_ascii=False).encode('utf-8'))
            return
        
        try:
            # Obtener parámetros
            alcaldia = query.get('alcaldia', ['cdmx'])[0]  # Usar CDMX como valor por defecto
            stats_only = query.get('stats', ['false'])[0].lower() == 'true'
            hours = query.get('hours', [None])[0]
            
            # Convertir hours a entero si existe
            if hours:
                try:
                    hours = int(hours)
                except ValueError:
                    hours = None
            
            # Obtener datos de series temporales
            if stats_only:
                # Si solo se solicitan estadísticas
                from conagua_timeseries import timeseries_collector
                stats_data = timeseries_collector.get_statistics()
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(stats_data, indent=2, ensure_ascii=False).encode('utf-8'))
                return
            
            # Obtener datos para una alcaldía específica
            from conagua_timeseries import get_timeseries
            timeseries_data = get_timeseries(alcaldia)
            
            # Filtrar por horas si se especifica
            if hours and hours > 0:
                now = datetime.now()
                filtered_series = []
                
                # Solo incluir puntos de las últimas X horas
                for point in timeseries_data.get('series', []):
                    point_time = datetime.fromisoformat(point['t'])
                    if (now - point_time).total_seconds() <= hours * 3600:
                        filtered_series.append(point)
                
                timeseries_data['series'] = filtered_series
                timeseries_data['filtered_by_hours'] = hours
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(timeseries_data, indent=2, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            print(f"❌ Error obteniendo series temporales: {e}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_response = {
                "error": "server_error",
                "message": f"Error al procesar series temporales: {str(e)}",
                "status": "error"
            }
            self.wfile.write(json.dumps(error_response, indent=2, ensure_ascii=False).encode('utf-8'))
    
    def handle_pronostico(self, query):
        """Proxy ligero para /api/pronostico usando el servicio externo de ejemplo"""
        # leer parámetros compatibles con el ejemplo
        ides = query.get('ides', [None])[0]
        idmun = query.get('idmun', [None])[0]
        ndia = query.get('ndia', [None])[0]

        # Validación básica: valores nulos o no numéricos -> 400
        def is_int_like(x):
            if x is None: return False
            try:
                int(str(x))
                return True
            except:
                return False

        # If none provided, return 400
        if not any([ides, idmun, ndia]):
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'missing_parameters', 'message': 'Provide at least one of ides, idmun, ndia'}).encode('utf-8'))
            return

        params = {}
        if ides and is_int_like(ides): params['ides'] = int(str(ides))
        if idmun and is_int_like(idmun): params['idmun'] = int(str(idmun))
        if ndia and is_int_like(ndia): params['ndia'] = int(str(ndia))

        # Cache key
        cache_key = f"p:{params.get('ides')}_{params.get('idmun')}_{params.get('ndia')}"
        cached = _cache_get(cache_key)
        if cached is not None:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(cached, indent=2, ensure_ascii=False).encode('utf-8'))
            return

        try:
            url = BASE_URL + RESOURCE
            headers = {'User-Agent': 'Hydredelback/1.0 (+https://github.com/Edbeto13/Hydredelback)', 'Accept': 'application/json'}
            r = requests.get(url, params=params, timeout=10, headers=headers)
            r.raise_for_status()
            data = r.json()

            # Normalizar respuesta (matching example fields)
            fc = {
                'ides': to_int(data.get('ides')),
                'idmun': to_int(data.get('idmun')),
                'nes': data.get('nes'),
                'nmun': data.get('nmun'),
                'dloc': data.get('dloc'),
                'dloc_iso': parse_dloc(data.get('dloc')),
                'ndia': to_int(data.get('ndia')),
                'tmax': to_float(data.get('tmax')),
                'tmin': to_float(data.get('tmin')),
                'desciel': data.get('desciel'),
                'probprec': to_float(data.get('probprec')),
                'prec': to_float(data.get('prec')),
                'velvien': to_float(data.get('velvien')),
                'dirvienc': data.get('dirvienc'),
                'dirvieng': to_float(data.get('dirvieng')),
                'cc': to_float(data.get('cc')),
                'lat': to_float(data.get('lat')),
                'lon': to_float(data.get('lon')),
                'dh': to_int(data.get('dh')),
                'raf': to_float(data.get('raf')),
                'raw': data
            }
            # Store in cache
            _cache_set(cache_key, fc)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(fc, indent=2, ensure_ascii=False).encode('utf-8'))

        except Exception as e:
            print(f"\u274c Error en proxy pronostico: {e}")
            self.send_response(502)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            err = {'error': 'proxy_failed', 'message': str(e)}
            self.wfile.write(json.dumps(err, indent=2).encode('utf-8'))

def run_server(port=8000):
    """Ejecutar servidor con integración Conagua"""
    # Inicializar recolección automática de Conagua si está disponible
    if CONAGUA_AVAILABLE:
        print("🔄 Iniciando recolección automática de datos Conagua...")
        start_weather_collection()
        print("✅ Sistema de recolección Conagua iniciado (actualización cada 75 minutos)")
    else:
        print("⚠️ Funcionando en modo fallback sin integración Conagua")
    
    server = HTTPServer(('0.0.0.0', port), ClimaCDMXHandler)
    print(f"🌤️ Servidor Clima CDMX iniciado en puerto {port}")
    print(f"📡 Endpoints disponibles:")
    print(f"   http://localhost:{port}/api/")
    print(f"   http://localhost:{port}/api/weather")
    print(f"   http://localhost:{port}/api/weather/status")
    print(f"   http://localhost:{port}/health")
    
    if CONAGUA_AVAILABLE:
        print(f"🌐 Integración Conagua: ACTIVA (datos reales cada 75 minutos)")
    else:
        print(f"📊 Integración Conagua: INACTIVA (usando datos simulados)")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")
        server.shutdown()

if __name__ == "__main__":
    run_server()
