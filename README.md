# 🚀 EdBetoSolutions

[![Website](https://img.shields.io/website?url=https%3A%2F%2Fedbetosolutions.tech)](https://edbetosolutions.tech)
[![License](https://img.shields.io/github/license/Edbeto13/edbetosolutions)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/Edbeto13/edbetosolutions)](https://github.com/Edbeto13/edbetosolutions/commits/main)

> 🌐 **[edbetosolutions.tech](https://edbetosolutions.tech)** - Portafolio profesional de soluciones tecnológicas innovadoras

Colección de aplicaciones web interactivas y sistemas inteligentes desarrollados por **Edson Alberto Herrera Cervantes**, incluyendo sistemas meteorológicos, chatbots con IA, gestión universitaria y herramientas de productividad.

## 🌟 Aplicaciones Disponibles

| 🎯 **Aplicación** | � **URL** | 📝 **Descripción** |
|---|---|---|
| **Portafolio Principal** | [edbetosolutions.tech](https://edbetosolutions.tech) | Portal principal con todos los proyectos |
| **Sistema Meteorológico** | [edbetosolutions.tech/clima](https://edbetosolutions.tech/clima) | Pronósticos CDMX con modelos 3D |
| **Chat IA Llama 4** | [edbetosolutions.tech/llama4](https://edbetosolutions.tech/llama4) | Chatbot con NVIDIA NIM |
| **CV Interactivo** | [edbetosolutions.tech/micveahc](https://edbetosolutions.tech/micveahc) | Curriculum vitae web profesional |
| **UNEGario** | [edbetosolutions.tech/UNEGario](https://edbetosolutions.tech/UNEGario) | Sistema universitario con Google Calendar |

## ⚡ Tecnologías Principales

- **Frontend**: HTML5, CSS3, JavaScript ES6+, Three.js
- **Backend**: Python, Flask, NVIDIA NIM APIs  
- **Integración**: Google Calendar API, CONAGUA API
- **Infraestructura**: DigitalOcean, Nginx, SSL/HTTPS

## 📁 Estructura del Proyecto

```
edbetosolutions/
│
├── 🏠 SITIO WEB PRINCIPAL
│   ├── index.html                 # Redirección automática al portafolio
│   ├── package.json              # Configuración del proyecto
│   └── README.md                 # Este archivo
│
├── 🎨 FRONTEND APPLICATIONS
│   └── frontend/
│       ├── Portafolio/           # 🎯 Portal principal de proyectos (PÁGINA PRINCIPAL)
│       │   ├── index.html        # → Landing page completa del sitio
│       │   └── README.md         # → Documentación del portafolio
│       │
│       ├── clima/                # 🌦️ Sistema Meteorológico CDMX
│       │   ├── index.html        # → Interfaz principal
│       │   ├── clima-production.html # → Versión optimizada
│       │   ├── styles-fixed.css  # → Estilos
│       │   ├── script-fixed.js   # → Lógica JS
│       │   ├── READMEclima.md    # → Documentación
│       │   ├── 3Dclimagbl/       # → Modelos 3D meteorológicos
│       │   ├── components/       # → Componentes React
│       │   └── scripts/          # → Scripts de configuración
│       │
│       ├── llama4/               # 🦙 Chat con IA Llama 4
│       │   ├── index.html        # → Interfaz del chat
│       │   ├── chat.js           # → Lógica del chat
│       │   ├── styles.css        # → Estilos del chat
│       │   └── README.md         # → Documentación
│       │
│       ├── micveahc/             # 👨‍💼 CV Web Interactivo
│       │   ├── micveahc.html     # → CV principal
│       │   ├── micveahc.css      # → Estilos del CV
│       │   ├── micveahc.js       # → Interactividad
│       │   ├── READMEmicveahc.md # → Documentación
│       │   └── assets/           # → Recursos (CV PDF, fotos, etc.)
│       │
│       └── UNEGario/             # 📚 Sistema Universitario
│           ├── UNEGario.html     # → Interfaz principal
│           ├── unegario.js       # → Lógica del sistema
│           ├── READMEunegario.md # → Documentación
│           └── UNEGarioimages/   # → Recursos visuales
│
├── 📋 DOCUMENTACIÓN Y CONFIGURACIÓN
│   ├── .gitignore                # Archivos ignorados por Git
│   ├── .github/                  # Configuraciones de GitHub
│   ├── DEPLOYMENT.md             # Guía de despliegue
│   └── LICENSE                   # Licencia MIT
│
└── 🔧 BACKEND (Próximamente)
    └── backend/                  # APIs y servicios backend
        └── llama4/               # → API del chat con Llama 4
```

## 🌟 Proyectos Destacados

### 🌦️ Sistema Meteorológico CDMX
**Ubicación**: [`frontend/clima/`](frontend/clima/)
- **Funcionalidad**: Visualización en tiempo real del clima por alcaldías
- **Tecnologías**: HTML5, CSS3, JavaScript, CONAGUA API
- **Características**: Mapas interactivos, gráficos temporales, modelos 3D
- **Estado**: ✅ Funcional y optimizado

### 🦙 Chat con Llama 4 Maverick
**Frontend**: [`frontend/llama4/`](frontend/llama4/) | **Backend**: *Próximamente*
- **Funcionalidad**: Chat interactivo con IA avanzada
- **Tecnologías**: NVIDIA NIM Service, FastAPI, JavaScript
- **Características**: Conversaciones naturales, interfaz moderna
- **Estado**: 🔶 Frontend listo - Backend en desarrollo

### 👨‍💼 CV Web Interactivo
**Ubicación**: [`frontend/micveahc/`](frontend/micveahc/)
- **Funcionalidad**: Currículum vitae web profesional
- **Tecnologías**: HTML5, CSS3, JavaScript
- **Características**: Diseño responsivo, descarga PDF, animaciones
- **Estado**: ✅ Funcional y actualizado

### 📚 UNEGario - Sistema Universitario
**Ubicación**: [`frontend/UNEGario/`](frontend/UNEGario/)
- **Funcionalidad**: Gestión de horarios universitarios
- **Tecnologías**: JavaScript, Google Calendar API
- **Características**: Integración con calendarios, interfaz intuitiva
- **Estado**: ✅ Funcional para estudiantes

## 🛠️ Stack Tecnológico

### Frontend
- **Lenguajes**: HTML5, CSS3, JavaScript ES6+
- **Frameworks**: Vanilla JS (sin dependencias pesadas)
- **Diseño**: CSS Grid, Flexbox, Responsive Design
- **Herramientas**: CSS Custom Properties, Animations

### Backend (En desarrollo)
- **Lenguaje**: Python 3.8+
- **Framework**: FastAPI
- **Servidor**: Uvicorn ASGI
- **Validación**: Pydantic

### Integraciones
- **NVIDIA NIM Service** - Modelos de IA (Llama 4)
- **CONAGUA API** - Datos meteorológicos oficiales
- **Google Calendar API** - Gestión de horarios
- **Model Viewer** - Visualización 3D

### Desarrollo
- **Control de versiones**: Git + GitHub
- **Documentación**: Markdown
- **Despliegue**: GitHub Pages (frontend)
- **Hosting**: edbetosolutions.tech

## 🚀 Navegación del Sitio

### 🏠 Página Principal
```
https://edbetosolutions.tech/
```
Landing page con información general y enlaces directos.

### 🎯 Portafolio Completo
```
https://edbetosolutions.tech/frontend/Portafolio/
```
Vista de todos los proyectos con descripciones y enlaces.

### 📱 Proyectos Individuales
```
https://edbetosolutions.tech/frontend/clima/         # Sistema Meteorológico
https://edbetosolutions.tech/frontend/llama4/       # Chat con IA
https://edbetosolutions.tech/frontend/micveahc/     # CV Interactivo
https://edbetosolutions.tech/frontend/UNEGario/     # Sistema Universitario
```

## 🎨 Flujo de Usuario

1. **Entrada** → `index.html` (Landing page atractiva)
2. **Exploración** → `frontend/Portafolio/` (Vista general)
3. **Interacción** → Proyectos individuales
4. **Navegación** → Enlaces entre proyectos

## 📖 Documentación Específica

Cada proyecto incluye documentación detallada:

| Proyecto | Documentación | Descripción |
|----------|---------------|-------------|
| 🎯 **Portafolio** | [`frontend/Portafolio/README.md`](frontend/Portafolio/README.md) | Guía del portafolio principal |
| 🌦️ **Clima CDMX** | [`frontend/clima/READMEclima.md`](frontend/clima/READMEclima.md) | Sistema meteorológico completo |
| 🦙 **Llama 4 Chat** | [`frontend/llama4/README.md`](frontend/llama4/README.md) | Chat con IA - Frontend |
| 👨‍💼 **CV Web** | [`frontend/micveahc/READMEmicveahc.md`](frontend/micveahc/READMEmicveahc.md) | CV interactivo |
| 📚 **UNEGario** | [`frontend/UNEGario/READMEunegario.md`](frontend/UNEGario/READMEunegario.md) | Sistema universitario |
| 🚀 **Despliegue** | [`DEPLOYMENT.md`](DEPLOYMENT.md) | Guía de despliegue |

## 💻 Desarrollo Local

### Requisitos Mínimos
- **Navegador**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Servidor local** (opcional): Python 3.8+ o Node.js 14+

### Iniciar Desarrollo
```bash
# Clonar repositorio
git clone https://github.com/Edbeto13/edbetosolutions.git
cd edbetosolutions

# Servir archivos localmente (opcional)
python -m http.server 8080
# O con Node.js
npx http-server -p 8080

# Acceder en navegador
http://localhost:8080
```

### Scripts Disponibles
```bash
npm start        # Servidor de desarrollo (puerto 8080)
npm run dev      # Servidor de desarrollo (puerto 3000)
npm test         # Ejecutar tests (cuando estén disponibles)
```

## 📊 Estado de los Proyectos

| Proyecto | Estado | Tecnología Principal | Última Actualización |
|----------|--------|----------------------|---------------------|
| � **Sitio Principal** | ✅ Producción | HTML5/CSS3 | Enero 2025 |
| 🎯 **Portafolio** | ✅ Funcional | HTML5/CSS3/JS | Enero 2025 |
| �🌦️ **Clima CDMX** | ✅ Activo | JavaScript/API | Enero 2025 |
| 🦙 **Llama 4 Chat** | 🔶 Frontend listo | JavaScript | Enero 2025 |
| 👨‍💼 **CV Web** | ✅ Actualizado | HTML5/CSS3/JS | Enero 2025 |
| 📚 **UNEGario** | ✅ Funcional | JavaScript/APIs | Enero 2025 |

### Leyenda de Estados
- ✅ **Funcional**: Proyecto completo y operativo
- 🔶 **En desarrollo**: Parcialmente funcional
- ⏳ **Planeado**: En fase de planificación
- 🔧 **Mantenimiento**: Actualizaciones menores

## � Instalación y Desarrollo Local

### Prerrequisitos
- Node.js 18+ 
- Python 3.8+
- Git

### Clonar el Repositorio
```bash
git clone https://github.com/Edbeto13/edbetosolutions.git
cd edbetosolutions
```

### Configuración del Backend
```bash
cd backend
pip install -r requirements.txt
python api_server.py  # Puerto 8000
```

### Configuración del Frontend
```bash
# Servir archivos estáticos
npx serve frontend/Portafolio -p 8080
# O usar cualquier servidor HTTP
python -m http.server 8080
```

## 📚 Documentación

Para documentación técnica detallada, consulta la carpeta [`docs/`](docs/) que incluye:

- 🚀 **Guías de Deployment**
- 🔍 **Diagnósticos del Servidor** 
- �️ **Estructura del Proyecto**
- 🐍 **Configuración NVIDIA NIM**

## 🤝 Contribuciones

Este es un proyecto de portafolio personal, pero las sugerencias y feedback son bienvenidos:

1. Abre un Issue para reportar bugs o sugerir mejoras
2. Fork el proyecto para contribuciones
3. Crea un Pull Request con tus cambios

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👨‍💻 Autor

**Edson Alberto Herrera Cervantes**
- 🌐 Website: [edbetosolutions.tech](https://edbetosolutions.tech)
- 💼 LinkedIn: [Perfil profesional](https://edbetosolutions.tech/micveahc)
- 📧 Contacto: A través del sitio web

---

⭐ Si este proyecto te resulta útil, ¡dale una estrella!
- **📧 Email**: [edbeto13@gmail.com](mailto:edbeto13@gmail.com)

### Desarrollo
- **💻 GitHub**: [@Edbeto13](https://github.com/Edbeto13)
- **📂 Repositorio**: [edbetosolutions](https://github.com/Edbeto13/edbetosolutions)

### Recursos
- **📋 Issues**: [GitHub Issues](https://github.com/Edbeto13/edbetosolutions/issues)
- **🔄 Contribuciones**: [GitHub PRs](https://github.com/Edbeto13/edbetosolutions/pulls)
- **📈 Proyecto**: [GitHub Projects](https://github.com/Edbeto13/edbetosolutions/projects)

## 📄 Licencia

© 2025 EdBetoSolutions. Todos los derechos reservados.

---

**Desarrollado con ❤️ por EdBetoSolutions**
