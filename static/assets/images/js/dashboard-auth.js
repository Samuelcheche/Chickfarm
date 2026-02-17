console.log('Dashboard auth script loaded'); // Debug log

// Check if user is authenticated before allowing access to dashboard
document.addEventListener('DOMContentLoaded', function() {
    console.log('Checking dashboard access...'); // Debug log
    
    const user = localStorage.getItem('currentUser');
    console.log('User data:', user); // Debug log
    
    if (!user) {
        console.log('No user found, redirecting to login...'); // Debug log
        // User is not logged in, redirect to home page
        window.location.href = 'index.html';
        return;
    }

    // User is logged in, show dashboard content
    const userData = JSON.parse(user);
    console.log('User authenticated:', userData); // Debug log
    
    // Update navigation to show logged-in state
    updateUIForLoggedInUser(userData);
    
    // Show dashboard content
    const dashboardContent = document.querySelector('.dashboard-content');
    if (dashboardContent) {
        dashboardContent.style.display = 'block';
    }
});