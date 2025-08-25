#!/bin/bash

echo "=== 🔍 DIAGNÓSTICO DEL SERVIDOR - edbetosolutions.tech ==="
echo ""

echo "📂 VERIFICANDO ESTRUCTURA DE ARCHIVOS:"
echo "Directory: /var/www/html/edbetosolutions"
ls -la /var/www/html/edbetosolutions/

echo ""
echo "📄 VERIFICANDO ARCHIVOS HTML:"
find /var/www/html/edbetosolutions -name "*.html" -type f

echo ""
echo "🔒 VERIFICANDO PERMISOS:"
ls -la /var/www/html/edbetosolutions/index.html 2>/dev/null || echo "❌ index.html no encontrado"
ls -la /var/www/html/edbetosolutions/frontend/ 2>/dev/null || echo "❌ directorio frontend no encontrado"

echo ""
echo "🌐 VERIFICANDO CONFIGURACIÓN NGINX:"
nginx -t
systemctl status nginx --no-pager -l

echo ""
echo "📋 VERIFICANDO LOGS RECIENTES:"
echo "--- Access Log (últimas 10 líneas) ---"
tail -10 /var/log/nginx/access.log 2>/dev/null || echo "❌ No se puede acceder al access log"

echo ""
echo "--- Error Log (últimas 10 líneas) ---"
tail -10 /var/log/nginx/error.log 2>/dev/null || echo "❌ No se puede acceder al error log"

echo ""
echo "✅ DIAGNÓSTICO COMPLETADO"
