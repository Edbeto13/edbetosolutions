#!/usr/bin/env bash
set -euo pipefail

# Desde la raíz del repo (edbetosolutions/)
mkdir -p data web/chatbot

# Si no existe, crea enlace simbólico para exponer los JSON en el sitio
if [ ! -e web/data ]; then
  ln -s ../data web/data
  echo "✓ Creado symlink web/data → ../data"
else
  echo "• web/data ya existe (ok)"
fi

echo "Listo. Sirve la carpeta 'web/' como root del sitio (Nginx, Caddy, etc.)."
