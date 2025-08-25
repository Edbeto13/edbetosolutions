#!/usr/bin/env python3
"""
Backend API Server con integración NVIDIA NIM para Llama4
Author: EdbETO Solutions Team
Política: Solo datos reales, integración completa con NVIDIA
"""

import json
import os
import requests
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class NVIDIALlamaAPIHandler(BaseHTTPRequestHandler):
    
    # Configuración NVIDIA NIM
    NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
    # Obtener API key desde variable de entorno (más seguro)
    NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "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")
    NVIDIA_MODEL = "meta/llama-4-maverick-17b-128e-instruct"
    
    def do_OPTIONS(self):
        """Manejar preflight CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """Manejar requests GET"""
        path = self.path
        
        # Status endpoint
        if path == '/api/status':
            self.handle_status()
        
        # Health check
        elif path == '/health':
            self.handle_health()
        
        # Chat status (para Llama4)
        elif path == '/api/chat/status':
            self.handle_chat_status()
        
        else:
            self.send_404()
    
    def do_POST(self):
        """Manejar requests POST"""
        path = self.path
        
        # Chat endpoint (para Llama4)
        if path == '/api/chat':
            self.handle_chat()
        
        else:
            self.send_404()
    
    def handle_status(self):
        """Status general del API"""
        response = {
            "status": "ok",
            "message": "API funcionando correctamente con NVIDIA NIM",
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0",
            "services": {
                "llama4": "disponible",
                "nvidia_nim": "conectado",
                "model": self.NVIDIA_MODEL
            }
        }
        self.send_json_response(response)
    
    def handle_health(self):
        """Health check básico"""
        response = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "nvidia_integration": "active"
        }
        self.send_json_response(response)
    
    def handle_chat_status(self):
        """Status específico del chat Llama4"""
        try:
            # Probar conexión con NVIDIA
            test_response = self.test_nvidia_connection()
            
            if test_response:
                response = {
                    "status": "ok",
                    "message": "Servicio Llama4 disponible",
                    "model": self.NVIDIA_MODEL,
                    "timestamp": datetime.now().isoformat(),
                    "nvidia_status": "connected"
                }
                self.send_json_response(response)
            else:
                raise Exception("No se pudo conectar con NVIDIA NIM")
                
        except Exception as e:
            response = {
                "status": "error",
                "message": f"Error de conexión con NVIDIA: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
            self.send_response(503)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))
    
    def handle_chat(self):
        """Endpoint del chat Llama4 con NVIDIA NIM"""
        try:
            # Leer el body del request
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                body = self.rfile.read(content_length)
                data = json.loads(body.decode('utf-8'))
            else:
                data = {}
            
            # Obtener mensajes del request
            messages = data.get('messages', [])
            if not messages:
                raise ValueError("No se proporcionaron mensajes")
            
            # Configurar parámetros para NVIDIA
            temperature = data.get('temperature', 0.7)
            max_tokens = data.get('max_tokens', 512)
            
            # Llamar a NVIDIA NIM API
            nvidia_response = self.call_nvidia_api(messages, temperature, max_tokens)
            
            if nvidia_response and 'choices' in nvidia_response:
                # Formatear respuesta compatible con frontend
                response = {
                    "choices": nvidia_response['choices'],
                    "model": self.NVIDIA_MODEL,
                    "usage": nvidia_response.get('usage', {}),
                    "timestamp": datetime.now().isoformat()
                }
                self.send_json_response(response)
            else:
                raise Exception("Respuesta inválida de NVIDIA NIM")
            
        except ValueError as e:
            error_response = {
                "error": "invalid_request",
                "message": f"Request inválido: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(error_response, indent=2).encode('utf-8'))
            
        except Exception as e:
            print(f"❌ Error en chat: {e}")
            error_response = {
                "error": "nvidia_api_error", 
                "message": f"Error al comunicarse con NVIDIA: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
            self.send_response(502)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(error_response, indent=2).encode('utf-8'))
    
    def test_nvidia_connection(self):
        """Probar conexión con NVIDIA NIM"""
        try:
            headers = {
                "Authorization": f"Bearer {self.NVIDIA_API_KEY}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.NVIDIA_MODEL,
                "messages": [{"role": "user", "content": "test"}],
                "max_tokens": 10,
                "temperature": 0.1
            }
            
            response = requests.post(
                self.NVIDIA_API_URL, 
                headers=headers, 
                json=payload,
                timeout=10
            )
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"⚠️ Error al probar conexión NVIDIA: {e}")
            return False
    
    def call_nvidia_api(self, messages, temperature=0.7, max_tokens=512):
        """Llamar a NVIDIA NIM API"""
        headers = {
            "Authorization": f"Bearer {self.NVIDIA_API_KEY}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.NVIDIA_MODEL,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 1.00,
            "frequency_penalty": 0.00,
            "presence_penalty": 0.00,
            "stream": False
        }
        
        print(f"🚀 Enviando request a NVIDIA: {len(messages)} mensajes")
        
        response = requests.post(
            self.NVIDIA_API_URL, 
            headers=headers, 
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Respuesta recibida de NVIDIA")
            return result
        else:
            print(f"❌ Error NVIDIA API: {response.status_code} - {response.text}")
            raise Exception(f"NVIDIA API error: {response.status_code}")
    
    def send_json_response(self, data, status_code=200):
        """Enviar respuesta JSON"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2, ensure_ascii=False).encode('utf-8'))
    
    def send_404(self):
        """Enviar error 404"""
        response = {
            "error": "not_found",
            "message": f"Endpoint no encontrado: {self.path}",
            "timestamp": datetime.now().isoformat()
        }
        self.send_response(404)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Log personalizado"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")

def run_nvidia_server(port=8000):
    """Ejecutar servidor con integración NVIDIA NIM"""
    server = HTTPServer(('0.0.0.0', port), NVIDIALlamaAPIHandler)
    print(f"🦙 Servidor Llama4 + NVIDIA NIM iniciado en puerto {port}")
    print(f"📡 Endpoints disponibles:")
    print(f"   http://localhost:{port}/api/status")
    print(f"   http://localhost:{port}/api/chat")
    print(f"   http://localhost:{port}/api/chat/status")
    print(f"   http://localhost:{port}/health")
    print(f"")
    print(f"🎯 Modelo: {NVIDIALlamaAPIHandler.NVIDIA_MODEL}")
    
    # Verificar si se está usando la API key del entorno o el fallback
    if os.environ.get("NVIDIA_API_KEY"):
        print(f"🔐 NVIDIA NIM: Usando API key desde variable de entorno")
    else:
        print(f"⚠️ NVIDIA NIM: Usando API key de fallback del código (recomendado: usar variable de entorno)")
        
    print(f"🔗 NVIDIA NIM: Integración activa")
    print(f"⚡ Política: Solo datos reales de NVIDIA")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")
        server.shutdown()

if __name__ == "__main__":
    run_nvidia_server()
