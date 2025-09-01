# Utilidades Backend - EdbETO Solutions
# Funciones comunes y helpers para el backend

import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional

# Configurar logging básico
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def setup_cors_headers() -> Dict[str, str]:
    """
    Configura headers CORS estándar para las APIs
    
    Returns:
        Dict con headers CORS configurados
    """
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json; charset=utf-8'
    }

def create_json_response(data: Any, status_code: int = 200) -> tuple:
    """
    Crea una respuesta JSON estándar para las APIs
    
    Args:
        data: Datos a incluir en la respuesta
        status_code: Código de estado HTTP
        
    Returns:
        Tuple (data_json, status_code, headers)
    """
    headers = setup_cors_headers()
    
    response_data = {
        'status': 'success' if status_code < 400 else 'error',
        'timestamp': datetime.now().isoformat(),
        'data': data
    }
    
    return json.dumps(response_data, ensure_ascii=False), status_code, headers

def create_error_response(message: str, status_code: int = 500) -> tuple:
    """
    Crea una respuesta de error estándar
    
    Args:
        message: Mensaje de error
        status_code: Código de estado HTTP
        
    Returns:
        Tuple (error_json, status_code, headers)
    """
    headers = setup_cors_headers()
    
    error_data = {
        'status': 'error',
        'timestamp': datetime.now().isoformat(),
        'error': {
            'message': message,
            'code': status_code
        }
    }
    
    return json.dumps(error_data, ensure_ascii=False), status_code, headers

def log_request(method: str, path: str, ip: str = 'unknown') -> None:
    """
    Registra una petición HTTP en los logs
    
    Args:
        method: Método HTTP (GET, POST, etc.)
        path: Ruta solicitada
        ip: IP del cliente
    """
    logger = logging.getLogger('backend')
    logger.info(f"{method} {path} - IP: {ip}")

def validate_json_data(data: str) -> Optional[Dict]:
    """
    Valida y parsea datos JSON
    
    Args:
        data: String JSON a validar
        
    Returns:
        Dict con los datos parseados o None si hay error
    """
    try:
        return json.loads(data)
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing JSON: {e}")
        return None

def safe_file_read(file_path: str) -> Optional[str]:
    """
    Lee un archivo de forma segura
    
    Args:
        file_path: Ruta del archivo
        
    Returns:
        Contenido del archivo o None si hay error
    """
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            logging.warning(f"File not found: {file_path}")
            return None
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return None

def safe_file_write(file_path: str, content: str) -> bool:
    """
    Escribe un archivo de forma segura
    
    Args:
        file_path: Ruta del archivo
        content: Contenido a escribir
        
    Returns:
        True si se escribió correctamente, False en caso contrario
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        logging.error(f"Error writing file {file_path}: {e}")
        return False

def get_cache_file_path(cache_name: str) -> str:
    """
    Obtiene la ruta del archivo de cache
    
    Args:
        cache_name: Nombre del cache
        
    Returns:
        Ruta completa del archivo de cache
    """
    cache_dir = os.path.join(os.path.dirname(__file__), 'cache')
    os.makedirs(cache_dir, exist_ok=True)
    return os.path.join(cache_dir, f"{cache_name}.json")

def is_cache_valid(cache_file: str, max_age_seconds: int = 4500) -> bool:
    """
    Verifica si un archivo de cache es válido
    
    Args:
        cache_file: Ruta del archivo de cache
        max_age_seconds: Edad máxima en segundos (default: 75 minutos)
        
    Returns:
        True si el cache es válido, False en caso contrario
    """
    try:
        if not os.path.exists(cache_file):
            return False
            
        file_age = datetime.now().timestamp() - os.path.getmtime(cache_file)
        return file_age < max_age_seconds
    except Exception as e:
        logging.error(f"Error checking cache validity: {e}")
        return False

# Constantes útiles
HTTP_METHODS = {
    'GET': 'GET',
    'POST': 'POST',
    'PUT': 'PUT',
    'DELETE': 'DELETE',
    'OPTIONS': 'OPTIONS'
}

CONTENT_TYPES = {
    'json': 'application/json; charset=utf-8',
    'html': 'text/html; charset=utf-8',
    'text': 'text/plain; charset=utf-8'
}

# Exportar funciones principales
__all__ = [
    'setup_cors_headers',
    'create_json_response', 
    'create_error_response',
    'log_request',
    'validate_json_data',
    'safe_file_read',
    'safe_file_write',
    'get_cache_file_path',
    'is_cache_valid',
    'HTTP_METHODS',
    'CONTENT_TYPES'
]
