# Backend Configuration - EdbETO Solutions
# Configuración centralizada para todas las APIs y servicios

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Configuración base del backend"""
    
    # Configuración del servidor
    HOST = os.getenv('BACKEND_HOST', '0.0.0.0')
    PORT = int(os.getenv('BACKEND_PORT', 8000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # APIs externas
    CONAGUA_BASE_URL = "https://smn.conagua.gob.mx/es/"
    WEATHER_API_TIMEOUT = 30
    
    # Configuración de caché
    CACHE_TIMEOUT = 75 * 60  # 75 minutos en segundos
    
    # Configuración de logs
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'backend.log')
    
    # Configuración CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    
    # Configuración UNEGario
    UNEGARIO_DATA_PATH = os.getenv('UNEGARIO_DATA_PATH', './data')
    
    # Google Calendar API (para UNEGario)
    GOOGLE_CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH', './credentials.json')
    
    # Configuración de respuesta
    DEFAULT_RESPONSE_HEADERS = {
        'Content-Type': 'application/json; charset=utf-8',
        'Cache-Control': 'no-cache',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    HOST = '0.0.0.0'

class TestingConfig(Config):
    """Configuración para testing"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    CACHE_TIMEOUT = 60  # Cache más corto para tests

# Seleccionar configuración según entorno
ENV = os.getenv('FLASK_ENV', 'development')

if ENV == 'production':
    config = ProductionConfig()
elif ENV == 'testing':
    config = TestingConfig()
else:
    config = DevelopmentConfig()

# Exportar configuración por defecto
__all__ = ['config', 'Config', 'DevelopmentConfig', 'ProductionConfig', 'TestingConfig']
