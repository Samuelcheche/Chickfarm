from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
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
    recent_orders = order.objects.select_related('customer', 'product').order_by('-order_date')[:5]
    return render(request, 'dashboard.html', {
        'recent_orders': recent_orders,
    })

def products(request):
    return render(request, 'products.html')

def orders(request):
    if request.method == 'POST':
        action = request.POST.get('action', 'create_order')

        if action == 'create_customer':
            name = request.POST.get('name', '').strip()
            surname = request.POST.get('surname', '').strip()
            email = request.POST.get('email', '').strip().lower()
            password = request.POST.get('password', '').strip()
            phone = request.POST.get('phone', '').strip()
            location = request.POST.get('location', '').strip()
            message = request.POST.get('message', '').strip()

            if not all([name, surname, email, password, phone, location]):
                messages.error(request, 'Please fill in all required customer fields.')
                return redirect('orders')

            if customer.objects.filter(email=email).exists():
                messages.error(request, 'A customer with that email already exists.')
                return redirect('orders')

            customer.objects.create(
                name=name,
                surname=surname,
                email=email,
                password=make_password(password),
                phone=phone,
                location=location,
                message=message,
            )
            messages.success(request, 'Customer created successfully.')
            return redirect('orders')

        if action != 'create_order':
            messages.error(request, 'Unknown action.')
            return redirect('orders')

        customer_id = request.POST.get('customer')
        product_id = request.POST.get('product')
        trays_raw = request.POST.get('number_of_trays')
        status = request.POST.get('status', order.STATUS_PROCESSING)

        try:
            trays = int(trays_raw)
        except (TypeError, ValueError):
            trays = 0

        if trays <= 0:
            messages.error(request, 'Please enter a valid number of trays.')
            return redirect('orders')

        selected_customer = get_object_or_404(customer, pk=customer_id)
        selected_product = get_object_or_404(product, pk=product_id)

        order.objects.create(
            customer=selected_customer,
            product=selected_product,
            number_of_trays=trays,
            status=status,
        )
        messages.success(request, 'Order created successfully.')
        return redirect('orders')

    all_orders = order.objects.select_related('customer', 'product').order_by('-order_date')
    all_customers = customer.objects.order_by('name', 'surname')
    all_products = product.objects.filter(is_active=True).order_by('name')
    return render(request, 'order.html', {
        'orders': all_orders,
        'customers': all_customers,
        'products': all_products,
        'status_choices': order.STATUS_CHOICES,
    })

def register(request):
    """ Show the registration form """
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        # Validate inputs
        if not email or not password:
            messages.error(request, "Email and password are required")
            return render(request, 'register.html')

        # Check the password
        if password == confirm_password:
            try:
                # Check if user already exists
                if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
                    messages.error(request, "Email already exists")
                else:
                    user = User.objects.create_user(username=email, email=email, password=password)
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
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')

        # Validate inputs
        if not email or not password:
            messages.error(request, "Email and password are required")
            return render(request, 'login.html')

        # Authenticate user
        user = authenticate(request, username=email, password=password)

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
            messages.error(request, "Invalid email or password. Please try again.")

    return render(request, 'login.html')