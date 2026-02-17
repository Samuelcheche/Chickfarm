// Authentication JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Handle login form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = document.getElementById('loginEmail')?.value;
            const password = document.getElementById('loginPassword')?.value;
            
            if (email && password) {
                // Validate email format
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(email)) {
                    alert('Please enter a valid email address');
                    return;
                }
                
                // Show loading state
                const submitButton = this.querySelector('button[type="submit"]');
                const originalText = submitButton.textContent;
                submitButton.disabled = true;
                submitButton.textContent = 'Logging in...';
                
                // Simulate API call (replace with actual authentication)
                setTimeout(() => {
                    // In a real application, you would make an AJAX request here
                    console.log('Login attempt:', email);
                    alert('Login successful! Redirecting to dashboard...');
                    // window.location.href = '/dashboard/';
                    submitButton.disabled = false;
                    submitButton.textContent = originalText;
                }, 1500);
            }
        });
    }
    
    // Handle registration form
    const registerForms = document.querySelectorAll('form.needs-validation');
    registerForms.forEach(form => {
        if (form.querySelector('input[type="password"]')) {
            form.addEventListener('submit', function(e) {
                if (!this.checkValidity()) {
                    e.preventDefault();
                    e.stopPropagation();
                }
                
                const password = this.querySelector('input[type="password"]')?.value;
                const confirmPassword = this.querySelectorAll('input[type="password"]')[1]?.value;
                
                if (password && confirmPassword && password !== confirmPassword) {
                    e.preventDefault();
                    alert('Passwords do not match');
                    return;
                }
                
                this.classList.add('was-validated');
            });
        }
    });
    
    // Password visibility toggle
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(input => {
        const wrapper = input.parentElement;
        const toggleButton = document.createElement('button');
        toggleButton.type = 'button';
        toggleButton.className = 'btn btn-link text-muted';
        toggleButton.innerHTML = '<i class="fas fa-eye"></i>';
        toggleButton.style.position = 'absolute';
        toggleButton.style.right = '10px';
        toggleButton.style.top = '50%';
        toggleButton.style.transform = 'translateY(-50%)';
        
        wrapper.style.position = 'relative';
        wrapper.appendChild(toggleButton);
        
        toggleButton.addEventListener('click', function(e) {
            e.preventDefault();
            input.type = input.type === 'password' ? 'text' : 'password';
            toggleButton.innerHTML = input.type === 'password' ? 
                '<i class="fas fa-eye"></i>' : 
                '<i class="fas fa-eye-slash"></i>';
        });
    });
    
    // Check if user is logged in (placeholder)
    function checkAuthStatus() {
        // This would check with your backend if user is authenticated
        const isAuthenticated = localStorage.getItem('userToken');
        return !!isAuthenticated;
    }
    
    console.log('Auth module loaded');
});
