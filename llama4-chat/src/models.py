"""
Modelos de datos usando Pydantic
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Message(BaseModel):
    """Modelo para un mensaje del chat"""
    role: str = Field(..., description="Rol del mensaje: 'user' o 'assistant'")
    content: str = Field(..., description="Contenido del mensaje")

class ChatRequest(BaseModel):
    """Modelo para una solicitud de chat"""
    messages: List[Message] = Field(..., description="Lista de mensajes")
    stream: Optional[bool] = Field(False, description="Si usar streaming")
    max_tokens: Optional[int] = Field(512, description="Máximo de tokens")
    temperature: Optional[float] = Field(0.7, description="Temperatura de generación")

class Choice(BaseModel):
    """Modelo para una opción de respuesta"""
    message: Message
    finish_reason: Optional[str] = None
    index: Optional[int] = None

class ChatResponse(BaseModel):
    """Modelo para respuesta del chat"""
    id: Optional[str] = None
    object: Optional[str] = None
    created: Optional[int] = None
    model: Optional[str] = None
    choices: List[Choice] = []
    usage: Optional[Dict[str, Any]] = None

class StatusResponse(BaseModel):
    """Modelo para la respuesta de estado"""
    status: str = Field(..., description="Estado del servicio")
    nim_client: str = Field(..., description="Estado del cliente NIM")
    connection: str = Field(..., description="Estado de la conexión")
    model: str = Field(..., description="Modelo en uso")

class HealthResponse(BaseModel):
    """Modelo para health check"""
    status: str = Field("healthy", description="Estado de salud")
    service: str = Field("EdBetoSolutions Llama 4 Chat", description="Nombre del servicio")
