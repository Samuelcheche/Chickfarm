// Mock user data (Replace this with actual backend authentication)
const mockUsers = [
    {
        email: 'admin@example.com',
        password: 'admin123', // In real application, passwords should be hashed
        role: 'admin'
    },
    {
        email: 'user@example.com',
        password: 'user123',
        role: 'user'
    }
];

// Check if user is logged in
function checkAuthStatus() {
    const user = localStorage.getItem('currentUser'); // Changed to localStorage for persistence
    if (user) {
        // User is logged in
        const userData = JSON.parse(user);
        updateUIForLoggedInUser(userData);
        return userData;
    }
    return null;
}

// Update UI elements based on login status
function updateUIForLoggedInUser(userData) {
    const loginBtn = document.querySelector('[data-bs-target="#loginModal"]');
    const registerBtn = document.querySelector('[data-bs-target="#registerModal"]');
    
    if (loginBtn && registerBtn) {
        // Replace login/register buttons with user menu
        const parentDiv = loginBtn.parentElement;
        parentDiv.innerHTML = `
            <div class="dropdown">
                <button class="btn btn-farm-green dropdown-toggle" type="button" id="userMenuButton" data-bs-toggle="dropdown" aria-expanded="false">
                    <i class="fas fa-user-circle me-2"></i>${userData.email}
                </button>
                <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userMenuButton">
                    <li><a class="dropdown-item" href="dashboard.html"><i class="fas fa-chart-bar me-2"></i>Dashboard</a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="#" onclick="logout(); return false;"><i class="fas fa-sign-out-alt me-2"></i>Logout</a></li>
                </ul>
            </div>
        `;
    }
}

// Handle login form submission
document.addEventListener('DOMContentLoaded', function() {
    // Check auth status on page load
    checkAuthStatus();

    // Setup login form handler
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;
            
            // In a real application, this would be an API call
            const user = mockUsers.find(u => u.email === email && u.password === password);
            
            if (user) {
                // Store user data in session storage
                const userData = {
                    email: user.email,
                    role: user.role
                };
                sessionStorage.setItem('currentUser', JSON.stringify(userData));
                
                // Close the login modal
                const loginModal = bootstrap.Modal.getInstance(document.getElementById('loginModal'));
                loginModal.hide();
                
                // Update UI
                updateUIForLoggedInUser(userData);
                
                // Redirect to dashboard if on index page
                if (window.location.pathname.includes('index.html') || window.location.pathname === '/') {
                    window.location.href = 'dashboard.html';
                }
            } else {
                // Show error message
                alert('Invalid email or password. For testing, use:\nEmail: admin@example.com\nPassword: admin123');
            }
        });
    }
});

// Handle logout
function logout() {
    // Clear session storage
    sessionStorage.removeItem('currentUser');
    // Redirect to home page if on dashboard
    if (window.location.pathname.includes('dashboard.html')) {
        window.location.href = 'index.html';
    } else {
        // Reload current page to reset UI
        window.location.reload();
    }
}