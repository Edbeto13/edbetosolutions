#!/bin/bash

# Script de limpieza para preparar deployment
# Uso: ./cleanup-for-deployment.sh

echo "🧹 Limpiando archivos para deployment..."

# Eliminar archivos de desarrollo
rm -rf __pycache__/
rm -rf .pytest_cache/
rm -rf node_modules/
rm -rf .vscode/
rm -f *.pyc
rm -f .DS_Store

# Eliminar logs de desarrollo
rm -f *.log
rm -f debug.log

# Crear .gitignore si no existe
if [ ! -f .gitignore ]; then
    cat > .gitignore << EOF
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.log
.env.local
.vscode/
.DS_Store
node_modules/
.pytest_cache/
*.swp
*.swo
*~
EOF
fi

echo "✅ Limpieza completada"
echo "📦 Archivos listos para deployment a 146.190.249.76"
echo ""
echo "Para desplegar ejecuta:"
echo "   ./deploy-to-droplet.ps1"
echo "   o"
echo "   ./deploy.ps1"
