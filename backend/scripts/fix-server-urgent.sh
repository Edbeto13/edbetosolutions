#!/bin/bash

echo "🚨 SCRIPT DE CORRECCIÓN URGENTE - edbetosolutions.tech"
echo "======================================================"
echo ""

echo "📍 Ubicación actual:"
pwd

echo ""
echo "🔍 PASO 1: Verificar estructura actual"
echo "--------------------------------------"
cd /var/www/html/edbetosolutions || { echo "❌ No se puede acceder al directorio del sitio"; exit 1; }

echo "📂 Contenido actual del directorio:"
ls -la

echo ""
echo "🔄 PASO 2: Actualizar código desde GitHub"
echo "------------------------------------------"
echo "🔄 Fetching latest changes..."
git fetch origin

echo "🔄 Resetting to latest main..."
git reset --hard origin/main

echo "🔄 Pulling latest changes..."
git pull origin main

echo "📊 Estado después del pull:"
git status

echo ""
echo "🔒 PASO 3: Corregir permisos"
echo "----------------------------"
echo "🔧 Ajustando permisos del propietario..."
chown -R www-data:www-data /var/www/html/edbetosolutions

echo "🔧 Ajustando permisos de archivos..."
find /var/www/html/edbetosolutions -type f -exec chmod 644 {} \;

echo "🔧 Ajustando permisos de directorios..."
find /var/www/html/edbetosolutions -type d -exec chmod 755 {} \;

echo ""
echo "📋 PASO 4: Verificar archivos críticos"
echo "--------------------------------------"
echo "🔍 index.html en raíz:"
ls -la /var/www/html/edbetosolutions/index.html 2>/dev/null && echo "✅ index.html encontrado" || echo "❌ index.html NO encontrado"

echo ""
echo "🔍 Directorio frontend:"
ls -la /var/www/html/edbetosolutions/frontend/ 2>/dev/null && echo "✅ directorio frontend encontrado" || echo "❌ directorio frontend NO encontrado"

echo ""
echo "🔍 Portafolio (landing page):"
ls -la /var/www/html/edbetosolutions/frontend/Portafolio/index.html 2>/dev/null && echo "✅ Portafolio encontrado" || echo "❌ Portafolio NO encontrado"

echo ""
echo "🔍 Chat Llama4:"
ls -la /var/www/html/edbetosolutions/frontend/llama4/index.html 2>/dev/null && echo "✅ Llama4 encontrado" || echo "❌ Llama4 NO encontrado"

echo ""
echo "🌐 PASO 5: Reiniciar nginx"
echo "-------------------------"
echo "🔄 Recargando configuración de nginx..."
nginx -t && echo "✅ Configuración de nginx válida" || echo "❌ Error en configuración de nginx"

systemctl reload nginx && echo "✅ nginx recargado exitosamente" || echo "❌ Error al recargar nginx"

echo ""
echo "📊 PASO 6: Verificación final"
echo "-----------------------------"
echo "📁 Estructura final:"
tree /var/www/html/edbetosolutions -L 3 2>/dev/null || find /var/www/html/edbetosolutions -type d | head -10

echo ""
echo "🎉 CORRECCIÓN COMPLETADA"
echo "========================"
echo "✅ Código actualizado desde GitHub"
echo "✅ Permisos corregidos (www-data:www-data)"
echo "✅ nginx recargado"
echo ""
echo "🌐 Verifica el sitio en: https://edbetosolutions.tech"
echo "📋 URLs importantes:"
echo "   • Principal: https://edbetosolutions.tech"
echo "   • Portafolio: https://edbetosolutions.tech/frontend/Portafolio/"
echo "   • Chat IA: https://edbetosolutions.tech/frontend/llama4/"
echo "   • Clima: https://edbetosolutions.tech/frontend/clima/"
