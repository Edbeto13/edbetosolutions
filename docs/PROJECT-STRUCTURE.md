# 📁 Estructura de Archivos - EdBetoSolutions

```
📁 edbetosolutions/
│
├── 🌐 SITIO WEB
│   ├── 🏠 index_redirect.html            # Redirección al portafolio principal
│   ├── 📖 README.md                      # Documentación principal
│   └── 📄 LICENSE                        # Licencia MIT
│
├── 🎨 APLICACIONES FRONTEND
│   └── 📂 frontend/
│       │
│       ├── 🎯 Portafolio/               # Portal de proyectos (PÁGINA PRINCIPAL)
│       │   ├── 📄 index.html            # Landing page completa del sitio
│       │   ├── 📋 package.json          # Configuración del proyecto
│       │   └── 📖 READMEportafolio.md   # Documentación del portafolio
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
│       │   ├── ⚡ chat.js               # Lógica del chat actualizado
│       │   ├── 🎨 styles.css            # Estilos del chat
│       │   ├── 🔧 test-tool.html        # Herramienta de pruebas
│       │   └── 📖 READMELlama4.md       # Documentación
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
├── 🔧 BACKEND SERVICES
│   └── 📁 backend/
│       │
│       ├── 🐍 SERVIDORES API
│       │   ├── ⚡ api_server.py              # Servidor API principal
│       │   ├── 🦙 nvidia_api_server.py       # Servidor NVIDIA NIM Llama4
│       │   ├── 🔄 simple_api_server.py       # Servidor simplificado (503)
│       │   └── 🧪 test_nvidia_api.py         # Tests API NVIDIA
│       │
│       ├── 🌤️ SERVICIOS CLIMA
│       │   ├── 🌊 conagua_collector.py       # Recolector datos CONAGUA
│       │   ├── 📊 conagua_timeseries.py      # Series temporales
│       │   ├── 🧪 test_conagua.py            # Tests CONAGUA
│       │   └── 💾 weather_cache.json         # Cache meteorológico
│       │
│       ├── 📚 SERVICIOS UNEGARIO
│       │   ├── 📅 UNEGario_GoogleCalendar.py # Google Calendar API
│       │   └── 🏗️ build_unegario.py          # Constructor UNEGario
│       │
│       ├── ⚙️ CONFIGURACIÓN
│       │   ├── 📋 requirements.txt           # Dependencias Python
│       │   ├── 📄 sync-assets.ps1            # Script sincronización
│       │   └── 📁 config/
│       │       ├── 🌐 nginx-edbetosolutions.conf # Config Nginx principal
│       │       ├── 🌐 nginx-production.conf     # Config Nginx producción
│       │       ├── 🌐 nginx-hydredelback.conf   # Config Nginx Hydred
│       │       └── 🔄 conagua-api.service       # Servicio systemd
│       │
│       ├── 📜 SCRIPTS
│       │   └── 📁 scripts/
│       │       ├── 🛠️ install-backend.sh        # Instalación automática
│       │       ├── 🚀 run_nvidia_server.sh      # Ejecutar NVIDIA server
│       │       ├── 🔍 server-diagnostics.sh     # Diagnóstico servidor
│       │       ├── 🔧 fix-server-urgent.sh      # Reparación urgente
│       │       ├── 💻 Deploy-UNEGario.ps1       # Deploy PowerShell
│       │       └── 🐧 deploy-unegario.sh        # Deploy Bash
│       │
│       └── 📖 DOCUMENTACIÓN
│           ├── 📄 README-BACKEND.md             # Documentación principal
│           ├── 📄 INSTRUCCIONES.md              # Instrucciones de uso
│           ├── 📄 CV-DOCUMENTACION.md           # Documentación CV
│           ├── 🦙 NVIDIA-LLAMA4-README.md       # Guía NVIDIA NIM
│           ├── 🚀 DEPLOYMENT-NVIDIA.md          # Deploy NVIDIA
│           └── 📚 UNEGario_DEPLOYMENT.md        # Deploy UNEGario
│
└── 🔧 CONFIGURACIÓN Y DOCUMENTACIÓN
    ├── 🚀 DEPLOYMENT.md                # Guía de despliegue general
    ├── 📊 PROJECT-STRUCTURE.md         # Este archivo
    └── 🔍 DROPLET-DIAGNOSTICO.md       # Diagnóstico del droplet
```

## 🎯 Navegación de Archivos

### 📄 Archivos Principales
- **🏠 Landing Page**: [`index_redirect.html`](../index_redirect.html)
- **🎯 Portafolio**: [`frontend/Portafolio/index.html`](../frontend/Portafolio/index.html)
- **📖 Documentación**: [`README.md`](../README.md)

### 🌐 Aplicaciones Web
- **🌦️ Clima**: [`frontend/clima/index.html`](../frontend/clima/index.html)
- **🦙 Chat IA**: [`frontend/llama4/index.html`](../frontend/llama4/index.html)
- **👨‍💼 CV Web**: [`frontend/micveahc/micveahc.html`](../frontend/micveahc/micveahc.html)
- **📚 Universidad**: [`frontend/UNEGario/UNEGario.html`](../frontend/UNEGario/UNEGario.html)

### 🔧 Servicios Backend
- **🦙 NVIDIA NIM**: [`backend/nvidia_api_server.py`](../backend/nvidia_api_server.py)
- **🌤️ CONAGUA API**: [`backend/conagua_collector.py`](../backend/conagua_collector.py)
- **📚 UNEGario API**: [`backend/UNEGario_GoogleCalendar.py`](../backend/UNEGario_GoogleCalendar.py)

### 📖 Documentación Específica
- **🌦️ Clima**: [`frontend/clima/READMEclima.md`](../frontend/clima/READMEclima.md)
- **🦙 Llama 4**: [`frontend/llama4/READMELlama4.md`](../frontend/llama4/READMELlama4.md)
- **👨‍💼 CV**: [`frontend/micveahc/READMEmicveahc.md`](../frontend/micveahc/READMEmicveahc.md)
- **📚 UNEGario**: [`frontend/UNEGario/READMEunegario.md`](../frontend/UNEGario/READMEunegario.md)
- **🔧 Backend**: [`backend/README-BACKEND.md`](../backend/README-BACKEND.md)
- **🦙 NVIDIA NIM**: [`backend/NVIDIA-LLAMA4-README.md`](../backend/NVIDIA-LLAMA4-README.md)

### 🔧 Herramientas de Desarrollo
- **🔧 Test Tool Llama4**: [`frontend/llama4/test-tool.html`](../frontend/llama4/test-tool.html)
- **🧪 Test NVIDIA API**: [`backend/test_nvidia_api.py`](../backend/test_nvidia_api.py)
- **🔍 Diagnósticos**: [`backend/scripts/server-diagnostics.sh`](../backend/scripts/server-diagnostics.sh)

## 📊 Estadísticas del Proyecto

### 📂 Organización
- **Total de proyectos**: 5 (1 portafolio + 4 aplicaciones)
- **Servidores Backend**: 3 (API principal, NVIDIA NIM, Simple)
- **Archivos HTML**: 9 páginas principales
- **Archivos JavaScript**: 5 aplicaciones interactivas
- **Archivos Python**: 10 servicios backend
- **Documentación**: 12 archivos README y guías

### 🎨 Recursos Multimedia
- **Modelos 3D**: 4 archivos (.glb)
- **Imágenes**: 15+ archivos (PNG, JPG)
- **Documentos**: 1 CV en PDF
- **Iconos**: Múltiples logos y certificaciones

### 🌐 Tecnologías
- **Frontend**: HTML5, CSS3, JavaScript ES6+, Three.js
- **Backend**: Python 3.8+, HTTP Servers, NVIDIA NIM
- **APIs**: CONAGUA, Google Calendar, NVIDIA Llama4
- **Servidor**: DigitalOcean, Nginx, Ubuntu 22.04

### 🔒 Seguridad
- **API Keys**: Gestionadas con variables de entorno
- **HTTPS**: SSL/TLS configurado
- **CORS**: Configuración segura

---

**📅 Última actualización**: Agosto 2025  
**👨‍💻 Desarrollado por**: Edson Alberto Herrera Cervantes  
**🌐 Sitio web**: [edbetosolutions.tech](https://edbetosolutions.tech)
