#!/bin/bash
# Script para ejecutar el servidor de Llama4 con NVIDIA NIM API
# Autor: EdbetoSolutions Team
# Fecha: Agosto 2025

# Directorio del script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Configuración
LOG_FILE="nvidia_server.log"
PID_FILE="nvidia_server.pid"

# Función para iniciar el servidor
start_server() {
    echo "🚀 Iniciando servidor NVIDIA NIM API..."
    
    # Verificar si existe la variable de entorno
    if [ -z "$NVIDIA_API_KEY" ]; then
        echo "⚠️ ADVERTENCIA: Variable de entorno NVIDIA_API_KEY no está configurada"
        echo "⚠️ Se usará la clave de fallback en el código (menos seguro)"
        echo "⚠️ Para mayor seguridad, configura la variable con:"
        echo "⚠️ export NVIDIA_API_KEY=\"tu-clave-aqui\""
        echo
    fi
    
    # Iniciar en background
    nohup python3 nvidia_api_server.py > $LOG_FILE 2>&1 &
    PID=$!
    echo $PID > $PID_FILE
    echo "✅ Servidor iniciado con PID: $PID"
    echo "📝 Logs disponibles en: $LOG_FILE"
}

# Función para detener el servidor
stop_server() {
    if [ -f $PID_FILE ]; then
        PID=$(cat $PID_FILE)
        if ps -p $PID > /dev/null; then
            echo "🛑 Deteniendo servidor (PID: $PID)..."
            kill $PID
            rm $PID_FILE
            echo "✅ Servidor detenido"
        else
            echo "⚠️ El servidor no está en ejecución (PID: $PID no encontrado)"
            rm $PID_FILE
        fi
    else
        echo "⚠️ Archivo PID no encontrado, verificando procesos..."
        pkill -f "python3 nvidia_api_server.py"
        echo "✅ Procesos detenidos"
    fi
}

# Función para ver el estado del servidor
status_server() {
    if [ -f $PID_FILE ]; then
        PID=$(cat $PID_FILE)
        if ps -p $PID > /dev/null; then
            echo "🟢 Servidor en ejecución (PID: $PID)"
            echo "📝 Logs en: $LOG_FILE"
            echo "🔍 Últimas 5 líneas del log:"
            tail -n 5 $LOG_FILE
        else
            echo "🔴 Servidor no está en ejecución (PID: $PID no encontrado)"
            rm $PID_FILE
        fi
    else
        echo "🔴 Servidor no está en ejecución (archivo PID no encontrado)"
    fi
}

# Función para ver los logs en tiempo real
view_logs() {
    if [ -f $LOG_FILE ]; then
        echo "📊 Mostrando logs en tiempo real (Ctrl+C para salir):"
        tail -f $LOG_FILE
    else
        echo "❌ Archivo de logs no encontrado: $LOG_FILE"
    fi
}

# Función para mostrar comandos curl de prueba
test_commands() {
    echo "🧪 Comandos de prueba:"
    echo "  curl -s http://localhost:8000/health | jq"
    echo "  curl -s http://localhost:8000/api/status | jq"
    echo "  curl -s http://localhost:8000/api/chat/status -i"
    echo ""
    echo "🔍 Prueba de mensaje al chat:"
    echo 'curl -X POST -H "Content-Type: application/json" -d '\''{"messages":[{"role":"user","content":"Hola, ¿cómo estás?"}]}'\'' http://localhost:8000/api/chat | jq'
}

# Mostrar ayuda
show_help() {
    echo "Uso: $0 [comando]"
    echo ""
    echo "Comandos:"
    echo "  start    - Iniciar el servidor NVIDIA NIM API"
    echo "  stop     - Detener el servidor"
    echo "  restart  - Reiniciar el servidor"
    echo "  status   - Ver estado del servidor"
    echo "  logs     - Ver logs en tiempo real"
    echo "  test     - Mostrar comandos de prueba"
    echo "  help     - Mostrar esta ayuda"
}

# Procesar comandos
case "$1" in
    start)
        start_server
        ;;
    stop)
        stop_server
        ;;
    restart)
        stop_server
        sleep 2
        start_server
        ;;
    status)
        status_server
        ;;
    logs)
        view_logs
        ;;
    test)
        test_commands
        ;;
    help|*)
        show_help
        ;;
esac

exit 0
