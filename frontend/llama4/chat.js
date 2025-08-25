document.addEventListener('DOMContentLoaded', () => {
    // Elementos del DOM
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const clearButton = document.getElementById('clear-button');
    const statusIndicator = document.getElementById('status-indicator');
    const charCounter = document.getElementById('char-counter');
    
    // Estado de la aplicación
    let messageHistory = [];
    let isProcessing = false;
    const MAX_CHARS = 2000;
    
    // URL del backend - ajustar según configuración
    const BACKEND_URL = 'http://localhost:8000';
    
    // Inicialización
    init();
    
    async function init() {
        console.log('Inicializando chat con Llama 4...');
        
        // Verificar estado del servicio
        await checkServiceStatus();
        
        // Configurar event listeners
        setupEventListeners();
        
        // Configurar sugerencias
        setupSuggestions();
        
        // Enfocar el input
        userInput.focus();
        
        console.log('Chat inicializado correctamente');
    }
    
    async function checkServiceStatus() {
        try {
            const response = await fetch(`${BACKEND_URL}/api/status`);
            const status = await response.json();
            
            updateStatusIndicator(status.status === 'ok', status.message || 'Servicio disponible');
            
            if (status.status !== 'ok') {
                console.warn('Advertencia del servicio:', status);
            }
        } catch (error) {
            console.error('Error al verificar estado:', error);
            updateStatusIndicator(false, 'Error de conexión');
        }
    }
    
    function updateStatusIndicator(isConnected, message) {
        const statusText = statusIndicator.querySelector('.status-text');
        
        statusIndicator.className = 'status-indicator';
        if (isConnected) {
            statusIndicator.classList.add('connected');
            statusText.textContent = 'Conectado';
        } else {
            statusIndicator.classList.add('error');
            statusText.textContent = message || 'Desconectado';
        }
    }
    
    function setupEventListeners() {
        // Botón enviar
        sendButton.addEventListener('click', handleSendMessage);
        
        // Botón limpiar
        clearButton.addEventListener('click', handleClearChat);
        
        // Input de texto
        userInput.addEventListener('keydown', handleKeyDown);
        userInput.addEventListener('input', handleInputChange);
        
        // Auto-resize del textarea
        userInput.addEventListener('input', autoResizeTextarea);
    }
    
    function setupSuggestions() {
        const suggestionChips = document.querySelectorAll('.chip[data-suggestion]');
        suggestionChips.forEach(chip => {
            chip.addEventListener('click', () => {
                const suggestion = chip.getAttribute('data-suggestion');
                userInput.value = suggestion;
                userInput.focus();
                updateCharCounter();
                autoResizeTextarea();
            });
        });
    }
    
    function handleKeyDown(event) {
        if (event.key === 'Enter' && !event.shiftKey && !event.ctrlKey) {
            event.preventDefault();
            handleSendMessage();
        }
    }
    
    function handleInputChange() {
        updateCharCounter();
    }
    
    function updateCharCounter() {
        const currentLength = userInput.value.length;
        charCounter.textContent = `${currentLength}/${MAX_CHARS}`;
        
        charCounter.className = 'char-counter';
        if (currentLength > MAX_CHARS * 0.9) {
            charCounter.classList.add(currentLength > MAX_CHARS ? 'error' : 'warning');
        }
        
        // Deshabilitar envío si excede el límite
        sendButton.disabled = currentLength > MAX_CHARS || currentLength === 0 || isProcessing;
    }
    
    function autoResizeTextarea() {
        userInput.style.height = 'auto';
        userInput.style.height = Math.min(userInput.scrollHeight, 120) + 'px';
    }
    
    async function handleSendMessage() {
        const message = userInput.value.trim();
        if (!message || isProcessing || message.length > MAX_CHARS) return;
        
        try {
            // Preparar UI para envío
            setProcessingState(true);
            
            // Limpiar input
            userInput.value = '';
            updateCharCounter();
            autoResizeTextarea();
            
            // Remover mensaje de bienvenida si existe
            removeWelcomeMessage();
            
            // Añadir mensaje del usuario
            addMessage(message, 'user');
            
            // Añadir al historial
            messageHistory.push({
                role: 'user',
                content: message
            });
            
            // Mostrar indicador de pensando
            const thinkingElement = showThinking();
            
            // Enviar solicitud a la API
            const response = await sendToAPI(messageHistory);
            
            // Remover indicador de pensando
            thinkingElement.remove();
            
            if (response && response.choices && response.choices[0]) {
                const assistantMessage = response.choices[0].message.content;
                
                // Añadir respuesta del asistente
                addMessage(assistantMessage, 'assistant');
                
                // Añadir al historial
                messageHistory.push({
                    role: 'assistant',
                    content: assistantMessage
                });
            } else {
                throw new Error('Respuesta inválida del servidor');
            }
            
        } catch (error) {
            console.error('Error al enviar mensaje:', error);
            
            // Remover indicador de pensando si existe
            const thinkingElement = document.querySelector('.thinking');
            if (thinkingElement) {
                thinkingElement.remove();
            }
            
            // Mostrar mensaje de error
            addMessage(
                '❌ Lo siento, ha ocurrido un error al procesar tu mensaje. Por favor, inténtalo de nuevo.',
                'assistant'
            );
        } finally {
            setProcessingState(false);
        }
    }
    
    async function sendToAPI(messages) {
        const response = await fetch(`${BACKEND_URL}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                messages: messages,
                stream: false,
                temperature: 0.7,
                max_tokens: 512
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Error HTTP: ${response.status}`);
        }
        
        return await response.json();
    }
    
    function addMessage(content, role) {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${role}-message fade-in`;
        
        // Formatear contenido (básico)
        const formattedContent = formatMessageContent(content);
        
        if (formattedContent.includes('<')) {
            messageElement.innerHTML = formattedContent;
        } else {
            messageElement.textContent = formattedContent;
        }
        
        chatMessages.appendChild(messageElement);
        
        // Scroll al final
        scrollToBottom();
        
        return messageElement;
    }
    
    function formatMessageContent(content) {
        // Formateo básico de código y texto
        return content
            .replace(/```(\\w*)\\n([\\s\\S]*?)```/g, (match, language, code) => {
                return `<pre><code class="${language}">${escapeHtml(code.trim())}</code></pre>`;
            })
            .replace(/`([^`]+)`/g, '<code>$1</code>')
            .replace(/\\n/g, '<br>');
    }
    
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    function showThinking() {
        const thinkingElement = document.createElement('div');
        thinkingElement.className = 'thinking fade-in';
        thinkingElement.innerHTML = `
            Pensando
            <div class="dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        
        chatMessages.appendChild(thinkingElement);
        scrollToBottom();
        
        return thinkingElement;
    }
    
    function removeWelcomeMessage() {
        const welcomeMessage = document.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.style.animation = 'fadeOut 0.3s ease';
            setTimeout(() => {
                welcomeMessage.remove();
            }, 300);
        }
    }
    
    function handleClearChat() {
        if (confirm('¿Estás seguro de que quieres limpiar toda la conversación?')) {
            // Limpiar historial y mensajes
            messageHistory = [];
            
            // Limpiar mensajes del chat (excepto bienvenida)
            const messages = chatMessages.querySelectorAll('.message:not(.welcome-message)');
            messages.forEach(message => {
                message.style.animation = 'fadeOut 0.3s ease';
                setTimeout(() => {
                    if (message.parentNode) {
                        message.remove();
                    }
                }, 300);
            });
            
            // Enfocar input
            userInput.focus();
            
            console.log('Conversación limpiada');
        }
    }
    
    function setProcessingState(processing) {
        isProcessing = processing;
        sendButton.disabled = processing || userInput.value.trim().length === 0;
        userInput.disabled = processing;
        
        if (processing) {
            sendButton.classList.add('loading');
            sendButton.querySelector('.send-icon').classList.add('spinning');
        } else {
            sendButton.classList.remove('loading');
            sendButton.querySelector('.send-icon').classList.remove('spinning');
            userInput.focus();
        }
    }
    
    function scrollToBottom() {
        setTimeout(() => {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 100);
    }
    
    // Verificar estado periódicamente
    setInterval(checkServiceStatus, 30000); // Cada 30 segundos
    
    // CSS para animaciones adicionales
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeOut {
            from { opacity: 1; transform: translateY(0); }
            to { opacity: 0; transform: translateY(-20px); }
        }
    `;
    document.head.appendChild(style);
    
    console.log('Chat.js cargado completamente');
});
