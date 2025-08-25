# 🦙 Llama 4 Chat Frontend

Frontend web para interactuar con Meta Llama 4 Maverick a través de NVIDIA NIM Service.

## 🚀 Características

- **Chat interactivo** en tiempo real
- **Interfaz moderna** y responsiva
- **Sugerencias inteligentes** para iniciar conversaciones
- **Indicador de estado** de conexión en tiempo real
- **Formateo automático** de código en las respuestas
- **Contador de caracteres** con validación
- **Animaciones fluidas** y feedback visual
- **Historial de conversación** persistente durante la sesión

## 📁 Estructura de Archivos

```
llama4/
├── index.html              # Página principal del chat
├── styles.css              # Estilos CSS de la aplicación
├── chat.js                 # Lógica JavaScript del chat
└── README.md              # Este archivo
```

## 🛠️ Configuración

### Conexión con Backend

El frontend se conecta automáticamente al backend en `http://localhost:8000`. Para cambiar esta configuración, edita la constante `BACKEND_URL` en `chat.js`:

```javascript
const BACKEND_URL = 'http://tu-servidor:puerto';
```

### Personalización de la Interfaz

#### Cambiar Colores y Temas
Edita las variables CSS en `styles.css`:

```css
:root {
    --primary-color: #0052cc;     /* Color principal */
    --accent-color: #28a745;      /* Color de éxito */
    --error-color: #dc3545;       /* Color de error */
    /* ... más variables */
}
```

#### Modificar Sugerencias de Chat
Edita las sugerencias en `index.html`:

```html
<span class="chip" data-suggestion="Tu pregunta aquí">🤖 Tu sugerencia</span>
```

## 🎨 Funcionalidades

### Chat Interactivo
- **Envío de mensajes**: Enter para enviar, Shift+Enter para nueva línea
- **Limpieza de conversación**: Botón para reiniciar el chat
- **Auto-resize**: El área de texto se ajusta automáticamente
- **Límite de caracteres**: Máximo 2000 caracteres por mensaje

### Estados Visuales
- **Conectado**: Indicador verde cuando el backend está disponible
- **Desconectado**: Indicador rojo cuando hay problemas de conexión
- **Procesando**: Animación mientras se espera respuesta del modelo
- **Escribiendo**: Indicador animado cuando el asistente está respondiendo

### Responsive Design
- **Desktop**: Experiencia completa con todas las funcionalidades
- **Tablet**: Interfaz adaptada para pantallas medianas
- **Mobile**: Optimizada para dispositivos móviles

## 🔧 Desarrollo

### Estructura del Código JavaScript

```javascript
// Configuración inicial
const BACKEND_URL = 'http://localhost:8000';
const MAX_CHARS = 2000;

// Funciones principales
init()                    // Inicialización del chat
checkServiceStatus()      // Verificación de conexión
handleSendMessage()       // Envío de mensajes
updateStatusIndicator()   // Actualización de estado
```

### Eventos y Listeners

- **Input de texto**: Auto-resize, conteo de caracteres, validación
- **Botones**: Enviar mensaje, limpiar chat
- **Sugerencias**: Click para rellenar el input
- **Estado del servicio**: Verificación periódica cada 30 segundos

### Animaciones y Transiciones

- **Entrada de mensajes**: Slide-in desde abajo
- **Indicador de pensando**: Dots pulsantes
- **Estados de botones**: Hover effects y transformaciones
- **Scroll automático**: Hacia el último mensaje

## 🌐 Integración

### Endpoints del Backend Utilizados

- `GET /api/status` - Verificar estado del servicio
- `POST /api/chat` - Enviar mensaje al modelo
- `GET /api/health` - Health check básico

### Formato de Mensajes

```javascript
// Estructura de mensaje enviado
{
    "messages": [
        {"role": "user", "content": "mensaje del usuario"},
        {"role": "assistant", "content": "respuesta anterior"}
    ],
    "stream": false,
    "temperature": 0.7,
    "max_tokens": 512
}
```

## 🎯 Uso

1. **Abrir en navegador**: Cargar `index.html`
2. **Verificar conexión**: El indicador debe mostrar "Conectado"
3. **Escribir mensaje**: En el área de texto inferior
4. **Enviar**: Presionar Enter o hacer clic en el botón enviar
5. **Continuar conversación**: El historial se mantiene automáticamente

### Atajos de Teclado

- `Enter`: Enviar mensaje
- `Shift+Enter`: Nueva línea
- `Ctrl+Enter`: Nueva línea
- `Ctrl+L`: No implementado (reservado para limpiar)

## 🔍 Solución de Problemas

### El indicador muestra "Desconectado"
- Verificar que el backend esté ejecutándose
- Comprobar la URL del backend en `chat.js`
- Revisar la consola del navegador para errores de CORS

### Los mensajes no se envían
- Verificar conexión a internet
- Comprobar que el campo no esté vacío
- Verificar límite de caracteres (máximo 2000)

### La interfaz no se ve correctamente
- Verificar que `styles.css` se cargue correctamente
- Comprobar la consola para errores de recursos
- Asegurar compatibilidad del navegador

## 📱 Compatibilidad

### Navegadores Soportados
- ✅ Chrome 90+
- ✅ Firefox 90+
- ✅ Safari 14+
- ✅ Edge 90+

### Características Modernas Utilizadas
- CSS Grid y Flexbox
- Fetch API
- ES6+ JavaScript
- CSS Custom Properties
- Modern animations

## 🚀 Mejoras Futuras

- [ ] **Modo oscuro** automático
- [ ] **Exportar conversaciones** a PDF/texto
- [ ] **Configuración avanzada** del modelo
- [ ] **Streaming de respuestas** en tiempo real
- [ ] **Soporte para archivos** adjuntos
- [ ] **Modo offline** con cache

## 📄 Licencia

Este proyecto es parte de EdBetoSolutions © 2025

---

**Desarrollado con ❤️ por el equipo de EdBetoSolutions**
