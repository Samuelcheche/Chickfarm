from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from chickapp.models import *
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def delivery(request):
    return render(request, 'delivery.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def products(request):
    return render(request, 'products.html')

def register(request):
    """ Show the registration form """
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        # Validate inputs
        if not username or not password:
            messages.error(request, "Username and password are required")
            return render(request, 'register.html')

        # Check the password
        if password == confirm_password:
            try:
                # Check if user already exists
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Username already exists")
                else:
                    user = User.objects.create_user(username=username, password=password)
                    messages.success(request, "Account created successfully! Please login.")
                    return redirect('/login')
            except Exception as e:
                logger.error(f"Registration error: {str(e)}")
                messages.error(request, "An error occurred during registration")
        else:
            # Display a message saying passwords don't match
            messages.error(request, "Passwords do not match")

    return render(request, 'register.html')

   
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Validate inputs
        if not username or not password:
            messages.error(request, "Username and password are required")
            return render(request, 'login.html')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        # Check if the user exists
        if user is not None:
            login(request, user)
            messages.success(request, "You are now logged in!")
            # Admin
            if user.is_superuser:
                return redirect('/appointment')

            # For Normal Users
            return redirect('/index')
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, 'login.html')