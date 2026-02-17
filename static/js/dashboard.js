// Dashboard JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize dashboard functionality
    
    // Export data functionality
    const exportButtons = document.querySelectorAll('[data-action="export"]');
    exportButtons.forEach(button => {
        button.addEventListener('click', function() {
            alert('Export functionality will be implemented soon');
        });
    });
    
    // New Order button
    const newOrderButton = document.querySelector('.btn-farm-yellow');
    if (newOrderButton && newOrderButton.textContent.includes('New Order')) {
        newOrderButton.addEventListener('click', function() {
            // Redirect to products page
            window.location.href = '/products/';
        });
    }
    
    // Order status updates
    const statusBadges = document.querySelectorAll('.badge');
    statusBadges.forEach(badge => {
        if (badge.textContent.includes('Pending')) {
            badge.classList.add('bg-warning');
        } else if (badge.textContent.includes('Completed')) {
            badge.classList.add('bg-success');
        } else if (badge.textContent.includes('Failed')) {
            badge.classList.add('bg-danger');
        }
    });
    
    // Sidebar toggle on mobile
    const sidebar = document.querySelector('.sidebar');
    const sidebarToggle = document.querySelector('[data-bs-toggle="offcanvas"]');
    
    if (sidebar && window.innerWidth < 768) {
        sidebarToggle?.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });
    }
    
    console.log('Dashboard initialized');
});
