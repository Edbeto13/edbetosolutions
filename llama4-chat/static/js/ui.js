/**
 * EdBetoSolutions - Llama 4 Chat
 * Módulo de interfaz de usuario y utilidades
 */

class UIManager {
    constructor() {
        this.modals = {};
        this.init();
    }

    init() {
        this.setupModals();
        this.setupSettings();
        this.setupFooterLinks();
        this.setupKeyboardShortcuts();
    }

    /**
     * Configurar modales
     */
    setupModals() {
        // Modal de configuración
        const settingsBtn = document.getElementById('settings-btn');
        const settingsModal = document.getElementById('settings-modal');
        const modalClose = document.getElementById('modal-close');

        if (settingsBtn && settingsModal) {
            settingsBtn.addEventListener('click', () => {
                this.showModal('settings-modal');
            });

            modalClose?.addEventListener('click', () => {
                this.hideModal('settings-modal');
            });

            // Cerrar modal al hacer clic fuera
            settingsModal.addEventListener('click', (e) => {
                if (e.target === settingsModal) {
                    this.hideModal('settings-modal');
                }
            });
        }
    }

    /**
     * Configurar panel de configuración
     */
    setupSettings() {
        // Slider de temperatura
        const temperatureSlider = document.getElementById('temperature-slider');
        const temperatureValue = document.getElementById('temperature-value');

        if (temperatureSlider && temperatureValue) {
            temperatureSlider.addEventListener('input', (e) => {
                const value = parseFloat(e.target.value);
                temperatureValue.textContent = value.toFixed(1);
                
                if (window.llama4Chat) {
                    window.llama4Chat.updateSettings({ temperature: value });
                }
            });
        }

        // Input de max tokens
        const maxTokensInput = document.getElementById('max-tokens-input');
        if (maxTokensInput) {
            maxTokensInput.addEventListener('change', (e) => {
                const value = parseInt(e.target.value);
                if (value >= 50 && value <= 1000) {
                    if (window.llama4Chat) {
                        window.llama4Chat.updateSettings({ maxTokens: value });
                    }
                }
            });
        }

        // Checkbox de auto-scroll
        const autoScrollCheckbox = document.getElementById('auto-scroll-checkbox');
        if (autoScrollCheckbox) {
            autoScrollCheckbox.addEventListener('change', (e) => {
                if (window.llama4Chat) {
                    window.llama4Chat.updateSettings({ autoScroll: e.target.checked });
                }
            });
        }

        // Cargar configuración inicial
        this.loadSettingsUI();
    }

    /**
     * Cargar configuración en la UI
     */
    loadSettingsUI() {
        if (!window.llama4Chat) return;

        const settings = window.llama4Chat.settings;

        // Temperatura
        const temperatureSlider = document.getElementById('temperature-slider');
        const temperatureValue = document.getElementById('temperature-value');
        if (temperatureSlider && temperatureValue) {
            temperatureSlider.value = settings.temperature;
            temperatureValue.textContent = settings.temperature.toFixed(1);
        }

        // Max tokens
        const maxTokensInput = document.getElementById('max-tokens-input');
        if (maxTokensInput) {
            maxTokensInput.value = settings.maxTokens;
        }

        // Auto-scroll
        const autoScrollCheckbox = document.getElementById('auto-scroll-checkbox');
        if (autoScrollCheckbox) {
            autoScrollCheckbox.checked = settings.autoScroll;
        }
    }

    /**
     * Configurar enlaces del footer
     */
    setupFooterLinks() {
        // Link de API docs
        const apiDocsLink = document.getElementById('api-docs-link');
        if (apiDocsLink) {
            apiDocsLink.addEventListener('click', (e) => {
                e.preventDefault();
                this.showAPIDocumentation();
            });
        }

        // Link de acerca de
        const aboutLink = document.getElementById('about-link');
        if (aboutLink) {
            aboutLink.addEventListener('click', (e) => {
                e.preventDefault();
                this.showAboutInfo();
            });
        }
    }

    /**
     * Configurar atajos de teclado
     */
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + L para limpiar chat
            if ((e.ctrlKey || e.metaKey) && e.key === 'l') {
                e.preventDefault();
                if (window.llama4Chat) {
                    window.llama4Chat.handleClearChat();
                }
            }

            // Escape para cerrar modales
            if (e.key === 'Escape') {
                this.hideAllModals();
            }

            // Ctrl/Cmd + , para configuración
            if ((e.ctrlKey || e.metaKey) && e.key === ',') {
                e.preventDefault();
                this.showModal('settings-modal');
            }
        });
    }

    /**
     * Mostrar modal
     */
    showModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('show');
            this.modals[modalId] = true;

            // Cargar configuración si es el modal de settings
            if (modalId === 'settings-modal') {
                setTimeout(() => this.loadSettingsUI(), 100);
            }
        }
    }

    /**
     * Ocultar modal
     */
    hideModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('show');
            delete this.modals[modalId];
        }
    }

    /**
     * Ocultar todos los modales
     */
    hideAllModals() {
        Object.keys(this.modals).forEach(modalId => {
            this.hideModal(modalId);
        });
    }

    /**
     * Mostrar documentación de la API
     */
    showAPIDocumentation() {
        const apiInfo = `
# API Documentation - EdBetoSolutions Llama 4 Chat

## Endpoints Disponibles:

### POST /api/chat
Enviar mensaje al chat
**Body:**
\`\`\`json
{
    "messages": [
        {"role": "user", "content": "Hola"}
    ],
    "temperature": 0.7,
    "max_tokens": 512,
    "stream": false
}
\`\`\`

### GET /api/status
Obtener estado del servicio
**Response:**
\`\`\`json
{
    "status": "ok",
    "nim_client": "disponible",
    "connection": "exitosa",
    "model": "meta/llama-4-maverick-17b-128e-instruct"
}
\`\`\`

### GET /api/health
Health check básico
**Response:**
\`\`\`json
{
    "status": "healthy",
    "service": "EdBetoSolutions Llama 4 Chat"
}
\`\`\`

## Modelo Utilizado:
- **Meta Llama 4 Maverick 17B** via NVIDIA NIM Service
- Contexto: 128K tokens
- Optimizado para conversación y código
        `;

        this.showInfoModal('Documentación de la API', apiInfo);
    }

    /**
     * Mostrar información acerca de
     */
    showAboutInfo() {
        const aboutInfo = `
# EdBetoSolutions - Chat con Llama 4

## 🚀 Acerca de este proyecto

Esta aplicación de chat interactivo utiliza **Meta Llama 4 Maverick** a través de NVIDIA NIM Service para proporcionar una experiencia de conversación avanzada con IA.

## ✨ Características:

- **🤖 IA Avanzada**: Powered by Meta Llama 4 Maverick 17B
- **⚡ Respuestas Rápidas**: Integración con NVIDIA NIM Service
- **💬 Conversación Contextual**: Mantiene el hilo de la conversación
- **🔧 Formateo de Código**: Soporte para código y sintaxis
- **📱 Responsive Design**: Funciona en desktop y móvil
- **⚙️ Configurable**: Ajusta temperatura y parámetros
- **🔒 Seguro**: Validación y sanitización de entrada

## 🛠️ Tecnologías:

- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **Backend**: Python FastAPI
- **IA**: Meta Llama 4 Maverick via NVIDIA NIM
- **Estilo**: CSS Grid, Flexbox, Variables CSS

## 👨‍💻 Desarrollado por:

**EdBetoSolutions** - Soluciones de desarrollo innovadoras

📧 Contacto: edbetodev@gmail.com
🌐 GitHub: github.com/Edbeto13

---

© 2025 EdBetoSolutions. Desarrollado con ❤️ y tecnología NVIDIA NIM.
        `;

        this.showInfoModal('Acerca de EdBetoSolutions Llama 4 Chat', aboutInfo);
    }

    /**
     * Mostrar modal de información
     */
    showInfoModal(title, content) {
        // Crear modal dinámico
        const modal = document.createElement('div');
        modal.className = 'modal show';
        modal.innerHTML = `
            <div class="modal-content" style="max-width: 700px;">
                <div class="modal-header">
                    <h3>${title}</h3>
                    <button class="modal-close">&times;</button>
                </div>
                <div class="modal-body">
                    <pre style="white-space: pre-wrap; font-family: inherit; background: var(--bg-secondary); padding: 1rem; border-radius: 8px; max-height: 60vh; overflow-y: auto;">${content}</pre>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        // Event listeners
        const closeBtn = modal.querySelector('.modal-close');
        closeBtn.addEventListener('click', () => {
            modal.remove();
        });

        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });

        // Cerrar con Escape
        const escapeHandler = (e) => {
            if (e.key === 'Escape') {
                modal.remove();
                document.removeEventListener('keydown', escapeHandler);
            }
        };
        document.addEventListener('keydown', escapeHandler);
    }

    /**
     * Crear notificación toast
     */
    showToast(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--bg-primary);
            color: var(--text-primary);
            padding: 1rem 1.5rem;
            border-radius: var(--border-radius);
            box-shadow: var(--shadow-lg);
            z-index: 10000;
            animation: slideInRight 0.3s ease;
            border-left: 4px solid ${type === 'error' ? 'var(--error-color)' : 
                                   type === 'success' ? 'var(--success-color)' : 
                                   type === 'warning' ? 'var(--warning-color)' : 
                                   'var(--primary-color)'};
        `;

        document.body.appendChild(toast);

        // Auto-remove
        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.remove();
                }
            }, 300);
        }, duration);

        return toast;
    }

    /**
     * Utilidad para detección de dispositivos móviles
     */
    isMobile() {
        return window.innerWidth <= 768;
    }

    /**
     * Utilidad para copiar texto al portapapeles
     */
    async copyToClipboard(text) {
        try {
            if (navigator.clipboard) {
                await navigator.clipboard.writeText(text);
                this.showToast('Texto copiado al portapapeles', 'success');
            } else {
                // Fallback para navegadores antiguos
                const textArea = document.createElement('textarea');
                textArea.value = text;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                this.showToast('Texto copiado al portapapeles', 'success');
            }
        } catch (error) {
            console.error('Error al copiar:', error);
            this.showToast('Error al copiar texto', 'error');
        }
    }

    /**
     * Formatear tiempo transcurrido
     */
    formatTimeAgo(date) {
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);
        const diffDays = Math.floor(diffMs / 86400000);

        if (diffMins < 1) return 'ahora';
        if (diffMins < 60) return `hace ${diffMins}m`;
        if (diffHours < 24) return `hace ${diffHours}h`;
        return `hace ${diffDays}d`;
    }
}

// CSS adicional para animaciones
const additionalStyles = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }

    .toast {
        font-size: 0.875rem;
        font-weight: 500;
        cursor: pointer;
        transition: var(--transition);
    }

    .toast:hover {
        transform: translateX(-5px);
    }
`;

// Inyectar estilos adicionales
const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet);

// Inicializar UI Manager cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.uiManager = new UIManager();
});

// Exportar para uso externo
if (typeof module !== 'undefined' && module.exports) {
    module.exports = UIManager;
}
