"""
Configuración principal para la aplicación Llama 4 Chat
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Configuración base"""
    # API de NVIDIA NIM
    NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
    NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
    NVIDIA_MODEL = "meta/llama-4-maverick-17b-128e-instruct"
    
    # Servidor
    HOST = "0.0.0.0"
    PORT = 8000
    DEBUG = True
    RELOAD = True
    
    # Chat configuración
    MAX_TOKENS = 512
    DEFAULT_TEMPERATURE = 0.7
    MAX_CHAR_LIMIT = 2000
    
    # Timeouts
    API_TIMEOUT = 30
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
    
    @classmethod
    def validate(cls):
        """Valida que la configuración sea correcta"""
        if not cls.NVIDIA_API_KEY:
            raise ValueError("NVIDIA_API_KEY no encontrada en las variables de entorno")
        return True

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    RELOAD = True

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    RELOAD = False
    HOST = "0.0.0.0"

# Configuración activa
config = DevelopmentConfig()
