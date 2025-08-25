/**
 * EdBetoSolutions - Llama 4 Chat
 * Módulo principal de funcionalidad del chat
 */

class Llama4Chat {
    constructor() {
        // Elementos del DOM
        this.chatMessages = document.getElementById('chat-messages');
        this.userInput = document.getElementById('user-input');
        this.sendButton = document.getElementById('send-button');
        this.clearButton = document.getElementById('clear-button');
        this.statusIndicator = document.getElementById('status-indicator');
        this.charCounter = document.getElementById('char-counter');

        // Estado de la aplicación
        this.messageHistory = [];
        this.isProcessing = false;
        this.settings = {
            maxTokens: 512,
            temperature: 0.7,
            autoScroll: true,
            maxChars: 2000
        };

        // Configuración de la API
        this.apiEndpoints = {
            chat: '/api/chat',
            status: '/api/status',
            health: '/api/health'
        };

        // Inicializar
        this.init();
    }

    /**
     * Inicialización de la aplicación
     */
    async init() {
        console.log('🚀 Inicializando Llama 4 Chat...');

        try {
            // Configurar event listeners
            this.setupEventListeners();
            
            // Configurar sugerencias
            this.setupSuggestions();
            
            // Verificar estado del servicio
            await this.checkServiceStatus();
            
            // Configurar auto-resize del textarea
            this.setupAutoResize();
            
            // Cargar configuración del localStorage
            this.loadSettings();
            
            // Enfocar el input
            this.userInput.focus();
            
            console.log('✅ Chat inicializado correctamente');
        } catch (error) {
            console.error('❌ Error al inicializar:', error);
            this.showError('Error al inicializar la aplicación');
        }
    }

    /**
     * Configurar event listeners
     */
    setupEventListeners() {
        // Botón enviar
        this.sendButton.addEventListener('click', () => this.handleSendMessage());
        
        // Botón limpiar
        this.clearButton.addEventListener('click', () => this.handleClearChat());
        
        // Input de texto
        this.userInput.addEventListener('keydown', (e) => this.handleKeyDown(e));
        this.userInput.addEventListener('input', () => this.handleInputChange());
        
        // Verificación periódica del estado
        setInterval(() => this.checkServiceStatus(), 30000); // Cada 30 segundos
    }

    /**
     * Configurar sugerencias de preguntas
     */
    setupSuggestions() {
        const suggestionChips = document.querySelectorAll('.chip[data-suggestion]');
        suggestionChips.forEach(chip => {
            chip.addEventListener('click', () => {
                const suggestion = chip.getAttribute('data-suggestion');
                this.userInput.value = suggestion;
                this.userInput.focus();
                this.updateCharCounter();
                this.autoResizeTextarea();
            });
        });
    }

    /**
     * Configurar auto-resize del textarea
     */
    setupAutoResize() {
        this.userInput.addEventListener('input', () => {
            this.autoResizeTextarea();
        });
    }

    /**
     * Auto-resize del textarea
     */
    autoResizeTextarea() {
        this.userInput.style.height = 'auto';
        this.userInput.style.height = Math.min(this.userInput.scrollHeight, 120) + 'px';
    }

    /**
     * Manejar teclas presionadas
     */
    handleKeyDown(event) {
        if (event.key === 'Enter' && !event.shiftKey && !event.ctrlKey) {
            event.preventDefault();
            this.handleSendMessage();
        }
    }

    /**
     * Manejar cambios en el input
     */
    handleInputChange() {
        this.updateCharCounter();
        this.updateSendButton();
    }

    /**
     * Actualizar contador de caracteres
     */
    updateCharCounter() {
        const currentLength = this.userInput.value.length;
        this.charCounter.textContent = `${currentLength}/${this.settings.maxChars}`;
        
        // Cambiar color según el límite
        this.charCounter.className = 'char-counter';
        if (currentLength > this.settings.maxChars * 0.9) {
            this.charCounter.classList.add(currentLength > this.settings.maxChars ? 'error' : 'warning');
        }
    }

    /**
     * Actualizar estado del botón enviar
     */
    updateSendButton() {
        const messageLength = this.userInput.value.trim().length;
        const exceedsLimit = messageLength > this.settings.maxChars;
        
        this.sendButton.disabled = this.isProcessing || messageLength === 0 || exceedsLimit;
    }

    /**
     * Verificar estado del servicio
     */
    async checkServiceStatus() {
        try {
            const response = await fetch(this.apiEndpoints.status);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const status = await response.json();
            this.updateStatusIndicator(status.status === 'ok', status.connection || 'Servicio disponible');
            
            return status.status === 'ok';
        } catch (error) {
            console.warn('⚠️  Error al verificar estado:', error);
            this.updateStatusIndicator(false, 'Error de conexión');
            return false;
        }
    }

    /**
     * Actualizar indicador de estado
     */
    updateStatusIndicator(isConnected, message) {
        const statusText = this.statusIndicator.querySelector('.status-text');
        
        // Limpiar clases anteriores
        this.statusIndicator.className = 'status-indicator';
        
        if (isConnected) {
            this.statusIndicator.classList.add('connected');
            statusText.textContent = 'Conectado';
        } else {
            this.statusIndicator.classList.add('error');
            statusText.textContent = message || 'Desconectado';
        }
    }

    /**
     * Manejar envío de mensaje
     */
    async handleSendMessage() {
        const message = this.userInput.value.trim();
        
        if (!message || this.isProcessing || message.length > this.settings.maxChars) {
            return;
        }

        try {
            // Preparar UI para envío
            this.setProcessingState(true);
            
            // Limpiar input
            this.userInput.value = '';
            this.updateCharCounter();
            this.autoResizeTextarea();
            
            // Remover mensaje de bienvenida si existe
            this.removeWelcomeMessage();
            
            // Añadir mensaje del usuario
            this.addMessage(message, 'user');
            
            // Añadir al historial
            this.messageHistory.push({
                role: 'user',
                content: message
            });

            // Mostrar indicador de pensando
            const thinkingElement = this.showThinking();
            
            // Enviar solicitud a la API
            const response = await this.sendToAPI(this.messageHistory);
            
            // Remover indicador de pensando
            thinkingElement.remove();
            
            if (response && response.choices && response.choices[0]) {
                const assistantMessage = response.choices[0].message.content;
                
                // Añadir respuesta del asistente
                this.addMessage(assistantMessage, 'assistant');
                
                // Añadir al historial
                this.messageHistory.push({
                    role: 'assistant',
                    content: assistantMessage
                });
            } else {
                throw new Error('Respuesta inválida del servidor');
            }
            
        } catch (error) {
            console.error('❌ Error al enviar mensaje:', error);
            
            // Remover indicador de pensando si existe
            const thinkingElement = document.querySelector('.thinking');
            if (thinkingElement) {
                thinkingElement.remove();
            }
            
            // Mostrar mensaje de error
            this.addMessage(
                '❌ Lo siento, ha ocurrido un error al procesar tu mensaje. Por favor, inténtalo de nuevo en unos momentos.',
                'assistant'
            );
        } finally {
            this.setProcessingState(false);
        }
    }

    /**
     * Enviar solicitud a la API
     */
    async sendToAPI(messages) {
        const response = await fetch(this.apiEndpoints.chat, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                messages: messages,
                stream: false,
                temperature: this.settings.temperature,
                max_tokens: this.settings.maxTokens
            })
        });
        
        if (!response.ok) {
            let errorMessage;
            try {
                const errorData = await response.json();
                errorMessage = errorData.detail || `Error HTTP: ${response.status}`;
            } catch {
                errorMessage = `Error HTTP: ${response.status}`;
            }
            throw new Error(errorMessage);
        }
        
        return await response.json();
    }

    /**
     * Añadir mensaje al chat
     */
    addMessage(content, role) {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${role}-message fade-in`;
        
        // Formatear contenido
        const formattedContent = this.formatMessageContent(content);
        
        if (this.containsHTML(formattedContent)) {
            messageElement.innerHTML = formattedContent;
        } else {
            messageElement.textContent = formattedContent;
        }
        
        this.chatMessages.appendChild(messageElement);
        
        // Scroll al final si está habilitado
        if (this.settings.autoScroll) {
            this.scrollToBottom();
        }
        
        return messageElement;
    }

    /**
     * Formatear contenido del mensaje
     */
    formatMessageContent(content) {
        return content
            // Formatear bloques de código
            .replace(/```(\w*)\n([\s\S]*?)```/g, (match, language, code) => {
                return `<pre><code class="${language}">${this.escapeHtml(code.trim())}</code></pre>`;
            })
            // Formatear código inline
            .replace(/`([^`]+)`/g, '<code>$1</code>')
            // Convertir saltos de línea
            .replace(/\n/g, '<br>');
    }

    /**
     * Verificar si el contenido contiene HTML
     */
    containsHTML(str) {
        return /<[^>]*>/g.test(str);
    }

    /**
     * Escapar HTML para prevenir XSS
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Mostrar indicador de pensando
     */
    showThinking() {
        const thinkingElement = document.createElement('div');
        thinkingElement.className = 'thinking fade-in';
        thinkingElement.innerHTML = `
            🤔 Pensando
            <div class="dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        
        this.chatMessages.appendChild(thinkingElement);
        
        if (this.settings.autoScroll) {
            this.scrollToBottom();
        }
        
        return thinkingElement;
    }

    /**
     * Remover mensaje de bienvenida
     */
    removeWelcomeMessage() {
        const welcomeMessage = document.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.style.animation = 'fadeOut 0.3s ease';
            setTimeout(() => {
                if (welcomeMessage.parentNode) {
                    welcomeMessage.remove();
                }
            }, 300);
        }
    }

    /**
     * Manejar limpieza del chat
     */
    handleClearChat() {
        if (confirm('¿Estás seguro de que quieres limpiar toda la conversación?')) {
            this.clearChat();
        }
    }

    /**
     * Limpiar chat
     */
    clearChat() {
        // Limpiar historial
        this.messageHistory = [];
        
        // Limpiar mensajes del chat (excepto bienvenida)
        const messages = this.chatMessages.querySelectorAll('.message, .thinking');
        messages.forEach(message => {
            message.style.animation = 'fadeOut 0.3s ease';
            setTimeout(() => {
                if (message.parentNode) {
                    message.remove();
                }
            }, 300);
        });
        
        // Enfocar input
        setTimeout(() => {
            this.userInput.focus();
        }, 350);
        
        console.log('🧹 Conversación limpiada');
    }

    /**
     * Establecer estado de procesamiento
     */
    setProcessingState(processing) {
        this.isProcessing = processing;
        this.updateSendButton();
        this.userInput.disabled = processing;
        
        if (processing) {
            this.sendButton.classList.add('loading');
            this.sendButton.querySelector('.send-icon').classList.add('spinning');
        } else {
            this.sendButton.classList.remove('loading');
            this.sendButton.querySelector('.send-icon').classList.remove('spinning');
            this.userInput.focus();
        }
    }

    /**
     * Scroll al final del chat
     */
    scrollToBottom() {
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }

    /**
     * Mostrar error
     */
    showError(message) {
        console.error('❌', message);
        // Aquí se podría añadir una notificación visual
    }

    /**
     * Cargar configuración del localStorage
     */
    loadSettings() {
        try {
            const savedSettings = localStorage.getItem('llama4-chat-settings');
            if (savedSettings) {
                this.settings = { ...this.settings, ...JSON.parse(savedSettings) };
            }
        } catch (error) {
            console.warn('⚠️  Error al cargar configuración:', error);
        }
    }

    /**
     * Guardar configuración en localStorage
     */
    saveSettings() {
        try {
            localStorage.setItem('llama4-chat-settings', JSON.stringify(this.settings));
        } catch (error) {
            console.warn('⚠️  Error al guardar configuración:', error);
        }
    }

    /**
     * Actualizar configuración
     */
    updateSettings(newSettings) {
        this.settings = { ...this.settings, ...newSettings };
        this.saveSettings();
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.llama4Chat = new Llama4Chat();
});

// Exportar para uso externo
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Llama4Chat;
}
