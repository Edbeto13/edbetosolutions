# Deploy script for Llama4 Chat on droplet
# Usage: .\deploy.ps1

param(
    [string]$ServerIP = "",
    [string]$Username = "root"
)

Write-Host "🚀 Iniciando deployment de Llama4 Chat..." -ForegroundColor Green

if (-not $ServerIP) {
    $ServerIP = Read-Host "Ingresa la IP del droplet"
}

# Configuración
$LocalPath = "C:\edbetosolutions\llama4-chat"
$RemotePath = "/var/www/llama4-chat"
$ServiceName = "llama4-chat"

# Archivos a copiar (excluir archivos de desarrollo)
$FilesToCopy = @(
    "app.py",
    "requirements.txt",
    "deploy.sh",
    "src/",
    "config/",
    "templates/",
    "static/"
)

Write-Host "📦 Preparando archivos para deployment..." -ForegroundColor Yellow

# Crear directorio temporal limpio
$TempDir = "$env:TEMP\llama4-chat-deploy"
if (Test-Path $TempDir) {
    Remove-Item $TempDir -Recurse -Force
}
New-Item -ItemType Directory -Path $TempDir -Force | Out-Null

# Copiar archivos necesarios
foreach ($file in $FilesToCopy) {
    $SourcePath = Join-Path $LocalPath $file
    $DestPath = Join-Path $TempDir $file
    
    if (Test-Path $SourcePath) {
        if (Test-Path $SourcePath -PathType Container) {
            # Es un directorio
            Copy-Item $SourcePath $DestPath -Recurse -Force
            Write-Host "✅ Copiado directorio: $file" -ForegroundColor Green
        } else {
            # Es un archivo
            $DestDir = Split-Path $DestPath -Parent
            if (-not (Test-Path $DestDir)) {
                New-Item -ItemType Directory -Path $DestDir -Force | Out-Null
            }
            Copy-Item $SourcePath $DestPath -Force
            Write-Host "✅ Copiado archivo: $file" -ForegroundColor Green
        }
    } else {
        Write-Host "⚠️  No encontrado: $file" -ForegroundColor Yellow
    }
}

# Crear archivo .env para producción
$EnvContent = @"
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
"@

$EnvContent | Out-File -FilePath "$TempDir\.env" -Encoding UTF8
Write-Host "✅ Archivo .env creado para producción" -ForegroundColor Green

Write-Host "`n📡 Instrucciones para deployment manual:" -ForegroundColor Cyan
Write-Host "1. Sube los archivos del directorio temporal al servidor:" -ForegroundColor White
Write-Host "   scp -r $TempDir/* $Username@$ServerIP`:$RemotePath" -ForegroundColor Gray
Write-Host "`n2. Conéctate al servidor y ejecuta el script de deployment:" -ForegroundColor White
Write-Host "   ssh $Username@$ServerIP" -ForegroundColor Gray
Write-Host "   cd $RemotePath" -ForegroundColor Gray
Write-Host "   chmod +x deploy.sh" -ForegroundColor Gray
Write-Host "   sudo ./deploy.sh" -ForegroundColor Gray

Write-Host "`n3. Configurar DNS (opcional):" -ForegroundColor White
Write-Host "   - Apunta llama4.edbetosolutions.com a la IP: $ServerIP" -ForegroundColor Gray

Write-Host "`n📁 Archivos preparados en: $TempDir" -ForegroundColor Green
Write-Host "🎯 La aplicación estará disponible en: http://$ServerIP o http://llama4.edbetosolutions.com" -ForegroundColor Green

# Abrir el directorio temporal
if ($env:OS -eq "Windows_NT") {
    Start-Process "explorer.exe" -ArgumentList $TempDir
}
