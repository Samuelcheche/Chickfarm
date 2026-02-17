// Dashboard Authentication JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Check if user is authenticated
    const isAuthenticated = localStorage.getItem('userToken');
    
    // If accessing dashboard without authentication, redirect to login
    if (window.location.pathname === '/dashboard/' && !isAuthenticated) {
        // Uncomment to enforce authentication
        // window.location.href = '/';
        console.log('Dashboard access detected - authentication check performed');
    }
    
    // Logout functionality
    const logoutButton = document.querySelector('[data-action="logout"]');
    if (logoutButton) {
        logoutButton.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Clear user data
            localStorage.removeItem('userToken');
            localStorage.removeItem('userData');
            
            // Show logout message
            alert('You have been logged out successfully');
            window.location.href = '/';
        });
    }
    
    // User profile menu
    const userMenu = document.querySelector('.user-menu');
    if (userMenu) {
        userMenu.addEventListener('click', function() {
            this.classList.toggle('active');
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.user-menu')) {
                userMenu.classList.remove('active');
            }
        });
    }
    
    // Dashboard quick actions
    const quickActionButtons = document.querySelectorAll('[data-action]');
    quickActionButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const action = this.getAttribute('data-action');
            handleDashboardAction(action);
        });
    });
    
    function handleDashboardAction(action) {
        switch(action) {
            case 'view-orders':
                console.log('Viewing orders');
                // Redirect to orders view
                window.location.href = '#orders';
                break;
            case 'manage-account':
                console.log('Managing account');
                window.location.href = '#account';
                break;
            case 'view-stats':
                console.log('Viewing statistics');
                window.location.href = '#stats';
                break;
            default:
                console.log('Action:', action);
        }
    }
    
    // Auto-refresh dashboard data
    const refreshInterval = setInterval(function() {
        // In a real application, this would fetch updated data from the server
        console.log('Refreshing dashboard data...');
    }, 30000); // Refresh every 30 seconds
    
    // Cleanup on page unload
    window.addEventListener('beforeunload', function() {
        clearInterval(refreshInterval);
    });
    
    console.log('Dashboard auth module loaded');
});
