"""
Cliente para interactuar con NVIDIA NIM Service
"""
import requests
from typing import List, Dict, Optional
from config.settings import config

class NimClient:
    """Cliente para NVIDIA NIM API"""
    
    def __init__(self):
        self.api_url = config.NVIDIA_API_URL
        self.api_key = config.NVIDIA_API_KEY
        self.model = config.NVIDIA_MODEL
        
        if not self.api_key:
            raise ValueError("API key de NVIDIA NIM no configurada")
    
    def chat_completion(self, 
                       messages: List[Dict[str, str]], 
                       stream: bool = False,
                       max_tokens: int = None, 
                       temperature: float = None) -> Dict:
        """
        Envía una solicitud de chat a NVIDIA NIM
        
        Args:
            messages: Lista de mensajes [{"role": "user", "content": "texto"}]
            stream: Si usar streaming
            max_tokens: Máximo de tokens a generar
            temperature: Temperatura para la generación
            
        Returns:
            Respuesta de la API
        """
        if max_tokens is None:
            max_tokens = config.MAX_TOKENS
        if temperature is None:
            temperature = config.DEFAULT_TEMPERATURE
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "text/event-stream" if stream else "application/json",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 1.0,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "stream": stream
        }
        
        try:
            response = requests.post(
                self.api_url, 
                headers=headers, 
                json=payload, 
                timeout=config.API_TIMEOUT
            )
            response.raise_for_status()
            
            if stream:
                return response
            else:
                return response.json()
                
        except requests.exceptions.RequestException as e:
            return {"error": f"Error de conexión: {str(e)}"}
        except Exception as e:
            return {"error": f"Error inesperado: {str(e)}"}
    
    def test_connection(self) -> bool:
        """Prueba la conexión con la API"""
        try:
            test_messages = [{"role": "user", "content": "Test"}]
            response = self.chat_completion(test_messages, max_tokens=10)
            return "error" not in response and "choices" in response
        except:
            return False
    
    def get_status(self) -> Dict[str, str]:
        """Obtiene el estado del cliente"""
        connection_ok = self.test_connection()
        return {
            "status": "ok" if connection_ok else "error",
            "model": self.model,
            "connection": "exitosa" if connection_ok else "fallida"
        }
