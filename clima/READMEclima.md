# 🌦️ Sistema Meteorológico CDMX - Frontend

Interfaz de usuario para la visualización de datos meteorológicos en tiempo real de las 16 alcaldías de la Ciudad de México.

## 📋 Características

- **Visualización en tiempo real** de condiciones meteorológicas por alcaldía
- **Mapas interactivos** con datos localizados
- **Gráficos de series temporales** para análisis de tendencias
- **Diseño responsive** para cualquier dispositivo
- **Interfaz moderna** con animaciones y efectos visuales

## 📁 Estructura de Archivos

```
clima/
├── clima-production.html    # Página principal de la aplicación
├── script-fixed.js          # Lógica JavaScript principal
├── styles-fixed.css         # Estilos CSS de la aplicación
├── components/              # Componentes reutilizables
│   └── ClimaCDMX.jsx        # Componente principal de visualización
└── scripts/                 # Scripts utilitarios
    └── setup-conagua.ps1    # Script de configuración para desarrollo
```

## 🚀 Instalación y Ejecución

### Para desarrollo local

1. **Configurar el backend**:
   - Asegúrate que el backend esté en funcionamiento en `http://localhost:8000`
   - Verifica que el endpoint `/api/weather` esté disponible

2. **Abrir el archivo HTML**:
   - Puedes abrir directamente `clima-production.html` en tu navegador
   - O utilizar un servidor HTTP local:
     ```bash
     python -m http.server 8080
     ```

3. **Actualizar la configuración** (si es necesario):
   - Editar `script-fixed.js` para ajustar la URL de la API:
     ```javascript
     API_BASE_URL: '/api' // Cambiar según sea necesario
     ```

## 🔧 Personalización

### Cambiar estilos

Edita `styles-fixed.css` para personalizar:
- Colores y temas
- Tamaños y márgenes
- Animaciones y transiciones

### Añadir nuevas funcionalidades

El archivo `script-fixed.js` está organizado por secciones para facilitar modificaciones:
- Configuración global
- Funciones de comunicación con la API
- Procesamiento de datos
- Renderizado de interfaz

## 📱 Funcionalidades Específicas

### Mapa Interactivo

- Selección de alcaldía por clic
- Información emergente con datos detallados
- Colores dinámicos según condiciones meteorológicas

### Gráficos de Series Temporales

- Visualización de datos históricos
- Opciones para diferentes períodos de tiempo
- Exportación de datos en formato CSV

### Panel de Estadísticas

- Resumen de condiciones actuales
- Comparativa entre alcaldías
- Alertas para condiciones extremas

## 🔎 Solución de Problemas

### Error: "No se pueden cargar los datos meteorológicos"

1. **Verifica** que el backend esté en funcionamiento
2. **Comprueba** la URL de la API en la configuración
3. **Revisa** la consola del navegador para errores detallados

### Error: "Gráficos no se visualizan correctamente"

1. **Actualiza** tu navegador a la versión más reciente
2. **Limpia** la caché del navegador
3. **Verifica** que JavaScript esté habilitado

## 📝 Notas para Desarrolladores

- La aplicación utiliza Fetch API para comunicarse con el backend
- Los gráficos se generan con la biblioteca Chart.js
- Compatible con navegadores modernos (Chrome, Firefox, Safari, Edge)
- Se recomienda usar herramientas de desarrollo del navegador para depuración

---

**Desarrollado por EdbETO Solutions Team**

*Sistema Meteorológico CDMX v2.0.0 - Agosto 2025*
