# ⚡ COPIA Y PEGA - Backend Listo

## 📋 Archivos a Copiar

Copia toda esta carpeta `backend-production/` a tu repositorio edbetosolutions.

### Estructura final en edbetosolutions:
```
edbetosolutions/
├── src/backend/          ← COPIAR
├── deploy/               ← COPIAR  
├── nginx-production.conf ← COPIAR
├── install-backend.sh    ← COPIAR
└── README-BACKEND.md     ← COPIAR
```

## 🚀 Instalación Rápida

1. **Copia estos archivos** al repositorio edbetosolutions
2. **En el servidor**, ejecuta:
   ```bash
   chmod +x install-backend.sh
   sudo ./install-backend.sh
   ```

## ✅ Listo!

El script automáticamente:
- ✅ Instala el backend en `/opt/edbeto-backend`
- ✅ Configura el servicio systemd
- ✅ Actualiza nginx con proxy API
- ✅ Inicia todos los servicios
- ✅ Configura permisos correctos

## 🌐 Endpoints Disponibles

Después de la instalación:
- `https://edbetosolutions.tech/api/weather/benito-juarez`
- `https://edbetosolutions.tech/api/timeseries/coyoacan`  
- `https://edbetosolutions.tech/api/unegario/calendar`
- `https://edbetosolutions.tech/api/status`

## 📞 Si hay problemas:
```bash
sudo systemctl status conagua-api
sudo journalctl -u conagua-api -f
sudo nginx -t
```
