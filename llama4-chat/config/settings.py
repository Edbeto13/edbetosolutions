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
    NVIDIA_MODEL = os.getenv("NVIDIA_MODEL", "meta/llama-4-maverick-17b-128e-instruct")
    
    # Servidor
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    RELOAD = os.getenv("RELOAD", "True").lower() == "true"
    
    # Chat configuración
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", 1024))
    DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", 0.7))
    MAX_CHAR_LIMIT = int(os.getenv("MAX_CHAR_LIMIT", 8000))
    
    # Timeouts
    API_TIMEOUT = 30
    
    # CORS - Configuración dinámica
    @property
    def CORS_ORIGINS(self):
        if self.DEBUG:
            return ["*"]  # Desarrollo
        else:
            return [
                "https://llama4.edbetosolutions.com",
                "https://edbetosolutions.com",
                "http://llama4.edbetosolutions.com"
            ]
    
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
