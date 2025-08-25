// CV Professional Scripts - Compatible con edbetosolutions.tech
(function() {
    'use strict';

    // Configuration
    const CONFIG = {
    PDF_URL: 'assets/cv-edson-herrera.pdf',
        ANIMATION_DELAY: 100,
        SCROLL_OFFSET: 80,
        INTERSECTION_THRESHOLD: 0.1
    };

    // DOM elements
    const elements = {
        downloadBtn: null,
        printBtn: null,
        navLinks: null,
        skillBars: null,
        languageBars: null,
        sections: null
    };

    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', initializeCV);

    function initializeCV() {
        console.log('🎯 Inicializando CV Professional...');
        
        // Get DOM elements
        cacheElements();
        
        // Initialize features
        initializeDownload();
        initializePrint();
        initializeNavigation();
        initializeAnimations();
        initializeIntersectionObserver();
        initializeAccessibility();
        
        console.log('✅ CV Professional inicializado correctamente');
    }

    function cacheElements() {
        elements.downloadBtn = document.getElementById('download-cv-btn');
        elements.printBtn = document.getElementById('print-cv-btn');
        elements.navLinks = document.querySelectorAll('.cv-navigation a');
        elements.skillBars = document.querySelectorAll('.skill-bar');
        elements.languageBars = document.querySelectorAll('.language-bar');
        elements.sections = document.querySelectorAll('.cv-section[id]');
    }

    // Download functionality
    function initializeDownload() {
        if (!elements.downloadBtn) return;

        elements.downloadBtn.addEventListener('click', handleDownload);
        
        // Check if PDF exists
        checkPDFAvailability();
    }

    function handleDownload(event) {
        event.preventDefault();
        
        try {
            // Analytics tracking (if available)
            if (typeof gtag !== 'undefined') {
                gtag('event', 'download', {
                    'event_category': 'CV',
                    'event_label': 'PDF Download'
                });
            }

            // Create download link
            const link = document.createElement('a');
            link.href = CONFIG.PDF_URL;
            link.download = 'cv-edson-herrera.pdf';
            link.target = '_blank';
            link.rel = 'noopener';
            
            // Append to body, click, and remove
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            // Show success message
            showNotification('📄 CV descargado correctamente', 'success');
            
        } catch (error) {
            console.error('Error downloading CV:', error);
            showNotification('❌ Error al descargar el CV. Intenta de nuevo.', 'error');
        }
    }

    function checkPDFAvailability() {
        fetch(CONFIG.PDF_URL, { method: 'HEAD' })
            .then(response => {
                if (!response.ok) {
                    console.warn('PDF no disponible:', CONFIG.PDF_URL);
                    if (elements.downloadBtn) {
                        elements.downloadBtn.style.opacity = '0.6';
                        elements.downloadBtn.title = 'PDF no disponible temporalmente';
                    }
                }
            })
            .catch(error => {
                console.warn('No se pudo verificar el PDF:', error);
            });
    }

    // Print functionality
    function initializePrint() {
        if (!elements.printBtn) return;

        elements.printBtn.addEventListener('click', handlePrint);
    }

    function handlePrint(event) {
        event.preventDefault();
        
        try {
            // Analytics tracking
            if (typeof gtag !== 'undefined') {
                gtag('event', 'print', {
                    'event_category': 'CV',
                    'event_label': 'Print CV'
                });
            }

            // Prepare for print
            document.body.classList.add('printing');
            
            // Small delay to ensure styles are applied
            setTimeout(() => {
                window.print();
                document.body.classList.remove('printing');
            }, 100);
            
        } catch (error) {
            console.error('Error printing CV:', error);
            showNotification('❌ Error al imprimir. Intenta usar Ctrl+P.', 'error');
        }
    }

    // Navigation functionality
    function initializeNavigation() {
        if (!elements.navLinks.length) return;

        elements.navLinks.forEach(link => {
            link.addEventListener('click', handleNavClick);
        });

        // Update active nav on scroll
        window.addEventListener('scroll', throttle(updateActiveNav, 100));
    }

    function handleNavClick(event) {
        event.preventDefault();
        
        const targetId = event.target.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);
        
        if (targetElement) {
            smoothScrollTo(targetElement);
            
            // Update active state
            updateActiveNavLink(event.target);
            
            // Analytics tracking
            if (typeof gtag !== 'undefined') {
                gtag('event', 'navigation', {
                    'event_category': 'CV',
                    'event_label': targetId
                });
            }
        }
    }

    function smoothScrollTo(element) {
        const targetPosition = element.offsetTop - CONFIG.SCROLL_OFFSET;
        
        window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
        });
    }

    function updateActiveNav() {
        const scrollPosition = window.scrollY + CONFIG.SCROLL_OFFSET;
        
        elements.sections.forEach((section, index) => {
            const sectionTop = section.offsetTop;
            const sectionBottom = sectionTop + section.offsetHeight;
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
                const correspondingNavLink = document.querySelector(`[href="#${section.id}"]`);
                updateActiveNavLink(correspondingNavLink);
            }
        });
    }

    function updateActiveNavLink(activeLink) {
        // Remove active class from all links
        elements.navLinks.forEach(link => {
            link.classList.remove('active');
        });
        
        // Add active class to current link
        if (activeLink) {
            activeLink.classList.add('active');
        }
    }

    // Animation functionality
    function initializeAnimations() {
        // Animate skill bars on scroll
        if (elements.skillBars.length) {
            animateSkillBars();
        }
        
        // Animate language bars on scroll
        if (elements.languageBars.length) {
            animateLanguageBars();
        }
    }

    function animateSkillBars() {
        const skillSection = document.getElementById('habilidades');
        if (!skillSection) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        elements.skillBars.forEach((bar, index) => {
                            setTimeout(() => {
                                const width = bar.style.width || bar.getAttribute('data-width') || '0%';
                                bar.style.width = width;
                                bar.classList.add('animated');
                            }, index * CONFIG.ANIMATION_DELAY);
                        });
                    }, 200);
                    
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: CONFIG.INTERSECTION_THRESHOLD,
            rootMargin: '0px 0px -50px 0px'
        });

        observer.observe(skillSection);
    }

    function animateLanguageBars() {
        const languageSection = document.getElementById('idiomas');
        if (!languageSection) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        elements.languageBars.forEach((bar, index) => {
                            setTimeout(() => {
                                const width = bar.style.width || bar.getAttribute('data-width') || '0%';
                                bar.style.width = width;
                                bar.classList.add('animated');
                            }, index * CONFIG.ANIMATION_DELAY);
                        });
                    }, 200);
                    
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: CONFIG.INTERSECTION_THRESHOLD,
            rootMargin: '0px 0px -50px 0px'
        });

        observer.observe(languageSection);
    }

    // Intersection Observer for section animations
    function initializeIntersectionObserver() {
        const observerOptions = {
            threshold: CONFIG.INTERSECTION_THRESHOLD,
            rootMargin: '0px 0px -20px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    
                    // Animate child elements
                    const animatedElements = entry.target.querySelectorAll(
                        '.experience-item, .project-item, .cert-item, .contact-item, .education-item'
                    );
                    
                    animatedElements.forEach((el, index) => {
                        setTimeout(() => {
                            el.classList.add('fade-in');
                        }, index * 100);
                    });
                }
            });
        }, observerOptions);

        // Observe all sections
        elements.sections.forEach(section => {
            observer.observe(section);
        });
    }

    // Accessibility enhancements
    function initializeAccessibility() {
        // Skip to main content link
        addSkipLink();
        
        // Keyboard navigation
        initializeKeyboardNavigation();
        
        // Focus management
        initializeFocusManagement();
        
        // Screen reader announcements
        initializeScreenReaderSupport();
    }

    function addSkipLink() {
        const skipLink = document.createElement('a');
        skipLink.href = '#perfil';
        skipLink.className = 'skip-link';
        skipLink.textContent = 'Ir al contenido principal';
        skipLink.setAttribute('aria-label', 'Ir al contenido principal del CV');
        
        document.body.insertBefore(skipLink, document.body.firstChild);
    }

    function initializeKeyboardNavigation() {
        document.addEventListener('keydown', (event) => {
            // Escape key closes any open modals/notifications
            if (event.key === 'Escape') {
                closeNotifications();
            }
            
            // Ctrl/Cmd + P for print
            if ((event.ctrlKey || event.metaKey) && event.key === 'p') {
                event.preventDefault();
                handlePrint(event);
            }
            
            // Ctrl/Cmd + D for download
            if ((event.ctrlKey || event.metaKey) && event.key === 'd') {
                event.preventDefault();
                handleDownload(event);
            }
        });
    }

    function initializeFocusManagement() {
        // Ensure proper focus indicators
        document.addEventListener('mousedown', () => {
            document.body.classList.add('using-mouse');
        });
        
        document.addEventListener('keydown', (event) => {
            if (event.key === 'Tab') {
                document.body.classList.remove('using-mouse');
            }
        });
    }

    function initializeScreenReaderSupport() {
        // Add ARIA live region for notifications
        const liveRegion = document.createElement('div');
        liveRegion.setAttribute('aria-live', 'polite');
        liveRegion.setAttribute('aria-atomic', 'true');
        liveRegion.className = 'sr-only';
        liveRegion.id = 'live-region';
        document.body.appendChild(liveRegion);
    }

    // Notification system
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.setAttribute('role', 'alert');
        notification.setAttribute('aria-live', 'assertive');
        
        // Add close button
        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '&times;';
        closeBtn.className = 'notification-close';
        closeBtn.setAttribute('aria-label', 'Cerrar notificación');
        closeBtn.addEventListener('click', () => closeNotification(notification));
        notification.appendChild(closeBtn);
        
        // Position and show
        document.body.appendChild(notification);
        
        // Auto-close after 5 seconds
        setTimeout(() => {
            closeNotification(notification);
        }, 5000);
        
        // Announce to screen readers
        announceToScreenReader(message);
    }

    function closeNotification(notification) {
        if (notification && notification.parentNode) {
            notification.classList.add('closing');
            setTimeout(() => {
                notification.parentNode.removeChild(notification);
            }, 300);
        }
    }

    function closeNotifications() {
        const notifications = document.querySelectorAll('.notification');
        notifications.forEach(closeNotification);
    }

    function announceToScreenReader(message) {
        const liveRegion = document.getElementById('live-region');
        if (liveRegion) {
            liveRegion.textContent = message;
            setTimeout(() => {
                liveRegion.textContent = '';
            }, 1000);
        }
    }

    // Utility functions
    function throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    function debounce(func, wait, immediate) {
        let timeout;
        return function executedFunction() {
            const context = this;
            const args = arguments;
            const later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    }

    // Export for external use
    window.CVProfessional = {
        showNotification,
        downloadCV: handleDownload,
        printCV: handlePrint,
        scrollToSection: (sectionId) => {
            const section = document.getElementById(sectionId);
            if (section) smoothScrollTo(section);
        }
    };

    // Analytics integration
    function trackEvent(action, category = 'CV', label = '') {
        if (typeof gtag !== 'undefined') {
            gtag('event', action, {
                'event_category': category,
                'event_label': label
            });
        }
    }

    // Performance monitoring
    function measurePerformance() {
        if ('performance' in window) {
            window.addEventListener('load', () => {
                setTimeout(() => {
                    const perfData = performance.timing;
                    const loadTime = perfData.loadEventEnd - perfData.navigationStart;
                    console.log(`⚡ CV loaded in ${loadTime}ms`);
                    
                    if (loadTime > 3000) {
                        console.warn('🐌 Slow page load detected');
                    }
                }, 0);
            });
        }
    }

    // Initialize performance monitoring
    measurePerformance();

})();

// Additional CSS classes for animations (to be added to CSS)
const additionalStyles = `
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--cv-primary);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: var(--cv-shadow-lg);
        z-index: 1000;
        animation: slideIn 0.3s ease;
        max-width: 400px;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .notification-success {
        background: var(--cv-secondary);
    }
    
    .notification-error {
        background: var(--error);
    }
    
    .notification-close {
        background: none;
        border: none;
        color: white;
        font-size: 1.5rem;
        cursor: pointer;
        padding: 0;
        line-height: 1;
    }
    
    .notification.closing {
        animation: slideOut 0.3s ease forwards;
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .skip-link {
        position: absolute;
        top: -40px;
        left: 6px;
        background: var(--cv-primary);
        color: white;
        padding: 8px;
        text-decoration: none;
        border-radius: 4px;
        z-index: 1001;
        transition: top 0.3s;
    }
    
    .skip-link:focus {
        top: 6px;
    }
    
    .sr-only {
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border: 0;
    }
    
    .using-mouse *:focus {
        outline: none;
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease forwards;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .cv-section {
        opacity: 0;
        transition: opacity 0.6s ease;
    }
    
    .cv-section.visible {
        opacity: 1;
    }
    
    .cv-navigation a.active {
        background: rgba(255, 255, 255, 0.3);
        color: white;
    }
`;

// Inject additional styles
if (typeof document !== 'undefined') {
    const styleSheet = document.createElement('style');
    styleSheet.textContent = additionalStyles;
    document.head.appendChild(styleSheet);
}
