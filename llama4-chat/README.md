# Llama4 Chat - Deployment Guide

## 📋 Descripción
Chat interactivo con **Meta Llama 4 Maverick 17B** usando NVIDIA NIM Service. Aplicación FastAPI con frontend moderno y responsivo.

## 🏗️ Arquitectura
```
llama4-chat/
├── app.py              # Aplicación FastAPI principal
├── requirements.txt    # Dependencias Python
├── .env               # Variables de entorno (NO incluir en git)
├── deploy.sh          # Script de deployment para Linux
├── deploy.ps1         # Script de deployment para Windows
├── src/               # Código fuente
│   ├── nim_client.py  # Cliente NVIDIA NIM API
│   └── models.py      # Modelos Pydantic
├── config/            # Configuración
│   └── settings.py    # Settings centralizados
├── templates/         # Templates HTML
│   └── index.html     # Frontend principal
└── static/           # Archivos estáticos
    ├── css/styles.css # Estilos CSS
    └── js/            # JavaScript
        ├── chat.js    # Lógica del chat
        └── ui.js      # Gestión de UI
```

## 🚀 Deployment Rápido

### Opción 1: Script Automático (Recomendado)

#### En Windows:
```powershell
.\deploy.ps1 -ServerIP "YOUR_DROPLET_IP"
```

#### En el Servidor Linux:
```bash
chmod +x deploy.sh
sudo ./deploy.sh
```

### Opción 2: Deployment Manual

#### 1. Subir archivos al servidor
```bash
scp -r llama4-chat/ root@YOUR_DROPLET_IP:/var/www/
```

#### 2. Instalar dependencias
```bash
ssh root@YOUR_DROPLET_IP
cd /var/www/llama4-chat
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 3. Configurar variables de entorno
```bash
# Editar .env con tu API key real
nano .env
```

#### 4. Configurar servicios del sistema
```bash
# El script deploy.sh hace esto automáticamente
sudo ./deploy.sh
```

## ⚙️ Configuración

### Variables de Entorno (.env)
```bash
NVIDIA_API_KEY=tu_api_key_aqui
HOST=127.0.0.1
PORT=8000
DEBUG=False
RELOAD=False
NVIDIA_MODEL=meta/llama-4-maverick-17b-128e-instruct
MAX_TOKENS=1024
DEFAULT_TEMPERATURE=0.7
MAX_CHAR_LIMIT=8000
```

### Configuración Nginx
El script de deployment configura automáticamente Nginx para:
- Servir la aplicación en el puerto 80
- Proxy reverso a FastAPI (puerto 8000)
- Servir archivos estáticos optimizados
- Configurar headers de seguridad

### Configuración Supervisor
Gestiona automáticamente:
- Auto-inicio del servicio
- Reinicio automático en caso de fallo
- Logs estructurados
- Gestión de procesos

## 🛠️ Operaciones

### Verificar Estado
```bash
sudo supervisorctl status llama4-chat
sudo systemctl status nginx
```

### Ver Logs
```bash
sudo tail -f /var/log/llama4-chat.out.log
sudo tail -f /var/log/llama4-chat.err.log
```

### Reiniciar Servicios
```bash
sudo supervisorctl restart llama4-chat
sudo systemctl restart nginx
```

### Actualizar Aplicación
```bash
cd /var/www/llama4-chat
git pull  # Si usas git
source venv/bin/activate
pip install -r requirements.txt
sudo supervisorctl restart llama4-chat
```

## 🌐 URLs de Acceso

### Producción
- **Principal**: http://llama4.edbetosolutions.com
- **IP Directa**: http://YOUR_DROPLET_IP

### Desarrollo Local
- **Local**: http://localhost:8000

## 🔒 Seguridad

### Consideraciones
- ✅ API Key configurada como variable de entorno
- ✅ CORS configurado para dominios específicos en producción
- ✅ Nginx como proxy reverso
- ✅ Aplicación ejecutándose como usuario www-data
- ✅ Logs estructurados para auditoría

### Recomendaciones
- [ ] Configurar SSL/TLS con Let's Encrypt
- [ ] Implementar rate limiting
- [ ] Configurar firewall (UFW)
- [ ] Backup automático de configuraciones

## 📊 Monitoreo

### Métricas Disponibles
- Logs de aplicación: `/var/log/llama4-chat.out.log`
- Logs de errores: `/var/log/llama4-chat.err.log`
- Logs de Nginx: `/var/log/nginx/access.log`
- Estado de servicios: `supervisorctl status`

### Endpoints de Salud
- `GET /api/health` - Health check básico
- `GET /api/status` - Estado detallado del servicio
- `GET /api/info` - Información de la aplicación

## 🐛 Troubleshooting

### Problemas Comunes

#### Error: Cliente NIM no disponible
```bash
# Verificar API key
grep NVIDIA_API_KEY /var/www/llama4-chat/.env
# Verificar conectividad
curl -H "Authorization: Bearer $NVIDIA_API_KEY" https://integrate.api.nvidia.com/v1/chat/completions
```

#### Error 502 Bad Gateway
```bash
# Verificar que FastAPI está ejecutándose
sudo supervisorctl status llama4-chat
# Verificar logs
sudo tail -f /var/log/llama4-chat.err.log
```

#### Alta latencia
```bash
# Verificar recursos del servidor
htop
df -h
# Verificar logs de Nginx
sudo tail -f /var/log/nginx/access.log
```

## 📞 Soporte
- **Desarrollador**: EdBeto Solutions
- **Docs NVIDIA NIM**: https://docs.nvidia.com/nim/
- **FastAPI Docs**: https://fastapi.tiangolo.com/

---
**Versión**: 1.0.0  
**Última actualización**: Agosto 2025
