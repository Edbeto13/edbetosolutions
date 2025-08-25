#!/bin/bash
# 🚀 Script de Deployment Seguro para UNEGario
# Autor: EdbETO Solutions
# Fecha: 24 Agosto 2025

set -e  # Terminar en caso de error

# Configuración
SERVER="146.190.249.76"
USER="root"
REMOTE_PATH="/var/www/html"
LOCAL_PATH="src/frontend/UNEGario"
BACKUP_PATH="/root/backups"
DATE=$(date +%Y%m%d_%H%M%S)

echo "🚀 Iniciando deployment de UNEGario..."

# Función para log con timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Función de cleanup en caso de error
cleanup() {
    log "❌ Error detectado. Limpiando archivos temporales..."
    ssh ${USER}@${SERVER} "rm -rf /tmp/UNEGario_new" 2>/dev/null || true
    exit 1
}

trap cleanup ERR

# Paso 1: Verificaciones pre-deployment
log "🔍 Verificando estado local..."
if [ ! -d "${LOCAL_PATH}" ]; then
    log "❌ Error: Directorio local ${LOCAL_PATH} no encontrado"
    exit 1
fi

log "🔍 Verificando conectividad al servidor..."
if ! ssh ${USER}@${SERVER} "echo 'Conexión exitosa'" >/dev/null 2>&1; then
    log "❌ Error: No se puede conectar al servidor ${SERVER}"
    exit 1
fi

log "🔍 Verificando estado del servicio web..."
if ! curl -s -f https://edbetosolutions.tech/UNEGario >/dev/null; then
    log "⚠️  Advertencia: El sitio no responde correctamente"
fi

# Paso 2: Crear backup
log "💾 Creando backup de la versión actual..."
ssh ${USER}@${SERVER} "
    mkdir -p ${BACKUP_PATH}
    cd ${REMOTE_PATH}
    if [ -d 'UNEGario' ]; then
        tar -czf ${BACKUP_PATH}/UNEGario_backup_${DATE}.tar.gz UNEGario/
        log '✅ Backup creado: UNEGario_backup_${DATE}.tar.gz'
    else
        log '⚠️  No existe versión anterior para backup'
    fi
"

# Paso 3: Subir nueva versión
log "📤 Subiendo nueva versión al servidor..."
scp -r "${LOCAL_PATH}" ${USER}@${SERVER}:/tmp/UNEGario_new

# Paso 4: Verificar archivos subidos
log "🔍 Verificando archivos subidos..."
ssh ${USER}@${SERVER} "
    if [ ! -d '/tmp/UNEGario_new' ]; then
        log '❌ Error: Los archivos no se subieron correctamente'
        exit 1
    fi
    
    # Verificar archivos críticos
    for file in 'UNEGario.html' 'unegario.js' 'UNEGarioimages'; do
        if [ ! -e \"/tmp/UNEGario_new/\$file\" ]; then
            log \"❌ Error: Archivo crítico \$file no encontrado\"
            exit 1
        fi
    done
    
    log '✅ Todos los archivos críticos verificados'
"

# Paso 5: Configurar permisos
log "🔐 Configurando permisos..."
ssh ${USER}@${SERVER} "
    chown -R www-data:www-data /tmp/UNEGario_new/
    chmod -R 755 /tmp/UNEGario_new/
    log '✅ Permisos configurados'
"

# Paso 6: Deployment atómico
log "⚡ Ejecutando deployment atómico..."
ssh ${USER}@${SERVER} "
    cd ${REMOTE_PATH}
    
    # Crear respaldo de la versión actual
    if [ -d 'UNEGario' ]; then
        mv UNEGario UNEGario_old
    fi
    
    # Mover nueva versión
    mv /tmp/UNEGario_new UNEGario
    
    log '✅ Deployment atómico completado'
"

# Paso 7: Verificación post-deployment
log "🔍 Verificando deployment..."
sleep 2  # Dar tiempo al servidor web

# Verificar respuesta HTTP
if curl -s -f https://edbetosolutions.tech/UNEGario >/dev/null; then
    log "✅ Sitio web responde correctamente"
else
    log "❌ Error: El sitio no responde. Iniciando rollback..."
    
    # Rollback automático
    ssh ${USER}@${SERVER} "
        cd ${REMOTE_PATH}
        if [ -d 'UNEGario_old' ]; then
            mv UNEGario UNEGario_failed
            mv UNEGario_old UNEGario
            log '🔄 Rollback completado'
        fi
    "
    exit 1
fi

# Verificar archivos específicos
ssh ${USER}@${SERVER} "
    cd ${REMOTE_PATH}/UNEGario
    if curl -s localhost/UNEGario/UNEGario.html | grep -q 'subjects-calendar-container'; then
        log '✅ Funcionalidad de botones individuales verificada'
    else
        log '⚠️  Advertencia: No se detectaron los botones individuales'
    fi
"

# Paso 8: Limpieza
log "🧹 Limpiando archivos temporales..."
ssh ${USER}@${SERVER} "
    rm -rf UNEGario_old 2>/dev/null || true
    log '✅ Limpieza completada'
"

# Paso 9: Verificación final
log "🏁 Ejecutando verificación final..."
if curl -s https://edbetosolutions.tech/UNEGario | grep -q "Botones Individuales"; then
    log "✅ Deployment completado exitosamente"
    log "🌐 URL: https://edbetosolutions.tech/UNEGario"
    log "📅 Fecha: $(date)"
    log "📦 Backup disponible: UNEGario_backup_${DATE}.tar.gz"
else
    log "⚠️  Deployment completado pero verificación de contenido falló"
fi

echo ""
echo "🎉 ¡Deployment de UNEGario completado!"
echo "   URL: https://edbetosolutions.tech/UNEGario"
echo "   Backup: UNEGario_backup_${DATE}.tar.gz"
echo ""
