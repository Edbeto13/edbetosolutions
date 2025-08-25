# Script de configuración y despliegue - Sistema Conagua CDMX
# Author: EdbETO Solutions Team
# Repositorio: https://github.com/Edbeto13/Hydredelback
# Licencia: MIT

param(
    [Parameter(Position=0)]
    [ValidateSet('start', 'stop', 'restart', 'status', 'test', 'install')]
    [string]$Action = 'status',
    
    [switch]$Silent,
    [switch]$NoCache,
    [int]$Port = 8000
)

# Configuración
$ProjectRoot = "C:\HydredPageSolution\Hydredelback"
$BackendPath = "$ProjectRoot\src\backend"
$CacheFile = "$BackendPath\weather_cache.json"

# Funciones de utilidad
function Write-Status {
    param([string]$Message, [string]$Type = "INFO")
    if (-not $Silent) {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        switch ($Type) {
            "SUCCESS" { Write-Host "[$timestamp] ✅ $Message" -ForegroundColor Green }
            "ERROR"   { Write-Host "[$timestamp] ❌ $Message" -ForegroundColor Red }
            "WARNING" { Write-Host "[$timestamp] ⚠️ $Message" -ForegroundColor Yellow }
            "INFO"    { Write-Host "[$timestamp] 📋 $Message" -ForegroundColor Cyan }
            "DEBUG"   { Write-Host "[$timestamp] 🔍 $Message" -ForegroundColor DarkGray }
        }
    }
}

function Test-Dependencies {
    Write-Status "Verificando dependencias del sistema..." "INFO"
    
    # Verificar Python
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Status "Python encontrado: $pythonVersion" "SUCCESS"
        } else {
            Write-Status "Python no encontrado - Instalando..." "WARNING"
            return $false
        }
    } catch {
        Write-Status "Error verificando Python: $_" "ERROR"
        return $false
    }
    
    # Verificar archivos del proyecto
    $requiredFiles = @(
        "$BackendPath\conagua_collector.py",
        "$BackendPath\api_server.py"
    )
    
    foreach ($file in $requiredFiles) {
        if (Test-Path $file) {
            Write-Status "Archivo encontrado: $(Split-Path $file -Leaf)" "SUCCESS"
        } else {
            Write-Status "Archivo faltante: $file" "ERROR"
            return $false
        }
    }
    
    return $true
}

function Start-ConaguaSystem {
    Write-Status "🚀 INICIANDO SISTEMA CONAGUA CDMX" "INFO"
    
    if (-not (Test-Dependencies)) {
    Write-Status "Dependencias no encontradas. Ejecuta: .\scripts\setup-conagua.ps1 install" "ERROR"
        return
    }
    
    # Cambiar al directorio backend
    Push-Location $BackendPath
    
    try {
        # Limpiar caché si se solicita
        if ($NoCache -and (Test-Path $CacheFile)) {
            Remove-Item $CacheFile -Force
            Write-Status "Caché limpiado" "INFO"
        }
        
        # Verificar puerto
        $portInUse = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
        if ($portInUse) {
            Write-Status "Puerto $Port en uso. Intentando detener proceso anterior..." "WARNING"
            Stop-ConaguaSystem
            Start-Sleep -Seconds 2
        }
        
        Write-Status "Iniciando servidor en puerto $Port..." "INFO"
        Write-Status "🌐 URL: http://localhost:$Port" "SUCCESS"
        Write-Status "📡 API: http://localhost:$Port/api/" "SUCCESS"
        Write-Status "🌤️ Weather: http://localhost:$Port/api/weather" "SUCCESS"
        
        # Iniciar servidor
        python api_server.py --port $Port
        
    } finally {
        Pop-Location
    }
}

function Stop-ConaguaSystem {
    Write-Status "🛑 DETENIENDO SISTEMA CONAGUA" "INFO"
    
    # Buscar procesos Python ejecutando nuestro servidor
    $processes = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
        $_.ProcessName -eq "python" -and 
        (Get-WmiObject Win32_Process -Filter "ProcessId = $($_.Id)").CommandLine -like "*api_server.py*"
    }
    
    if ($processes) {
        foreach ($proc in $processes) {
            Write-Status "Deteniendo proceso Python (PID: $($proc.Id))" "INFO"
            $proc.Kill()
        }
        Write-Status "Servidor detenido" "SUCCESS"
    } else {
        Write-Status "No se encontraron procesos del servidor" "INFO"
    }
    
    # Limpiar puertos si es necesario
    $portInUse = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
    if ($portInUse) {
        Write-Status "Puerto $Port liberado" "SUCCESS"
    }
}

function Get-SystemStatus {
    Write-Status "📊 ESTADO DEL SISTEMA CONAGUA" "INFO"
    Write-Status ("=" * 50) "INFO"
    
    # Verificar archivos
    Write-Status "📁 Archivos del proyecto:" "INFO"
    if (Test-Path "$BackendPath\conagua_collector.py") {
        $collectorSize = (Get-Item "$BackendPath\conagua_collector.py").Length
        Write-Status "   conagua_collector.py: $collectorSize bytes ✅" "SUCCESS"
    } else {
        Write-Status "   conagua_collector.py: FALTANTE ❌" "ERROR"
    }
    
    if (Test-Path "$BackendPath\api_server.py") {
        $apiSize = (Get-Item "$BackendPath\api_server.py").Length
        Write-Status "   api_server.py: $apiSize bytes ✅" "SUCCESS"
    } else {
        Write-Status "   api_server.py: FALTANTE ❌" "ERROR"
    }
    
    # Verificar caché
    Write-Status "💾 Estado del caché:" "INFO"
    if (Test-Path $CacheFile) {
        $cacheSize = (Get-Item $CacheFile).Length
        $cacheTime = (Get-Item $CacheFile).LastWriteTime
        Write-Status "   Archivo: weather_cache.json (${cacheSize} bytes)" "SUCCESS"
        Write-Status "   Última modificación: $cacheTime" "INFO"
        
        try {
            $cacheContent = Get-Content $CacheFile | ConvertFrom-Json
            $alcaldias = $cacheContent.data.PSObject.Properties.Name.Count
            Write-Status "   Alcaldías en caché: $alcaldias/16" "INFO"
        } catch {
            Write-Status "   Error leyendo caché: $_" "WARNING"
        }
    } else {
        Write-Status "   No existe caché - Sistema sin inicializar" "WARNING"
    }
    
    # Verificar procesos
    Write-Status "🔄 Procesos activos:" "INFO"
    $pythonProcs = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
        (Get-WmiObject Win32_Process -Filter "ProcessId = $($_.Id)").CommandLine -like "*api_server.py*"
    }
    
    if ($pythonProcs) {
        foreach ($proc in $pythonProcs) {
            Write-Status "   Servidor Python (PID: $($proc.Id)) - Activo ✅" "SUCCESS"
        }
    } else {
        Write-Status "   No hay servidores ejecutándose" "INFO"
    }
    
    # Verificar puertos
    Write-Status "🌐 Estado de puertos:" "INFO"
    $portConnection = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
    if ($portConnection) {
        Write-Status "   Puerto ${Port}: EN USO (Estado: $($portConnection.State))" "SUCCESS"
    } else {
        Write-Status "   Puerto ${Port}: DISPONIBLE" "INFO"
    }
    
    # Información del sistema
    Write-Status "🖥️ Información del sistema:" "INFO"
    $pythonVer = python --version 2>&1
    Write-Status "   Python: $pythonVer" "INFO"
    Write-Status "   PowerShell: $($PSVersionTable.PSVersion)" "INFO"
    Write-Status "   OS: $($env:OS)" "INFO"
    
    Write-Status ("=" * 50) "INFO"
}

function Test-ConaguaSystem {
    Write-Status "🧪 EJECUTANDO PRUEBAS DEL SISTEMA" "INFO"
    
    Push-Location $BackendPath
    
    try {
        # Ejecutar script de pruebas
        python test_conagua.py
        
        if ($LASTEXITCODE -eq 0) {
            Write-Status "Todas las pruebas completadas exitosamente" "SUCCESS"
        } else {
            Write-Status "Algunas pruebas fallaron (código: $LASTEXITCODE)" "WARNING"
        }
    } catch {
        Write-Status "Error ejecutando pruebas: $_" "ERROR"
    } finally {
        Pop-Location
    }
}

function Install-ConaguaSystem {
    Write-Status "📦 INSTALANDO SISTEMA CONAGUA" "INFO"
    
    # Verificar Python
    try {
        python --version | Out-Null
        Write-Status "Python ya instalado" "SUCCESS"
    } catch {
        Write-Status "Python no encontrado. Por favor instala Python 3.8+" "ERROR"
        Write-Status "Descarga desde: https://www.python.org/downloads/" "INFO"
        return
    }
    
    # Crear directorios si no existen
    $directories = @(
        $ProjectRoot,
        "$ProjectRoot\src",
        "$ProjectRoot\src\backend",
        "$ProjectRoot\docs",
        "$ProjectRoot\logs"
    )
    
    foreach ($dir in $directories) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force
            Write-Status "Directorio creado: $dir" "SUCCESS"
        }
    }
    
    # Verificar archivos principales
    $coreFiles = @(
        "$BackendPath\conagua_collector.py",
        "$BackendPath\api_server.py",
        "$BackendPath\test_conagua.py"
    )
    
    $missingFiles = @()
    foreach ($file in $coreFiles) {
        if (-not (Test-Path $file)) {
            $missingFiles += $file
        }
    }
    
    if ($missingFiles.Count -gt 0) {
        Write-Status "Archivos faltantes detectados:" "WARNING"
        foreach ($file in $missingFiles) {
            Write-Status "   - $(Split-Path $file -Leaf)" "ERROR"
        }
        Write-Status "Por favor verifica que todos los archivos estén en su lugar" "INFO"
        return
    }
    
    Write-Status "✅ Sistema Conagua instalado y verificado" "SUCCESS"
    Write-Status "Ejecuta: .\scripts\setup-conagua.ps1 start para iniciar el servidor" "INFO"
}

# Función principal
function Main {
    Write-Host ""
    Write-Host "🌤️ SISTEMA CONAGUA CDMX - EdbETO Solutions" -ForegroundColor Yellow
    Write-Host "=" * 60 -ForegroundColor DarkGray
    Write-Host "Repositorio: https://github.com/Edbeto13/Hydredelback" -ForegroundColor DarkGray
    Write-Host "Autor: EdbETO Solutions Team" -ForegroundColor DarkGray
    Write-Host "=" * 60 -ForegroundColor DarkGray
    Write-Host ""
    
    switch ($Action) {
        'start' {
            Start-ConaguaSystem
        }
        'stop' {
            Stop-ConaguaSystem
        }
        'restart' {
            Stop-ConaguaSystem
            Start-Sleep -Seconds 3
            Start-ConaguaSystem
        }
        'status' {
            Get-SystemStatus
        }
        'test' {
            Test-ConaguaSystem
        }
        'install' {
            Install-ConaguaSystem
        }
        default {
            Write-Status "Acción no reconocida: $Action" "ERROR"
            Write-Host ""
            Write-Host "Uso: .\scripts\setup-conagua.ps1 [start|stop|restart|status|test|install]" -ForegroundColor Yellow
            Write-Host ""
            Write-Host "Acciones disponibles:" -ForegroundColor White
            Write-Host "  start    - Iniciar el servidor Conagua" -ForegroundColor Green
            Write-Host "  stop     - Detener el servidor" -ForegroundColor Red
            Write-Host "  restart  - Reiniciar el servidor" -ForegroundColor Yellow
            Write-Host "  status   - Ver estado del sistema" -ForegroundColor Cyan
            Write-Host "  test     - Ejecutar pruebas" -ForegroundColor Magenta
            Write-Host "  install  - Verificar instalación" -ForegroundColor Blue
            Write-Host ""
            Write-Host "Opciones:" -ForegroundColor White
            Write-Host "  -Port     - Puerto del servidor (default: 8000)"
            Write-Host "  -NoCache  - Limpiar caché antes de iniciar"
            Write-Host "  -Silent   - Modo silencioso"
            Write-Host ""
            Write-Host "Ejemplos:" -ForegroundColor Yellow
            Write-Host "  .\scripts\setup-conagua.ps1 start"
            Write-Host "  .\scripts\setup-conagua.ps1 start -Port 3000"
            Write-Host "  .\scripts\setup-conagua.ps1 restart -NoCache"
            Write-Host ""
        }
    }
}

# Ejecutar función principal
Main
