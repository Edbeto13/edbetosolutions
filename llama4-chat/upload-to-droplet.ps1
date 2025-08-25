# Script para subir archivos a droplet usando VS Code Remote SSH
Write-Host "🚀 Subiendo Llama4 Chat al Droplet usando VS Code Extensions" -ForegroundColor Green

$DropletIP = "146.190.249.76"
$CleanDir = "$env:TEMP\llama4-chat-clean"

Write-Host "📋 Pasos para deployment con VS Code:" -ForegroundColor Cyan

Write-Host "`n1. 🔧 Configurar conexión SSH:" -ForegroundColor Yellow
Write-Host "   - Abre el Remote Explorer (Ctrl+Shift+P -> 'Remote-SSH: Connect to Host')" -ForegroundColor White
Write-Host "   - Añade nuevo host: root@146.190.249.76" -ForegroundColor Gray
Write-Host "   - O usa la configuración creada: 'edbeto-droplet'" -ForegroundColor Gray

Write-Host "`n2. 📁 Conectar al droplet:" -ForegroundColor Yellow
Write-Host "   - Conecta a: edbeto-droplet" -ForegroundColor White
Write-Host "   - Abre la carpeta: /var/www/" -ForegroundColor Gray
Write-Host "   - Crea directorio: llama4-chat (si no existe)" -ForegroundColor Gray

Write-Host "`n3. 📤 Subir archivos:" -ForegroundColor Yellow
Write-Host "   Opción A - Drag & Drop:" -ForegroundColor White
Write-Host "   - Arrastra archivos desde: $CleanDir" -ForegroundColor Gray
Write-Host "   - Suelta en: /var/www/llama4-chat/" -ForegroundColor Gray
Write-Host "`n   Opción B - SFTP Extension:" -ForegroundColor White
Write-Host "   - Usa Ctrl+Shift+P -> 'SFTP: Upload Folder'" -ForegroundColor Gray
Write-Host "   - Selecciona: $CleanDir" -ForegroundColor Gray

Write-Host "`n4. 🚀 Ejecutar deployment:" -ForegroundColor Yellow
Write-Host "   - Abre terminal en VS Code (conectado al droplet)" -ForegroundColor White
Write-Host "   - Ejecuta: cd /var/www/llama4-chat" -ForegroundColor Gray
Write-Host "   - Ejecuta: chmod +x deploy.sh" -ForegroundColor Gray
Write-Host "   - Ejecuta: sudo ./deploy.sh" -ForegroundColor Gray

Write-Host "`n📁 Archivos preparados en: $CleanDir" -ForegroundColor Green
Write-Host "🌐 URL final: http://146.190.249.76:8000" -ForegroundColor Green

Write-Host "`n🔑 Si necesitas autenticación SSH:" -ForegroundColor Cyan
Write-Host "   - Configura clave SSH en: ~/.ssh/id_rsa" -ForegroundColor White
Write-Host "   - O usa autenticación por contraseña" -ForegroundColor White

# Abrir VS Code con Remote Explorer
Write-Host "`n⚡ Abriendo Remote Explorer..." -ForegroundColor Yellow
