# 📚 UNEGario - Sistema Inteligente de Gestión de Horarios

UNEGario es un sistema web interactivo para visualizar y gestionar horarios universitarios con integración a Google Calendar.

## 🚀 Características

- **Visualización Interactiva**: Horario semanal con diseño responsive
- **Integración Google Calendar**: Botón para añadir todo el semestre a tu calendario
- **Datos Dinámicos**: Carga automática desde archivos JSON generados
- **Estadísticas**: Resumen de horas, materias y profesores
- **Diseño Moderno**: Interfaz atractiva con animaciones CSS
- **Días Festivos**: Manejo automático de días sin clases

## 📁 Estructura de Archivos

```
UNEGario/
├── UNEGario.html          # Página principal
├── unegario.js            # Lógica JavaScript
├── UNEGarioimages/        # Recursos gráficos
│   ├── UNEGLogo.png      # Logo de la universidad
│   └── UNEGarioICON.png  # Icono para la pestaña
└── output/                # Archivos generados (creados automáticamente)
    ├── horario_data.json  # Datos del horario en JSON
    └── google_calendar_url.txt # URL de Google Calendar
```

## 🛠️ Instalación y Configuración

### Prerrequisitos

1. **Python 3.10+** con las siguientes dependencias:
   ```bash
   pip install openpyxl>=3.0.0
   ```

2. **Navegador web moderno** con soporte para ES6+

### Configuración Inicial

1. **Clona o descarga** el proyecto
2. **Asegúrate** de que los archivos de datos JSON estén generados en la carpeta output

### Ejecutar con Datos Generados

Los archivos de datos necesarios son:
- `output/horario_data.json`
- `output/google_calendar_url.txt`

Estos archivos deben ser generados previamente por el backend.

### Ejecutar Localmente

1. **Inicia un servidor HTTP** local:
   ```bash
   cd src/frontend/UNEGario
   python -m http.server 8080
   ```

2. **Abre tu navegador** en: `http://localhost:8080/UNEGario.html`

## 🔧 Personalización

### Modificar el Horario

1. **Actualiza** los archivos JSON generados con los nuevos datos de tu horario
2. **Recarga** la página web para ver los cambios

### Cambiar Colores y Estilos

1. **Modifica** los colores en `UNEGario.html` (sección `<style>`)
2. **Actualiza** el mapeo en `unegario.js` (variable `materiaClases`)

### Añadir Nuevas Funcionalidades

El archivo `unegario.js` está bien documentado y modularizado para facilitar modificaciones.

## 🌐 Despliegue en Producción

### Para DigitalOcean/VPS

1. **Copia los archivos** al servidor:
   ```bash
   scp -r UNEGario/ root@tu-servidor:/var/www/html/
   scp -r output/ root@tu-servidor:/var/www/html/UNEGario/
   ```

2. **Configura nginx** (si es necesario) para servir archivos estáticos

3. **Verifica** que el sitio esté accesible

### Para GitHub Pages

1. **Coloca todos los archivos** en el directorio raíz del repositorio
2. **Configura GitHub Pages** en la configuración del repositorio
3. **Accede** a tu sitio en `https://usuario.github.io/repositorio`

## 📱 Funcionalidades Principales

### Carga Dinámica de Datos

```javascript
// Carga automática desde JSON generado
const horarioData = await loadHorarioData();
const calendarURL = await loadCalendarURL();
```

### Integración con Google Calendar

El botón "Añadir a Google Calendar" incluye:
- **Evento recurrente** semanal
- **Fechas de exclusión** para días festivos
- **Descripción completa** del horario
- **Zona horaria** configurada (America/Mexico_City)

### Estadísticas Automáticas

- Total de horas de clase
- Número de materias
- Cantidad de profesores
- Distribución de tiempo

## 🎨 Características de Diseño

- **Gradiente atractivo** en el fondo
- **Animaciones suaves** al cargar
- **Tarjetas de día** con colores distintivos
- **Responsive design** para móviles
- **Iconos emoji** para mejor UX

## 🐛 Solución de Problemas

### Error: "No se pueden cargar los datos"

1. **Verifica** que los archivos JSON existen en `output/`
2. **Asegúrate** de que los archivos JSON están actualizados
3. **Revisa** la consola del navegador para errores

### Error: "Imágenes no se muestran"

1. **Verifica** que las imágenes están en `UNEGarioimages/`
2. **Comprueba** las rutas relativas en el HTML
3. **Asegúrate** de que el servidor puede servir archivos estáticos

### Error: "URL de Calendar no funciona"

1. **Verifica** que el archivo `google_calendar_url.txt` existe
2. **Comprueba** que la URL está correctamente codificada
3. **Prueba** la URL en un navegador separado

## 📋 Lista de Verificación para Despliegue

- [ ] Archivos JSON generados y disponibles
- [ ] Imágenes en su lugar correcto
- [ ] Servidor HTTP configurado
- [ ] Rutas relativas verificadas
- [ ] Funcionalidad de Google Calendar probada
- [ ] Responsive design verificado
- [ ] Console sin errores JavaScript

## 🔮 Próximas Mejoras

- [ ] **Notificaciones push** para recordatorios de clase
- [ ] **Modo oscuro** toggle
- [ ] **Exportación a PDF** del horario
- [ ] **Integración con Outlook** Calendar
- [ ] **Widget para escritorio**
- [ ] **App móvil** con PWA

## 📞 Soporte

Para reportar bugs o solicitar features:
- **Email**: edbeto13@gmail.com
- **Website**: https://edbetosolutions.tech
- **GitHub**: Abre un issue en el repositorio

---

**Desarrollado con ❤️ por EdbETO Solutions Team**

*UNEGario v1.0.0 - Agosto 2025*
