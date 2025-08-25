# 🚀 Backend de Producción - EdbETO Solutions

Este directorio contiene todo el backend listo para copiar al repositorio de producción.

## 📁 Estructura

```
backend-production/
├── src/
│   └── backend/          # Código del servidor API
│       ├── api_server.py           # Servidor principal
│       ├── conagua_collector.py    # Recolector meteorológico
│       ├── conagua_timeseries.py   # Series de tiempo
│       ├── requirements.txt        # Dependencias Python
│       ├── UNEGario_GoogleCalendar.py  # Integración Google Calendar
│       ├── build_unegario.py       # Constructor UNEGario
│       ├── test_conagua.py         # Tests
│       └── weather_cache.json      # Cache de datos
├── deploy/               # Configuraciones de despliegue
│   ├── conagua-api.service        # Servicio systemd
│   └── nginx-hydredelback.conf    # Configuración nginx
├── nginx-production.conf # Configuración nginx para producción
└── README-BACKEND.md     # Este archivo
```

## 🔧 Instalación en Producción

### 1. Copiar archivos
```bash
# Copiar toda la carpeta src/ al repositorio de producción
# Copiar deploy/ al repositorio de producción
# Copiar nginx-production.conf como nginx.conf
```

### 2. Instalar dependencias
```bash
cd src/backend
pip install -r requirements.txt
```

### 3. Configurar servicio
```bash
# Copiar deploy/conagua-api.service a /etc/systemd/system/
sudo systemctl enable conagua-api
sudo systemctl start conagua-api
```

### 4. Configurar nginx
```bash
# Usar nginx-production.conf como base
# Actualizar configuración para incluir proxy al backend
sudo systemctl reload nginx
```

## 🌐 Endpoints API

- `/api/weather/:alcaldia` - Datos meteorológicos por alcaldía
- `/api/timeseries/:alcaldia` - Series temporales
- `/api/unegario/calendar` - Datos de Google Calendar
- `/api/status` - Estado del servidor

## 📊 Componentes

### API Server (api_server.py)
- Servidor HTTP en puerto 8000
- Endpoints RESTful para datos meteorológicos
- Integración con Conagua
- Cache de datos para performance

### Conagua Collector (conagua_collector.py)
- Recolección automática de datos meteorológicos
- API de Conagua integrada
- Sistema de cache inteligente
- Manejo de errores robusto

### UNEGario Backend (UNEGario_GoogleCalendar.py)
- Integración con Google Calendar API
- Procesamiento de horarios académicos
- Generación de datos estructurados

## 🔒 Seguridad

- CORS configurado para edbetosolutions.tech
- Rate limiting implementado
- Validación de inputs
- Logs de seguridad

## 🚀 Producción

El backend está optimizado para:
- ✅ Alto rendimiento
- ✅ Escalabilidad
- ✅ Monitoreo
- ✅ Logs estructurados
- ✅ Cache inteligente
- ✅ Recuperación automática

## 📝 Notas

- Todos los archivos están listos para producción
- Las configuraciones están optimizadas para el servidor
- Los logs se almacenan en `/var/log/conagua-api/`
- El servicio se reinicia automáticamente en caso de fallo
