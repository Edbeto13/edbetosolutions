# 💼 MicVeaHC - Currículum Vitae Web

Página web personal tipo currículum vitae con diseño moderno y responsivo, destacando habilidades, proyectos y experiencia profesional.

## 🌟 Características

- **Diseño profesional** con animaciones suaves y transiciones
- **Secciones interactivas** para mostrar habilidades y experiencia
- **Visualizador de credenciales** con galería de certificaciones
- **Modo oscuro/claro** adaptado a preferencias del sistema
- **Totalmente responsive** para cualquier dispositivo

## 📁 Estructura de Archivos

```
micveahc/
├── micveahc.html           # Página principal HTML
├── micveahc.js             # Funcionalidad JavaScript
├── micveahc.css            # Estilos CSS
└── assets/                 # Recursos multimedia
    ├── profile-photo.jpg   # Foto de perfil
    ├── cv-edson-herrera.pdf # CV en formato PDF
    ├── Hydredlogos/        # Logotipos de la marca
    │   ├── HydredLogo.png
    │   └── HydredLetras.png
    └── credentials/        # Certificaciones y credenciales
        ├── python-essentials-1.1.png
        ├── networking-basics.png
        └── ...             # Otras certificaciones
```

## 🚀 Uso e Instalación

### Vista local

1. **Abrir directamente** el archivo HTML:
   - Doble clic en `micveahc.html` para abrir en tu navegador predeterminado

2. **Mediante servidor HTTP** (recomendado):
   ```bash
   python -m http.server 8080
   ```
   Luego navega a `http://localhost:8080/micveahc.html`

## 🎨 Personalización

### Editar información personal

1. **Abre** `micveahc.html` en un editor
2. **Modifica** las secciones:
   - Información de contacto
   - Resumen profesional
   - Listado de habilidades
   - Proyectos destacados
   - Experiencia laboral

### Cambiar estilos y apariencia

1. **Edita** `micveahc.css` para personalizar:
   - Colores y temas
   - Tipografías
   - Espaciados y márgenes
   - Animaciones

### Añadir nuevas certificaciones

1. **Añade** las imágenes a `/assets/credentials/`
2. **Actualiza** la galería en `micveahc.html`

## 🖌️ Características de Diseño

- **Paleta de colores** profesional con acentos
- **Tipografía** moderna y legible
- **Animaciones** con IntersectionObserver para elementos al aparecer en viewport
- **Efectos hover** en tarjetas de proyectos
- **Iconografía** consistente con temática tecnológica

## 💻 Elementos Interactivos

- **Barra de navegación** con scroll suave
- **Gráficos de barras** para visualización de habilidades técnicas
- **Galería de proyectos** con información detallada
- **Timeline** para experiencia profesional
- **Formulario de contacto** con validación

## 📱 Responsive Design

La página está optimizada para:
- **Dispositivos móviles** (< 768px)
- **Tablets** (768px - 1024px)
- **Escritorio** (> 1024px)
- **Pantallas grandes** (> 1440px)

Utiliza un enfoque mobile-first con media queries para adaptarse a diferentes tamaños de pantalla.

## 🔍 SEO y Accesibilidad

- **Etiquetas meta** para SEO
- **Estructura semántica** HTML5
- **Atributos ARIA** para accesibilidad
- **Alt text** en todas las imágenes
- **Contraste** adecuado entre texto y fondo

## 🛠️ Tecnologías Utilizadas

- **HTML5** para estructura
- **CSS3** con variables personalizadas
- **JavaScript** vanilla para interactividad
- **IntersectionObserver API** para animaciones al scroll
- **LocalStorage** para preferencias de usuario

---

**Desarrollado por Edson Herrera**

*MicVeaHC v1.0 - Agosto 2025*
