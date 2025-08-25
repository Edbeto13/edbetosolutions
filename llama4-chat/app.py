"""
Aplicación principal FastAPI para Llama 4 Chat
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import sys

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))

from nim_client import NimClient
from models import ChatRequest, StatusResponse, HealthResponse
from settings import config

# Inicializar FastAPI
app = FastAPI(
    title="EdBetoSolutions - Llama 4 Chat",
    description="Chat interactivo con Meta Llama 4 Maverick via NVIDIA NIM",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, cambiar por dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

# Inicializar cliente NIM
try:
    config.validate()
    nim_client = NimClient()
    print("✅ Cliente NIM inicializado correctamente")
except Exception as e:
    print(f"❌ Error al inicializar cliente NIM: {e}")
    nim_client = None

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    """Sirve la página principal del chat"""
    try:
        html_path = os.path.join(frontend_dir, "index.html")
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>Error: Archivo index.html no encontrado</h1>", 
            status_code=404
        )

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Endpoint principal para el chat con Llama 4"""
    if nim_client is None:
        raise HTTPException(status_code=500, detail="Cliente NIM no disponible")
    
    try:
        # Convertir mensajes al formato esperado
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        if not messages:
            raise HTTPException(status_code=400, detail="Se requiere al menos un mensaje")
        
        # Enviar solicitud a NVIDIA NIM
        response = nim_client.chat_completion(
            messages=messages,
            stream=request.stream or False,
            max_tokens=request.max_tokens or config.MAX_TOKENS,
            temperature=request.temperature or config.DEFAULT_TEMPERATURE
        )
        
        if "error" in response:
            raise HTTPException(status_code=500, detail=response["error"])
            
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.get("/api/status", response_model=StatusResponse)
async def get_status():
    """Endpoint para verificar el estado del servicio"""
    if nim_client is None:
        return StatusResponse(
            status="error",
            nim_client="no disponible",
            connection="fallida",
            model="N/A"
        )
    
    # Obtener estado del cliente
    client_status = nim_client.get_status()
    
    return StatusResponse(
        status=client_status["status"],
        nim_client="disponible",
        connection=client_status["connection"],
        model=client_status["model"]
    )

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check básico"""
    return HealthResponse()

@app.get("/api/info")
async def get_info():
    """Información sobre la aplicación"""
    return {
        "name": "EdBetoSolutions Llama 4 Chat",
        "version": "1.0.0",
        "model": config.NVIDIA_MODEL,
        "max_tokens": config.MAX_TOKENS,
        "char_limit": config.MAX_CHAR_LIMIT,
        "endpoints": {
            "chat": "/api/chat",
            "status": "/api/status",
            "health": "/api/health",
            "info": "/api/info"
        }
    }

def main():
    """Función principal para ejecutar el servidor"""
    print("🚀 Iniciando EdBetoSolutions - Llama 4 Chat...")
    print(f"📡 Servidor: http://{config.HOST}:{config.PORT}")
    print(f"🤖 Modelo: {config.NVIDIA_MODEL}")
    print("-" * 50)
    
    uvicorn.run(
        "app:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.RELOAD,
        log_level="info"
    )

if __name__ == "__main__":
    main()
