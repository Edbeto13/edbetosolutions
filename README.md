# 🚀 EdBetoSolutions

**Soluciones tecnológicas innovadoras** - Portafolio de proyectos web y aplicaciones

## 📁 Estructura del Proyecto

```
edbetosolutions/
├── backend/                    # Servicios backend y APIs
│   └── llama4/                # Backend del chat con Llama 4
│       ├── api/               # Endpoints de la API
│       ├── core/              # Configuración central
│       ├── services/          # Servicios de negocio
│       └── main.py           # Punto de entrada
├── frontend/                   # Aplicaciones frontend
│   ├── clima/                 # Sistema Meteorológico CDMX
│   ├── llama4/               # Chat con Llama 4 (Frontend)
│   ├── micveahc/             # CV Web Interactivo
│   └── UNEGario/             # Sistema de Horarios Universitarios
├── index.html                 # Página principal del portafolio
└── README.md                 # Este archivo
```

## 🌟 Proyectos Destacados

### 🌦️ Sistema Meteorológico CDMX
**Ubicación**: [`frontend/clima`](frontend/clima)
- Visualización en tiempo real del clima por alcaldías
- Integración con datos de CONAGUA
- Mapas interactivos y gráficos temporales
- Modelos 3D meteorológicos

### 🦙 Chat con Llama 4
**Backend**: [`backend/llama4`](backend/llama4) | **Frontend**: [`frontend/llama4`](frontend/llama4)
- Chat interactivo con Meta Llama 4 Maverick
- Integración con NVIDIA NIM Service
- API REST con FastAPI
- Interfaz moderna y responsiva

### 👨‍💼 CV Web Interactivo
**Ubicación**: [`frontend/micveahc`](frontend/micveahc)
- Currículum vitae web profesional
- Diseño responsivo y moderno
- Descarga en PDF
- Información de contacto y proyectos

### 📚 UNEGario - Sistema Universitario
**Ubicación**: [`frontend/UNEGario`](frontend/UNEGario)
- Gestión de horarios universitarios
- Integración con Google Calendar
- Interfaz intuitiva para estudiantes

## 🛠️ Tecnologías Utilizadas

### Backend
- **Python** con FastAPI
- **NVIDIA NIM Service** para IA
- **Pydantic** para validación
- **Uvicorn** como servidor ASGI

### Frontend
- **HTML5**, **CSS3**, **JavaScript** (Vanilla)
- **Responsive Design** con CSS Grid/Flexbox
- **APIs REST** para comunicación
- **Animaciones CSS** modernas

### Integración
- **CONAGUA API** para datos meteorológicos
- **Google Calendar API** para horarios
- **NVIDIA NIM** para modelos de IA
- **Model Viewer** para modelos 3D

## 🚀 Comenzar

### Ver el Portafolio
1. Abrir [`index.html`](index.html) en el navegador
2. Navegar por los diferentes proyectos
3. Cada proyecto tiene su propia documentación

### Ejecutar Backend (Llama 4)
```bash
cd backend/llama4
pip install -r requirements.txt
python main.py
```

### Configurar Frontend
1. Los proyectos frontend son estáticos
2. Abrir el archivo `index.html` correspondiente
3. Para desarrollo, usar un servidor local:
```bash
python -m http.server 8080
```

## 📖 Documentación

Cada proyecto tiene su propia documentación detallada:

- **Sistema Meteorológico**: [`frontend/clima/READMEclima.md`](frontend/clima/READMEclima.md)
- **Chat Llama 4 (Backend)**: [`backend/llama4/README.md`](backend/llama4/README.md)
- **Chat Llama 4 (Frontend)**: [`frontend/llama4/README.md`](frontend/llama4/README.md)
- **CV Web**: [`frontend/micveahc/READMEmicveahc.md`](frontend/micveahc/READMEmicveahc.md)
- **UNEGario**: [`frontend/UNEGario/READMEunegario.md`](frontend/UNEGario/READMEunegario.md)

## 🌐 Demo en Vivo

### Acceso Local
- **Portafolio Principal**: `file:///path/to/index.html`
- **Chat Llama 4**: `http://localhost:8000` (requiere backend)
- **Otros Proyectos**: Acceso directo desde el portafolio

## 🔧 Desarrollo y Contribución

### Estructura de Desarrollo
1. **Backend**: APIs y servicios en `/backend`
2. **Frontend**: Aplicaciones web en `/frontend`
3. **Documentación**: READMEs específicos por proyecto
4. **Configuración**: Archivos `.env` para variables de entorno

### Agregar Nuevo Proyecto
1. **Frontend**: Crear carpeta en `/frontend/nuevo-proyecto`
2. **Backend**: Crear carpeta en `/backend/nuevo-proyecto`
3. **Documentación**: Incluir README específico
4. **Integración**: Actualizar portafolio principal

## 📊 Estado de los Proyectos

| Proyecto | Estado | Tecnología | Última Actualización |
|----------|--------|------------|---------------------|
| 🌦️ Clima CDMX | ✅ Activo | HTML/CSS/JS | Enero 2025 |
| 🦙 Llama 4 Chat | ✅ Activo | Python/FastAPI | Enero 2025 |
| 👨‍💼 CV Web | ✅ Activo | HTML/CSS/JS | Enero 2025 |
| 📚 UNEGario | ✅ Activo | HTML/CSS/JS | Enero 2025 |

## 🤝 Contacto y Soporte

- **Desarrollador**: Edson Alberto Herrera Cervantes
- **Email**: edbeto13@gmail.com
- **GitHub**: [@Edbeto13](https://github.com/Edbeto13)
- **Organización**: EdBetoSolutions

## 📄 Licencia

© 2025 EdBetoSolutions. Todos los derechos reservados.

---

**Desarrollado con ❤️ por EdBetoSolutions**
