# 🦙 Llama 4 con NVIDIA NIM - Guía de Implementación

Este documento explica cómo configurar y ejecutar el backend de Llama 4 con integración a NVIDIA NIM API.

## 📋 Requisitos

- Python 3.7+
- Biblioteca `requests`
- API key de NVIDIA NIM
- Acceso SSH al servidor

## 🔑 Configuración de API Key

Por seguridad, la API key de NVIDIA debe configurarse como variable de entorno:

```bash
# Configurar API key temporalmente (sesión actual)
export NVIDIA_API_KEY="tu-api-key-de-nvidia-nim"

# O configurar permanentemente en ~/.bashrc o ~/.profile
echo 'export NVIDIA_API_KEY="tu-api-key-de-nvidia-nim"' >> ~/.bashrc
source ~/.bashrc
```

> ⚠️ **IMPORTANTE**: No compartas tu API key en repositorios públicos ni la incluyas en el código.

## 🚀 Ejecución Manual

Para ejecutar el servidor manualmente:

```bash
# Ir al directorio del backend
cd /var/www/html/edbetosolutions/backend

# Ejecutar en primer plano para depuración
python3 nvidia_api_server.py

# Ejecutar en segundo plano
nohup python3 nvidia_api_server.py > nvidia_server.log 2>&1 &
```

## 🛠️ Script de Control

También puedes usar el script de control para gestionar el servidor:

```bash
# Ir al directorio de scripts
cd /var/www/html/edbetosolutions/backend/scripts

# Dar permisos de ejecución
chmod +x run_nvidia_server.sh

# Iniciar el servidor
./run_nvidia_server.sh start

# Ver estado
./run_nvidia_server.sh status

# Ver logs en tiempo real
./run_nvidia_server.sh logs

# Detener el servidor
./run_nvidia_server.sh stop
```

## 🔍 Prueba del API

Para verificar que el servidor está funcionando correctamente:

```bash
# Health check
curl -s http://localhost:8000/health | jq

# Estado del API
curl -s http://localhost:8000/api/status | jq

# Estado del chat
curl -s http://localhost:8000/api/chat/status -i

# Enviar un mensaje
curl -X POST -H "Content-Type: application/json" \
    -d '{"messages":[{"role":"user","content":"Hola, ¿cómo estás?"}]}' \
    http://localhost:8000/api/chat | jq
```

## 🔐 Seguridad

- **Acceso**: Limita el acceso al API mediante firewall o nginx
- **API Keys**: Almacena la API key de NVIDIA en variables de entorno
- **HTTPS**: Configura nginx para proporcionar HTTPS

## 🌐 Configuración con Nginx

Para exponer el API a través de nginx:

```nginx
# En /etc/nginx/sites-available/edbetosolutions.tech
location /api/chat {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}

location /api/chat/status {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}

location /api/status {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

## 🚑 Solución de Problemas

1. **Error de conexión**: Verifica la API key y conexión a internet
2. **Error 502**: El servidor NVIDIA podría estar sobrecargado, reintenta
3. **Error 503**: El servicio no está disponible o configurado correctamente
4. **Logs vacíos**: Verifica permisos del directorio para escritura

## 📊 Monitoreo

Para monitorear el servidor en producción:

```bash
# Ver logs en tiempo real
tail -f /var/www/html/edbetosolutions/backend/nvidia_server.log

# Monitorear proceso
ps aux | grep nvidia_api_server.py

# Uso de CPU/memoria
htop -p $(pgrep -f nvidia_api_server.py)
```

---

Desarrollado por EdBetoSolutions © 2025
