#!/usr/bin/env python3
"""
Backend API Server simplificado para Llama4 y servicios básicos
Author: EdbETO Solutions Team
Política: Solo datos reales, no fallbacks
"""

import json
import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class SimpleAPIHandler(BaseHTTPRequestHandler):
    
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
            "message": "API funcionando correctamente",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "services": {
                "llama4": "disponible",
                "conagua": "datos_reales_solamente"
            }
        }
        self.send_json_response(response)
    
    def handle_health(self):
        """Health check básico"""
        response = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat()
        }
        self.send_json_response(response)
    
    def handle_chat_status(self):
        """Status específico del chat Llama4"""
        response = {
            "status": "error",
            "message": "Servicio Llama4 temporalmente no disponible",
            "reason": "nvidia_nim_not_configured",
            "timestamp": datetime.now().isoformat()
        }
        # Devolver error 503 - Service Unavailable
        self.send_response(503)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))
    
    def handle_chat(self):
        """Endpoint del chat Llama4"""
        try:
            # Leer el body del request
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                body = self.rfile.read(content_length)
                data = json.loads(body.decode('utf-8'))
            else:
                data = {}
            
            # Respuesta indicando que el servicio no está disponible
            response = {
                "error": "service_unavailable",
                "message": "El servicio de chat Llama4 no está disponible en este momento",
                "details": "NVIDIA NIM Service no configurado - Solo datos reales disponibles",
                "timestamp": datetime.now().isoformat(),
                "user_message": data.get("message", ""),
                "suggestion": "El administrador debe configurar las credenciales de NVIDIA NIM"
            }
            
            # Devolver error 503 - Service Unavailable
            self.send_response(503)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))
            
        except Exception as e:
            error_response = {
                "error": "internal_error",
                "message": f"Error interno: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(error_response, indent=2).encode('utf-8'))
    
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

def run_simple_server(port=8000):
    """Ejecutar servidor simple"""
    server = HTTPServer(('0.0.0.0', port), SimpleAPIHandler)
    print(f"🚀 Servidor API Simple iniciado en puerto {port}")
    print(f"📡 Endpoints disponibles:")
    print(f"   http://localhost:{port}/api/status")
    print(f"   http://localhost:{port}/api/chat (503 - no disponible)")
    print(f"   http://localhost:{port}/health")
    print(f"")
    print(f"🎯 Política: Solo datos reales, no fallbacks")
    print(f"⚠️  Llama4 deshabilitado hasta configurar NVIDIA NIM")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")
        server.shutdown()

if __name__ == "__main__":
    run_simple_server()
