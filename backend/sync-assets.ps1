<#
Script: sync-assets.ps1
Propósito: Copiar archivos estáticos necesarios desde el frontend `micveahc` a la carpeta de documentación `deploy/docs/assets`.
#>

Param()

$source = "..\..\src\frontend\micveahc\assets"
$dest = "assets"

if (-not (Test-Path $dest)) {
    New-Item -ItemType Directory -Path $dest | Out-Null
}

$files = @("profile-photo.jpg","cv-edson-herrera.pdf")

foreach ($f in $files) {
    $srcPath = Join-Path $source $f
    if (Test-Path $srcPath) {
        Copy-Item -Path $srcPath -Destination $dest -Force
        Write-Host "Copiado: $f"
    } else {
        Write-Host "No se encontró: $srcPath" -ForegroundColor Yellow
    }
}

Write-Host "Sincronización completada. Archivos en $(Resolve-Path $dest)"
