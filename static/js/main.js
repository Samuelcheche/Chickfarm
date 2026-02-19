// Main JavaScript File for Nyandiwa Smart Poultry Connect

// Back to Top Button with smooth scroll
document.addEventListener('DOMContentLoaded', function() {
    const backToTopButton = document.getElementById('backToTop');
    
    // Show/hide back to top button
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopButton?.classList.add('show');
        } else {
            backToTopButton?.classList.remove('show');
        }
    });
    
    // Smooth scroll to top
    backToTopButton?.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // Form Validation with better feedback
    const forms = document.querySelectorAll('.needs-validation, form');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                showNotification('Please fill in all required fields', 'warning');
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Navbar smooth active link and mobile menu close
    const navLinks = document.querySelectorAll('.nav-link');
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            // Update active state
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            
            // Close mobile menu
            if (window.innerWidth < 992 && navbarCollapse?.classList.contains('show')) {
                navbarToggler?.click();
            }
        });
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#' && document.querySelector(href)) {
                e.preventDefault();
                const target = document.querySelector(href);
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Initialize tooltips and popovers
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Carousel auto-play with enhanced settings
    const carouselElement = document.getElementById('heroCarousel');
    if (carouselElement) {
        new bootstrap.Carousel(carouselElement, {
            interval: 5000,
            pause: 'hover',
            wrap: true,
            touch: true
        });
    }
    
    // Intersection Observer for scroll animations
    const observerElements = document.querySelectorAll('.hover-lift, .product-card, .card, .feature-card');
    const elementObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'slideInUp 0.6s ease forwards';
                entry.target.style.opacity = '1';
                elementObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    observerElements.forEach(element => {
        element.style.opacity = '0';
        elementObserver.observe(element);
    });
    
    // Lazy load images
    if ('IntersectionObserver' in window) {
        const images = document.querySelectorAll('img[data-src]');
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    img.style.animation = 'fadeIn 0.5s ease';
                    imageObserver.unobserve(img);
                }
            });
        });
        images.forEach(img => imageObserver.observe(img));
    }
    
    // Modal form handling
    const loginModal = document.getElementById('loginModal');
    const registerModal = document.getElementById('registerModal');
    const paymentModal = document.getElementById('paymentModal');
    
    [loginModal, registerModal, paymentModal].forEach(modal => {
        if (modal) {
            modal.addEventListener('hidden.bs.modal', function() {
                this.querySelector('form')?.reset();
                this.classList.remove('was-validated');
            });
        }
    });
    
    // Add ripple effect to buttons
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            ripple.className = 'ripple';
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    });
    
    // Show notifications
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        const timeout = alert.classList.contains('alert-danger') ? 10000 : 5000;
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, timeout);
    });
    
    // Loading state for form submissions
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const form = this.closest('form');
            if (form && form.checkValidity() === false) {
                return;
            }
            this.disabled = true;
            const originalText = this.textContent;
            this.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
            
            // Re-enable after submission (or timeout)
            setTimeout(() => {
                this.disabled = false;
                this.textContent = originalText;
            }, 30000);
        });
    });
    
    console.log('Nyandiwa Smart Poultry - App Loaded Successfully ✓');
});

// Global notification function
function showNotification(message, type = 'info') {
    const alertHTML = `
        <div class="alert alert-${type} alert-dismissible fade show shadow-sm" role="alert" style="position: fixed; top: 20px; right: 20px; z-index: 9999; min-width: 300px; animation: slideInRight 0.3s ease;">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', alertHTML);
    
    // Auto-dismiss
    setTimeout(() => {
        const alert = document.querySelector('.alert:last-of-type');
        if (alert) {
            new bootstrap.Alert(alert).close();
        }
    }, 5000);
}
