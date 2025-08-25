# 🚀 Script de Deployment Seguro para UNEGario (PowerShell)
# Autor: EdbETO Solutions
# Fecha: 24 Agosto 2025

param(
    [switch]$DryRun = $false,
    [switch]$SkipBackup = $false,
    [string]$Server = "146.190.249.76",
    [string]$User = "root"
)

$ErrorActionPreference = "Stop"

# Configuración
$RemotePath = "/var/www/html"
$LocalPath = "src\frontend\UNEGario"
$BackupPath = "/root/backups"
$Date = Get-Date -Format "yyyyMMdd_HHmmss"

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $color = switch ($Level) {
        "ERROR" { "Red" }
        "WARNING" { "Yellow" }
        "SUCCESS" { "Green" }
        default { "White" }
    }
    Write-Host "[$timestamp] $Message" -ForegroundColor $color
}

function Test-Prerequisites {
    Write-Log "🔍 Verificando prerrequisitos..."
    
    # Verificar directorio local
    if (-not (Test-Path $LocalPath)) {
        Write-Log "❌ Error: Directorio local $LocalPath no encontrado" "ERROR"
        exit 1
    }
    
    # Verificar archivos críticos
    $criticalFiles = @("UNEGario.html", "unegario.js", "UNEGarioimages")
    foreach ($file in $criticalFiles) {
        if (-not (Test-Path (Join-Path $LocalPath $file))) {
            Write-Log "❌ Error: Archivo crítico $file no encontrado" "ERROR"
            exit 1
        }
    }
    
    # Verificar conectividad
    try {
        $null = ssh "$User@$Server" "echo 'test'" 2>$null
        Write-Log "✅ Conectividad al servidor verificada" "SUCCESS"
    } catch {
        Write-Log "❌ Error: No se puede conectar al servidor $Server" "ERROR"
        exit 1
    }
    
    # Verificar sitio web
    try {
        $response = Invoke-WebRequest -Uri "https://edbetosolutions.tech/UNEGario" -UseBasicParsing -TimeoutSec 10
        if ($response.StatusCode -eq 200) {
            Write-Log "✅ Sitio web responde correctamente" "SUCCESS"
        }
    } catch {
        Write-Log "⚠️  Advertencia: El sitio no responde correctamente" "WARNING"
    }
}

function New-Backup {
    if ($SkipBackup) {
        Write-Log "⏭️  Saltando creación de backup" "WARNING"
        return
    }
    
    Write-Log "💾 Creando backup de la versión actual..."
    
    $backupCommand = @"
mkdir -p $BackupPath
cd $RemotePath
if [ -d 'UNEGario' ]; then
    tar -czf $BackupPath/UNEGario_backup_$Date.tar.gz UNEGario/
    echo '✅ Backup creado: UNEGario_backup_$Date.tar.gz'
else
    echo '⚠️  No existe versión anterior para backup'
fi
"@
    
    ssh "$User@$Server" $backupCommand
}

function Deploy-Files {
    Write-Log "📤 Subiendo archivos al servidor..."
    
    if ($DryRun) {
        Write-Log "🔍 DRY RUN: Simulando upload de archivos" "WARNING"
        return
    }
    
    # Subir archivos
    scp -r $LocalPath "$User@${Server}:/tmp/UNEGario_new"
    
    # Verificar upload
    $verifyCommand = @"
if [ ! -d '/tmp/UNEGario_new' ]; then
    echo 'ERROR: Los archivos no se subieron correctamente'
    exit 1
fi

for file in 'UNEGario.html' 'unegario.js' 'UNEGarioimages'; do
    if [ ! -e "/tmp/UNEGario_new/`$file" ]; then
        echo "ERROR: Archivo crítico `$file no encontrado"
        exit 1
    fi
done

echo '✅ Todos los archivos críticos verificados'
"@
    
    $result = ssh "$User@$Server" $verifyCommand
    Write-Log $result
}

function Set-Permissions {
    Write-Log "🔐 Configurando permisos..."
    
    if ($DryRun) {
        Write-Log "🔍 DRY RUN: Simulando configuración de permisos" "WARNING"
        return
    }
    
    $permissionCommand = @"
chown -R www-data:www-data /tmp/UNEGario_new/
chmod -R 755 /tmp/UNEGario_new/
echo '✅ Permisos configurados'
"@
    
    ssh "$User@$Server" $permissionCommand
}

function Invoke-AtomicDeployment {
    Write-Log "⚡ Ejecutando deployment atómico..."
    
    if ($DryRun) {
        Write-Log "🔍 DRY RUN: Simulando deployment atómico" "WARNING"
        return
    }
    
    $deployCommand = @"
cd $RemotePath

if [ -d 'UNEGario' ]; then
    mv UNEGario UNEGario_old
fi

mv /tmp/UNEGario_new UNEGario
echo '✅ Deployment atómico completado'
"@
    
    ssh "$User@$Server" $deployCommand
}

function Test-Deployment {
    Write-Log "🔍 Verificando deployment..."
    
    Start-Sleep -Seconds 3
    
    # Verificar respuesta HTTP
    try {
        $response = Invoke-WebRequest -Uri "https://edbetosolutions.tech/UNEGario" -UseBasicParsing -TimeoutSec 15
        if ($response.StatusCode -eq 200) {
            Write-Log "✅ Sitio web responde correctamente" "SUCCESS"
        }
    } catch {
        Write-Log "❌ Error: El sitio no responde. Iniciando rollback..." "ERROR"
        Invoke-Rollback
        exit 1
    }
    
    # Verificar contenido específico
    $contentCheck = @"
cd $RemotePath/UNEGario
if curl -s localhost/UNEGario/UNEGario.html | grep -q 'subjects-calendar-container'; then
    echo '✅ Funcionalidad de botones individuales verificada'
else
    echo '⚠️  Advertencia: No se detectaron los botones individuales'
fi
"@
    
    $result = ssh "$User@$Server" $contentCheck
    Write-Log $result
}

function Invoke-Rollback {
    Write-Log "🔄 Ejecutando rollback..." "WARNING"
    
    $rollbackCommand = @"
cd $RemotePath
if [ -d 'UNEGario_old' ]; then
    mv UNEGario UNEGario_failed
    mv UNEGario_old UNEGario
    echo '🔄 Rollback completado'
else
    echo '❌ No hay versión anterior para rollback'
fi
"@
    
    ssh "$User@$Server" $rollbackCommand
}

function Remove-TempFiles {
    Write-Log "🧹 Limpiando archivos temporales..."
    
    if ($DryRun) {
        Write-Log "🔍 DRY RUN: Simulando limpieza" "WARNING"
        return
    }
    
    $cleanupCommand = @"
rm -rf UNEGario_old 2>/dev/null || true
rm -rf /tmp/UNEGario_new 2>/dev/null || true
echo '✅ Limpieza completada'
"@
    
    ssh "$User@$Server" $cleanupCommand
}

function Show-Summary {
    Write-Log "🏁 Resumen del deployment:" "SUCCESS"
    Write-Host ""
    Write-Host "🌐 URL: https://edbetosolutions.tech/UNEGario" -ForegroundColor Green
    Write-Host "📅 Fecha: $(Get-Date)" -ForegroundColor Green
    Write-Host "📦 Backup: UNEGario_backup_$Date.tar.gz" -ForegroundColor Green
    Write-Host "🎉 ¡Deployment completado exitosamente!" -ForegroundColor Green
    Write-Host ""
}

# Ejecución principal
try {
    Write-Log "🚀 Iniciando deployment de UNEGario..."
    
    if ($DryRun) {
        Write-Log "🔍 MODO DRY RUN - No se realizarán cambios reales" "WARNING"
    }
    
    Test-Prerequisites
    New-Backup
    Deploy-Files
    Set-Permissions
    Invoke-AtomicDeployment
    Test-Deployment
    Remove-TempFiles
    Show-Summary
    
} catch {
    Write-Log "❌ Error durante el deployment: $_" "ERROR"
    Write-Log "🔄 Considerando rollback..." "WARNING"
    Invoke-Rollback
    exit 1
}
