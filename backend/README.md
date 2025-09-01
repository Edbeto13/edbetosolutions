# Backend - EdbETO Solutions

Sistema backend para el portfolio de aplicaciones web de EdbETO Solutions. Proporciona APIs y servicios para las aplicaciones frontend.

## 🚀 Aplicaciones Soportadas

### 🌤️ Sistema Meteorológico CDMX
- **Archivo:** `api_server.py`
- **Descripción:** API para datos meteorológicos de la Ciudad de México
- **Fuente:** Servicio Meteorológico Nacional (Conagua)
- **Actualización:** Cada 75 minutos

### 🌡️ Recolector de Datos Conagua
- **Archivo:** `conagua_collector.py`
- **Descripción:** Recolector de datos meteorológicos en tiempo real
- **Funcionalidad:** Obtiene y procesa datos de estaciones meteorológicas
- **Almacenamiento:** Cache local con actualización automática

### 🔧 Construcción de UNEGario
- **Archivo:** `build_unegario.py`
- **Descripción:** Constructor y configurador para la aplicación UNEGario
- **Funcionalidad:** Procesamiento de horarios académicos

### 📊 Series Temporales Conagua
- **Archivo:** `conagua_timeseries.py`
- **Descripción:** Análisis de series temporales de datos meteorológicos
- **Funcionalidad:** Procesamiento estadístico y tendencias

### 📅 Integración Google Calendar
- **Archivo:** `UNEGario_GoogleCalendar.py`
- **Descripción:** Integración con Google Calendar para UNEGario
- **Funcionalidad:** Sincronización de horarios académicos

### 🧪 Testing Conagua
- **Archivo:** `test_conagua.py`
- **Descripción:** Tests para verificar la API de Conagua
- **Funcionalidad:** Validación de datos y endpoints

## 📁 Estructura del Backend

```
backend/
├── api_server.py              # Servidor API principal (22KB)
├── conagua_collector.py       # Recolector datos meteorológicos (22KB)
├── conagua_timeseries.py      # Análisis series temporales (18KB)
├── build_unegario.py          # Constructor UNEGario (5KB)
├── UNEGario_GoogleCalendar.py # Integración Google Calendar (3KB)
├── test_conagua.py            # Tests API Conagua (2KB)
├── weather_cache.json         # Cache de datos meteorológicos
├── requirements.txt           # Dependencias Python
├── config.py                  # Configuración centralizada
└── README.md                  # Esta documentación
```

## 🛠️ Instalación y Configuración

### 1. Instalar Dependencias

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno

Crear/editar archivo `.env` en la raíz del proyecto:

```env
# Configuración del Backend
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
DEBUG=True
LOG_LEVEL=INFO

# APIs Externas
WEATHER_API_TIMEOUT=30

# Google Calendar (para UNEGario)
GOOGLE_CREDENTIALS_PATH=./credentials.json

# Configuración CORS
CORS_ORIGINS=*
```

### 3. Ejecutar Servidor Principal

```bash
python api_server.py
```

El servidor estará disponible en: `http://localhost:8000`

## 🔌 Endpoints Disponibles

### API Meteorológica
- `GET /api/weather` - Datos meteorológicos actuales
- `GET /api/weather/cdmx` - Datos específicos de CDMX
- `GET /api/weather/forecast` - Pronóstico del tiempo

### API UNEGario
- `GET /api/unegario/schedule` - Horarios académicos
- `POST /api/unegario/calendar` - Sincronizar con Google Calendar

### Utilidades
- `GET /health` - Estado del servidor
- `GET /api/status` - Estado de APIs externas

## 📊 Fuentes de Datos

### Servicio Meteorológico Nacional (Conagua)
- **URL:** https://smn.conagua.gob.mx/
- **Tipo:** API REST
- **Frecuencia:** Actualización cada 75 minutos
- **Cobertura:** 16 alcaldías de CDMX

### Google Calendar API
- **Uso:** Sincronización de horarios académicos
- **Autenticación:** OAuth 2.0
- **Formato:** JSON

## 🧪 Testing

```bash
# Ejecutar tests de Conagua
python test_conagua.py

# Verificar estado de APIs
curl http://localhost:8000/health
```

## 📈 Monitoreo y Logs

- **Logs:** Configurables via `LOG_LEVEL` en `.env`
- **Cache:** `weather_cache.json` - actualizado automáticamente
- **Health Check:** Endpoint `/health` para monitoreo

## 🔧 Configuración Avanzada

### Timeout de APIs
Modificar en `config.py`:
```python
WEATHER_API_TIMEOUT = 30  # segundos
```

### Cache de Datos
El cache se actualiza automáticamente cada 75 minutos. Para forzar actualización:
```bash
rm weather_cache.json
```

## 🚀 Despliegue

### Desarrollo
```bash
python api_server.py
```

### Producción
```bash
FLASK_ENV=production python api_server.py
```

## 🤝 Contribución

1. Mantener la estructura de archivos existente
2. Actualizar `requirements.txt` si se agregan dependencias
3. Documentar nuevos endpoints en este README
4. Seguir las configuraciones en `config.py`

## 📝 Notas Técnicas

- **Puerto por defecto:** 8000
- **CORS:** Habilitado para desarrollo
- **Encoding:** UTF-8 para caracteres especiales
- **Timeout:** 30 segundos para APIs externas
- **Cache:** 75 minutos para datos meteorológicos

## 🔗 Enlaces Útiles

- [Documentación Conagua](https://smn.conagua.gob.mx/)
- [Google Calendar API](https://developers.google.com/calendar)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

**EdbETO Solutions** - Sistema Backend v1.0  
*Última actualización: Septiembre 2025*
