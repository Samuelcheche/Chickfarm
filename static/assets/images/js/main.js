// Main JavaScript for Nyandiwa Smart Poultry Connect

document.addEventListener('DOMContentLoaded', function() {
    // Enable all tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Enable all popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Handle active navigation state
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });

    // Smooth scrolling for anchor links
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

    // Form validation
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

    // Back to top button
    const backToTopButton = document.getElementById('backToTop');
    if (backToTopButton) {
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 100) {
                backToTopButton.classList.add('show');
            } else {
                backToTopButton.classList.remove('show');
            }
        });

        backToTopButton.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // Page-specific functionality
    const pageSpecificInit = {
        'delivery.html': initDeliveryPage,
        'dashboard.html': initDashboardPage,
        'products.html': initProductsPage
    };

    if (pageSpecificInit[currentPage]) {
        pageSpecificInit[currentPage]();
    }
});

// Delivery page initialization
function initDeliveryPage() {
    const calculatorForm = document.getElementById('deliveryCalculator');
    if (calculatorForm) {
        calculatorForm.addEventListener('submit', function(e) {
            e.preventDefault();
            calculateDeliveryCost();
        });
    }
}

// Dashboard page initialization
function initDashboardPage() {
    // Initialize charts and data tables
    initializeCharts();
    initializeTables();
}

// Products page initialization
function initProductsPage() {
    // Initialize product filters and sorting
    initializeFilters();
    initializeCart();
}

// Utility functions
function calculateDeliveryCost() {
    const location = document.getElementById('deliveryLocation').value;
    // Simulated calculation - replace with actual API call
    const distance = Math.floor(Math.random() * 20) + 1;
    const cost = distance * 50;
    
    document.getElementById('estimatedDistance').textContent = distance + ' km';
    document.getElementById('deliveryCost').textContent = 'KSh ' + cost;
}

function initializeCharts() {
    // Add chart initialization code here
    // Using Chart.js or similar library
}

function initializeTables() {
    // Add data table initialization code here
}

function initializeFilters() {
    // Add product filtering code here
}

function initializeCart() {
    // Add shopping cart functionality here
}

// Loading state handler
function showLoading(element) {
    element.classList.add('loading');
    element.setAttribute('disabled', true);
}

function hideLoading(element) {
    element.classList.remove('loading');
    element.removeAttribute('disabled');
}