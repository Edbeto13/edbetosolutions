# 📁 Estructura de Archivos - EdBetoSolutions

```
📁 edbetosolutions/
│
├── 🌐 SITIO WEB
│   ├── 🏠 index.html                     # Redirección al portafolio principal
│   ├── 📋 package.json                   # Configuración del proyecto
│   ├── 📖 README.md                      # Documentación principal
│   ├── 📝 .editorconfig                  # Configuración del editor
│   ├── 🚫 .gitignore                     # Archivos ignorados
│   └── 📄 LICENSE                        # Licencia MIT
│
├── 🎨 APLICACIONES FRONTEND
│   └── 📂 frontend/
│       │
│       ├── 🎯 Portafolio/               # Portal de proyectos (PÁGINA PRINCIPAL)
│       │   ├── 📄 index.html            # Landing page completa del sitio
│       │   └── 📖 README.md             # Documentación del portafolio
│       │
│       ├── 🌦️ clima/                    # Sistema Meteorológico CDMX
│       │   ├── 🌐 index.html            # Interfaz principal
│       │   ├── 🌟 clima-production.html # Versión optimizada
│       │   ├── 🎨 styles-fixed.css      # Estilos
│       │   ├── ⚡ script-fixed.js       # Lógica principal
│       │   ├── 📖 READMEclima.md        # Documentación
│       │   ├── 📁 3Dclimagbl/           # Modelos 3D (.glb)
│       │   ├── 📁 components/           # Componentes React
│       │   └── 📁 scripts/              # Scripts de configuración
│       │
│       ├── 🦙 llama4/                   # Chat con IA Llama 4
│       │   ├── 🌐 index.html            # Interfaz del chat
│       │   ├── ⚡ chat.js               # Lógica del chat
│       │   ├── 🎨 styles.css            # Estilos del chat
│       │   └── 📖 README.md             # Documentación
│       │
│       ├── 👨‍💼 micveahc/                 # CV Web Interactivo
│       │   ├── 🌐 micveahc.html         # CV principal
│       │   ├── 🎨 micveahc.css          # Estilos del CV
│       │   ├── ⚡ micveahc.js           # Interactividad
│       │   ├── 📖 READMEmicveahc.md     # Documentación
│       │   └── 📁 assets/               # Recursos (CV PDF, fotos, etc.)
│       │       ├── 📄 cv-edson-herrera.pdf
│       │       ├── 📸 profile-photo.jpg
│       │       ├── 📁 credentials/      # Certificaciones
│       │       └── 📁 Hydredlogos/      # Logos de marca
│       │
│       └── 📚 UNEGario/                 # Sistema Universitario
│           ├── 🌐 UNEGario.html         # Interfaz principal
│           ├── ⚡ unegario.js           # Lógica del sistema
│           ├── 📖 READMEunegario.md     # Documentación
│           └── 📁 UNEGarioimages/       # Recursos visuales
│               ├── 🧠 CerebroIA.glb     # Modelo 3D cerebro
│               ├── 🏛️ UNEGLogo.png      # Logo universidad
│               └── 🎯 UNEGarioICON.png  # Icono del sistema
│
├── 🔧 CONFIGURACIÓN Y DOCUMENTACIÓN
│   ├── 📁 .github/                     # Configuraciones de GitHub
│   ├── 🚀 DEPLOYMENT.md                # Guía de despliegue
│   └── 📊 PROJECT-STRUCTURE.md         # Este archivo
│
├── 🔧 BACKEND SERVICES
│   └── 📁 backend/
│       │
│       ├── 🐍 CÓDIGO PRINCIPAL
│       │   ├── ⚡ api_server.py              # Servidor API principal
│       │   ├── 🌤️ conagua_collector.py       # Recolector datos CONAGUA
│       │   ├── 📊 conagua_timeseries.py      # Series temporales
│       │   ├── 📅 UNEGario_GoogleCalendar.py # Google Calendar API
│       │   ├── 🏗️ build_unegario.py          # Constructor UNEGario
│       │   ├── 🧪 test_conagua.py            # Tests y validaciones
│       │   ├── 📋 requirements.txt           # Dependencias Python
│       │   └── 💾 weather_cache.json         # Cache meteorológico
│       │
│       ├── ⚙️ CONFIGURACIÓN
│       │   └── 📁 config/
│       │       ├── 🌐 nginx-production.conf     # Config Nginx principal
│       │       ├── 🔧 nginx-hydredelback.conf   # Config Nginx alternativa
│       │       └── 🔄 conagua-api.service       # Servicio systemd
│       │
│       ├── 🚀 SCRIPTS Y DEPLOYMENT
│       │   ├── 📁 scripts/
│       │   │   ├── 🛠️ install-backend.sh        # Instalación automática
│       │   │   ├── 💻 Deploy-UNEGario.ps1       # Deploy (PowerShell)
│       │   │   └── 🐧 deploy-unegario.sh        # Deploy (Bash)
│       │   │
│       │   └── 📁 deploy/
│       │       ├── 📖 DEPLOYMENT.md             # Guía de deployment
│       │       ├── 🌐 edbetosolutions.tech.new  # Config dominio
│       │       └── 📁 docs/                     # Documentación adicional
│       │
│       └── 📖 DOCUMENTACIÓN
│           ├── 📄 README.md                     # Documentación principal
│           ├── 📄 README-BACKEND.md             # Guía detallada
│           └── 📄 INSTRUCCIONES.md              # Instrucciones de uso
│
└── � BACKEND SERVICES
    └── 📁 backend/                     # APIs y servicios backend
        ├── 🐍 api_server.py            # Servidor API principal
        ├── 🏗️ build_unegario.py        # Constructor UNEGario
        ├── 🌊 conagua_collector.py     # Recolector datos CONAGUA
        ├── 📊 conagua_timeseries.py    # Series temporales clima
        ├── 🧪 test_conagua.py          # Tests del API CONAGUA
        ├── 📅 UNEGario_GoogleCalendar.py # Integración Google Calendar
        ├── 📋 requirements.txt         # Dependencias Python
        ├── 🗂️ weather_cache.json      # Cache de datos climáticos
        ├── 📄 sync-assets.ps1         # Script sincronización
        │
        ├── � DOCUMENTACIÓN
        │   ├── 📋 README-BACKEND.md    # Documentación principal
        │   ├── 📝 INSTRUCCIONES.md     # Instrucciones específicas
        │   ├── � CV-DOCUMENTACION.md  # Documentación CV
        │   └── 🚀 UNEGario_DEPLOYMENT.md # Guía deployment UNEGario
        │
        ├── ⚙️ config/                  # Configuraciones del servidor
        │   ├── 🌐 nginx-edbetosolutions.conf # Config nginx principal
        │   ├── 🌐 nginx-production.conf # Config nginx producción
        │   ├── 🌐 nginx-hydredelback.conf # Config nginx Hydred
        │   └── � conagua-api.service  # Servicio systemd CONAGUA
        │
        └── 📜 scripts/                 # Scripts de deployment
            ├── 🚀 Deploy-UNEGario.ps1 # Deploy PowerShell
            ├── 🚀 deploy-unegario.sh  # Deploy Bash
            └── 📦 install-backend.sh  # Instalación backend
```

## 🎯 Navegación de Archivos

### 📄 Archivos Principales
- **🏠 Landing Page**: [`index.html`](../index.html)
- **🎯 Portafolio**: [`frontend/Portafolio/index.html`](../frontend/Portafolio/index.html)
- **📖 Documentación**: [`README.md`](../README.md)

### 🌐 Aplicaciones Web
- **🌦️ Clima**: [`frontend/clima/index.html`](../frontend/clima/index.html)
- **🦙 Chat IA**: [`frontend/llama4/index.html`](../frontend/llama4/index.html)
- **👨‍💼 CV Web**: [`frontend/micveahc/micveahc.html`](../frontend/micveahc/micveahc.html)
- **📚 Universidad**: [`frontend/UNEGario/UNEGario.html`](../frontend/UNEGario/UNEGario.html)

### 📖 Documentación Específica
- **🌦️ Clima**: [`frontend/clima/READMEclima.md`](../frontend/clima/READMEclima.md)
- **🦙 Llama 4**: [`frontend/llama4/README.md`](../frontend/llama4/README.md)
- **👨‍💼 CV**: [`frontend/micveahc/READMEmicveahc.md`](../frontend/micveahc/READMEmicveahc.md)
- **📚 UNEGario**: [`frontend/UNEGario/READMEunegario.md`](../frontend/UNEGario/READMEunegario.md)

## 📊 Estadísticas del Proyecto

### 📂 Organización
- **Total de proyectos**: 5 (1 portafolio + 4 aplicaciones)
- **Archivos HTML**: 8 páginas principales
- **Archivos JavaScript**: 4 aplicaciones interactivas
- **Archivos CSS**: 4 hojas de estilo personalizadas
- **Documentación**: 6 archivos README específicos

### 🎨 Recursos Multimedia
- **Modelos 3D**: 4 archivos (.glb)
- **Imágenes**: 10+ archivos (PNG, JPG)
- **Documentos**: 1 CV en PDF
- **Iconos**: Múltiples logos y certificaciones

### 🌐 Compatibilidad
- **Navegadores**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Dispositivos**: Desktop, Tablet, Mobile
- **Tecnologías**: HTML5, CSS3, ES6+, Web APIs

---

**📅 Última actualización**: Enero 2025  
**👨‍💻 Desarrollado por**: Edson Alberto Herrera Cervantes  
**🌐 Sitio web**: [edbetosolutions.tech](https://edbetosolutions.tech)
