#!/bin/bash

# Deploy script para Llama4 Chat en el droplet
# Uso: ./deploy.sh

echo "🚀 Iniciando deployment de Llama4 Chat..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuración
APP_DIR="/var/www/llama4-chat"
SERVICE_NAME="llama4-chat"
NGINX_CONF="/etc/nginx/sites-available/llama4-chat"

# Función para logging
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

# Verificar que estamos corriendo como root
if [ "$EUID" -ne 0 ]; then 
    error "Este script debe ejecutarse como root (sudo)"
    exit 1
fi

# Crear directorio de aplicación
log "Creando directorio de aplicación..."
mkdir -p $APP_DIR
cd $APP_DIR

# Instalar dependencias del sistema
log "Instalando dependencias del sistema..."
apt update
apt install -y python3 python3-pip python3-venv nginx supervisor

# Crear entorno virtual
log "Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias Python
log "Instalando dependencias Python..."
pip install --upgrade pip
pip install -r requirements.txt

# Configurar variables de entorno
log "Configurando variables de entorno..."
if [ ! -f .env ]; then
    cat > .env << EOF
# Configuración de NVIDIA NIM Service
NVIDIA_API_KEY=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

# Configuración del servidor
HOST=127.0.0.1
PORT=8000
DEBUG=False
RELOAD=False

# Configuración del modelo
NVIDIA_MODEL=meta/llama-4-maverick-17b-128e-instruct
MAX_TOKENS=1024
DEFAULT_TEMPERATURE=0.7
MAX_CHAR_LIMIT=8000
EOF
    log "Archivo .env creado. ¡IMPORTANTE: Actualiza NVIDIA_API_KEY!"
fi

# Configurar Supervisor
log "Configurando Supervisor..."
cat > /etc/supervisor/conf.d/$SERVICE_NAME.conf << EOF
[program:$SERVICE_NAME]
command=$APP_DIR/venv/bin/uvicorn app:app --host 127.0.0.1 --port 8000
directory=$APP_DIR
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/$SERVICE_NAME.err.log
stdout_logfile=/var/log/$SERVICE_NAME.out.log
environment=PATH="$APP_DIR/venv/bin"
EOF

# Configurar Nginx
log "Configurando Nginx..."
cat > $NGINX_CONF << EOF
server {
    listen 80;
    server_name llama4.edbetosolutions.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Servir archivos estáticos
    location /static {
        alias $APP_DIR/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Habilitar sitio Nginx
ln -sf $NGINX_CONF /etc/nginx/sites-enabled/
nginx -t

# Configurar permisos
log "Configurando permisos..."
chown -R www-data:www-data $APP_DIR
chmod -R 755 $APP_DIR

# Reiniciar servicios
log "Reiniciando servicios..."
supervisorctl reread
supervisorctl update
supervisorctl restart $SERVICE_NAME
systemctl restart nginx

# Verificar estado
log "Verificando estado de los servicios..."
if supervisorctl status $SERVICE_NAME | grep RUNNING; then
    log "✅ Servicio $SERVICE_NAME está ejecutándose"
else
    error "❌ Error al iniciar $SERVICE_NAME"
    supervisorctl tail $SERVICE_NAME stderr
fi

if systemctl is-active --quiet nginx; then
    log "✅ Nginx está ejecutándose"
else
    error "❌ Error con Nginx"
fi

log "🎉 Deployment completado!"
log "🌐 Aplicación disponible en: http://llama4.edbetosolutions.com"
log "📊 Logs disponibles en:"
log "   - /var/log/$SERVICE_NAME.out.log"
log "   - /var/log/$SERVICE_NAME.err.log"
log ""
log "Para monitorear:"
log "   sudo supervisorctl status $SERVICE_NAME"
log "   sudo tail -f /var/log/$SERVICE_NAME.out.log"
