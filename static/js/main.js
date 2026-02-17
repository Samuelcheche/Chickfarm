// Main JavaScript File for Nyandiwa Smart Poultry Connect

// Back to Top Button
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
    
    // Form Validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Navbar smooth active link
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // Close mobile menu on link click
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth < 992) {
                navbarToggler?.click();
            }
        });
    });
    
    // Add to Cart functionality
    const addToCartButtons = document.querySelectorAll('.btn-farm-green, .btn-farm-yellow');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (this.textContent.includes('Add to Cart')) {
                e.preventDefault();
                // Simple notification
                const notification = document.createElement('div');
                notification.className = 'alert alert-success alert-dismissible fade show';
                notification.setAttribute('role', 'alert');
                notification.innerHTML = `
                    <strong>Success!</strong> Item added to cart.
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                `;
                document.body.insertBefore(notification, document.body.firstChild);
                
                // Auto-dismiss after 3 seconds
                setTimeout(() => {
                    notification.remove();
                }, 3000);
            }
        });
    });
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Carousel auto-play
    const carouselElement = document.getElementById('heroCarousel');
    if (carouselElement) {
        new bootstrap.Carousel(carouselElement, {
            interval: 4000,
            wrap: true
        });
    }
    
    // Intersection Observer for scroll animations
    const observerElements = document.querySelectorAll('.hover-lift, .product-card, .card');
    const elementObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'slideInUp 0.6s ease forwards';
                elementObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
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
                    imageObserver.unobserve(img);
                }
            });
        });
        images.forEach(img => imageObserver.observe(img));
    }
    
    // Handle modal forms
    const loginModal = document.getElementById('loginModal');
    const registerModal = document.getElementById('registerModal');
    
    loginModal?.addEventListener('hidden.bs.modal', function() {
        this.querySelector('form')?.reset();
        this.classList.remove('was-validated');
    });
    
    registerModal?.addEventListener('hidden.bs.modal', function() {
        this.querySelector('form')?.reset();
        this.classList.remove('was-validated');
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
    
    console.log('Nyandiwa Smart Poultry - App Loaded Successfully');
});
