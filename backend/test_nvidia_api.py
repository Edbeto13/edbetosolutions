#!/usr/bin/env python3
"""
NVIDIA NIM API Test Script
--------------------------
Este script prueba la conexión a la API de NVIDIA NIM para el modelo Llama 4
y verifica que la integración esté funcionando correctamente.

Autor: EdBetoSolutions
Fecha: 2024
"""

import requests
import os
import json
import sys
import time
from datetime import datetime

# Colores para output en terminal
class Colors:
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def print_colored(color, symbol, message):
    """Imprime un mensaje con color y símbolo"""
    print(f"{color}{symbol} {message}{Colors.NC}")

def info(message):
    print_colored(Colors.BLUE, "ℹ", message)

def success(message):
    print_colored(Colors.GREEN, "✓", message)

def warning(message):
    print_colored(Colors.YELLOW, "⚠", message)

def error(message):
    print_colored(Colors.RED, "✗", message)

def get_api_key():
    """Obtiene la API key de NVIDIA desde variables de entorno o solicita al usuario"""
    api_key = os.environ.get("NVIDIA_API_KEY")
    
    if not api_key:
        warning("No se encontró la variable de entorno NVIDIA_API_KEY")
        api_key = input("Por favor ingresa tu API key de NVIDIA NIM: ")
        
        if not api_key:
            error("No se proporcionó una API key válida")
            sys.exit(1)
    
    return api_key

def test_direct_nvidia_api(api_key):
    """Prueba la conexión directa a la API de NVIDIA NIM"""
    info("Probando conexión directa a NVIDIA NIM API...")
    
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messages": [
            {"role": "user", "content": "Hola, ¿quién eres?"}
        ],
        "model": "meta/llama4-maverick-17b",
        "max_tokens": 150
    }
    
    try:
        start_time = time.time()
        response = requests.post(url, json=data, headers=headers)
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            success(f"Conexión exitosa a NVIDIA NIM API (tiempo: {elapsed_time:.2f}s)")
            info(f"Respuesta: {content[:100]}...")
            return True
        else:
            error(f"Error al conectar con NVIDIA NIM API: {response.status_code}")
            warning(f"Detalle: {response.text[:200]}...")
            return False
    
    except Exception as e:
        error(f"Excepción al conectar con NVIDIA NIM API: {str(e)}")
        return False

def test_local_api_server(base_url="http://localhost:8000"):
    """Prueba el servidor local de la API de NVIDIA"""
    info(f"Probando servidor local en {base_url}...")
    
    endpoints = {
        "health": f"{base_url}/health",
        "status": f"{base_url}/api/status",
        "chat_status": f"{base_url}/api/chat/status"
    }
    
    # Comprobar endpoints básicos
    for name, url in endpoints.items():
        try:
            response = requests.get(url)
            if response.status_code == 200:
                success(f"Endpoint {name}: OK ({response.status_code})")
            else:
                error(f"Endpoint {name}: FALLO ({response.status_code})")
        except Exception as e:
            error(f"No se pudo conectar con {name}: {str(e)}")
            return False
    
    # Probar el endpoint de chat
    chat_url = f"{base_url}/api/chat"
    data = {
        "messages": [
            {"role": "user", "content": "Hola, dime quién eres en una frase corta"}
        ]
    }
    
    try:
        info("Enviando mensaje de prueba al API de chat...")
        start_time = time.time()
        response = requests.post(chat_url, json=data)
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            content = result.get("content", "")
            
            success(f"API de chat respondió correctamente (tiempo: {elapsed_time:.2f}s)")
            info(f"Respuesta: {content[:100]}...")
            return True
        else:
            error(f"Error en API de chat: {response.status_code}")
            warning(f"Detalle: {response.text[:200]}...")
            return False
    
    except Exception as e:
        error(f"Excepción al conectar con API de chat: {str(e)}")
        return False

def test_production_api(base_url="https://edbetosolutions.tech"):
    """Prueba el servidor de producción"""
    info(f"Probando servidor de producción en {base_url}...")
    return test_local_api_server(base_url)

def main():
    """Función principal"""
    print("\n" + "=" * 60)
    print("  NVIDIA NIM API TEST - LLAMA 4")
    print("=" * 60)
    print(f"  Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60 + "\n")
    
    # Obtener API key
    api_key = get_api_key()
    
    # Probar conexión directa a NVIDIA
    direct_test = test_direct_nvidia_api(api_key)
    
    print("\n" + "-" * 60)
    
    # Probar servidor local
    local_test = test_local_api_server()
    
    print("\n" + "-" * 60)
    
    # Preguntar si desea probar el servidor de producción
    test_prod = input("\n¿Deseas probar el servidor de producción? (s/n): ").lower() == 's'
    
    if test_prod:
        print("\n" + "-" * 60)
        prod_test = test_production_api()
    else:
        prod_test = None
    
    # Resumen
    print("\n" + "=" * 60)
    print("  RESUMEN DE PRUEBAS")
    print("=" * 60)
    print(f"  API NVIDIA directa:  {'✓ ÉXITO' if direct_test else '✗ FALLO'}")
    print(f"  Servidor local:      {'✓ ÉXITO' if local_test else '✗ FALLO'}")
    
    if prod_test is not None:
        print(f"  Servidor producción: {'✓ ÉXITO' if prod_test else '✗ FALLO'}")
    
    print("=" * 60 + "\n")
    
    # Sugerencias
    if not direct_test:
        warning("⚠ La API key podría no ser válida o el servicio NVIDIA NIM podría estar caído.")
        warning("  Verifica tu API key y tu conexión a internet.")
    
    if not local_test:
        warning("⚠ El servidor local no está respondiendo correctamente.")
        warning("  Verifica que el servidor esté en ejecución con 'run_nvidia_server.sh status'")
    
    if test_prod and not prod_test:
        warning("⚠ El servidor de producción no está respondiendo correctamente.")
        warning("  Verifica la configuración de Nginx y que el servidor esté en ejecución.")

if __name__ == "__main__":
    main()
