#!/bin/bash
# Script de instalación del backend para edbetosolutions.tech
# Ejecutar como: sudo ./install-backend.sh

echo "🚀 Instalando Backend de EdbETO Solutions..."

# Crear directorio de aplicación
sudo mkdir -p /opt/edbeto-backend
sudo mkdir -p /var/log/conagua-api

# Copiar archivos del backend
sudo cp -r src/backend/* /opt/edbeto-backend/
sudo chown -R www-data:www-data /opt/edbeto-backend
sudo chmod 755 /opt/edbeto-backend

# Instalar dependencias Python
cd /opt/edbeto-backend
sudo -u www-data python3 -m pip install -r requirements.txt

# Configurar servicio systemd
sudo cp deploy/conagua-api.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable conagua-api

# Configurar nginx
sudo cp nginx-production.conf /etc/nginx/sites-available/edbetosolutions
sudo ln -sf /etc/nginx/sites-available/edbetosolutions /etc/nginx/sites-enabled/
sudo nginx -t

# Iniciar servicios
sudo systemctl start conagua-api
sudo systemctl reload nginx

# Verificar estado
echo "📊 Estado de los servicios:"
sudo systemctl status conagua-api --no-pager
echo ""
echo "🌐 Backend instalado correctamente en:"
echo "  - API: http://edbetosolutions.tech/api/"
echo "  - Logs: /var/log/conagua-api/"
echo "  - Servicio: systemctl status conagua-api"

echo "✅ Instalación completada!"
