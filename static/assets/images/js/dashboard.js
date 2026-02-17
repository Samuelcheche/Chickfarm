document.addEventListener('DOMContentLoaded', function() {
    // Check authentication
    const user = localStorage.getItem('currentUser');
    if (!user) {
        window.location.href = 'index.html';
        return;
    }

    const userData = JSON.parse(user);

    // Update welcome message
    const welcomeMessage = document.querySelector('.dashboard-header p.text-secondary');
    if (welcomeMessage) {
        welcomeMessage.textContent = `Welcome back, ${userData.email}`;
    }

    // Setup logout functionality
    const logoutButton = document.querySelector('a[href="#logout"]');
    if (logoutButton) {
        logoutButton.addEventListener('click', function(e) {
            e.preventDefault();
            localStorage.removeItem('currentUser');
            window.location.href = 'index.html';
        });
    }

    // Initialize dashboard components
    initializeDashboard();
});

function initializeDashboard() {
    // Example data - In a real application, this would come from a backend API
    const dashboardData = {
        totalOrders: 156,
        revenue: 45290,
        activeOrders: 12,
        customerRating: 4.8,
        recentOrders: [
            { id: 'ORD-2589', customer: 'Alice Wanjiru', product: 'Medium Egg Tray', amount: 350, status: 'Delivered' },
            { id: 'ORD-2588', customer: 'James Omondi', product: 'Large Egg Tray', amount: 420, status: 'Processing' },
            { id: 'ORD-2587', customer: 'Sarah Muthoni', product: 'Small Egg Tray', amount: 180, status: 'In Transit' },
            // Add more orders as needed
        ],
        recentActivity: [
            { type: 'delivery', message: 'Order #ORD-2589 has been successfully delivered to Alice Wanjiru', time: '2 minutes ago' },
            { type: 'shipping', message: 'Order #ORD-2587 has been picked up by delivery partner', time: '1 hour ago' },
            // Add more activities as needed
        ]
    };

    // Update stats cards with real data
    updateStatsCards(dashboardData);

    // Setup event listeners for dashboard actions
    setupDashboardActions();
}

function updateStatsCards(data) {
    // Update total orders
    document.querySelector('.stat-card:nth-child(1) h3').textContent = data.totalOrders;
    
    // Update revenue
    document.querySelector('.stat-card:nth-child(2) h3').textContent = `KSh ${data.revenue}`;
    
    // Update active orders
    document.querySelector('.stat-card:nth-child(3) h3').textContent = data.activeOrders;
    
    // Update customer rating
    document.querySelector('.stat-card:nth-child(4) h3').textContent = `${data.customerRating}/5.0`;
}

function setupDashboardActions() {
    // Export Data button
    const exportBtn = document.querySelector('button.btn-farm-green i.fa-download').parentElement;
    if (exportBtn) {
        exportBtn.addEventListener('click', function() {
            // Implement export functionality
            alert('Exporting data...');
        });
    }

    // New Order button
    const newOrderBtn = document.querySelector('button.btn-farm-yellow i.fa-plus').parentElement;
    if (newOrderBtn) {
        newOrderBtn.addEventListener('click', function() {
            // Implement new order functionality
            window.location.href = 'products.html';
        });
    }

    // Order detail buttons
    const detailBtns = document.querySelectorAll('button.btn-sm.btn-farm-green');
    detailBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const orderId = this.closest('tr').querySelector('td:first-child').textContent;
            // Implement order detail view
            alert(`Viewing details for order ${orderId}`);
        });
    });
}