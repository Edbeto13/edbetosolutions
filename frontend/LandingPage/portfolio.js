// Portfolio Landing Page JavaScript
// Funcionalidad interactiva para la página principal del portfolio

// Función para mostrar notificaciones
function showNotification(message, type = 'info') {
    const statusDiv = document.getElementById('statusMessage');
    if (statusDiv) {
        statusDiv.textContent = message;
        statusDiv.className = `status-message ${type} show`;
        
        setTimeout(() => {
            statusDiv.classList.remove('show');
        }, 3000);
    }
}

// Inicialización cuando el DOM está listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('Portfolio Landing Page loaded');
    
    // Configurar eventos para enlaces de aplicaciones
    const appLinks = document.querySelectorAll('.btn-primary');
    appLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href && href.includes('frontend/')) {
                showNotification('Cargando aplicación...', 'info');
            }
        });
    });
    
    // Efecto de scroll suave
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Animaciones de entrada para las cards
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Aplicar animación a las cards
    document.querySelectorAll('.app-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
    
    showNotification('Portfolio cargado correctamente', 'success');
});

// Exportar funciones si se necesitan en otros scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        showNotification
    };
}
