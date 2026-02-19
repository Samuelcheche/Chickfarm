from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from chickapp.models import *
from django.contrib import messages
from django.db.utils import OperationalError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q
from datetime import timedelta
from django.utils import timezone
import json
import logging
from chickapp.mpesa import initiate_mpesa_payment

logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    """Home page view with modern UI"""
    context = {
        'page_title': 'Home - Nyandiwa Smart Poultry',
        'user_authenticated': request.user.is_authenticated,
    }
    return render(request, 'index_new.html', context)

def about(request):
    return render(request, 'about.html')

def delivery(request):
    return render(request, 'delivery.html')

def dashboard(request):
    """Admin dashboard with orders, stats, and analytics"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Redirect non-admin users to products page
    if not request.user.is_superuser and not request.user.is_staff:
        return redirect('products')
    
    recent_orders = []
    db_error = None
    total_orders = 0
    total_revenue = 0
    processing_orders = 0
    delivered_orders = 0

    try:
        # Fetch recent orders
        recent_orders = list(
            order.objects.select_related('customer', 'product').order_by('-order_date')[:5]
        )
        
        # Get statistics
        total_orders = order.objects.filter(status=order.STATUS_DELIVERED).count()
        
        # Calculate revenue from delivered orders only
        revenue_data = order.objects.filter(
            status=order.STATUS_DELIVERED
        ).aggregate(total=Sum('amount'))
        total_revenue = revenue_data['total'] or 0
        
        # Get processing orders
        processing_orders = order.objects.filter(
            status=order.STATUS_PROCESSING
        ).count()
        
        # Get delivered orders
        delivered_orders = order.objects.filter(
            status=order.STATUS_DELIVERED
        ).count()
        
        # Calculate percentage change (last 7 days vs previous 7 days)
        today = timezone.now()
        week_ago = today - timedelta(days=7)
        two_weeks_ago = today - timedelta(days=14)
        
        current_week_orders = order.objects.filter(
            order_date__gte=week_ago,
            status=order.STATUS_DELIVERED
        ).count()
        
        previous_week_orders = order.objects.filter(
            order_date__gte=two_weeks_ago,
            order_date__lt=week_ago,
            status=order.STATUS_DELIVERED
        ).count()
        
        order_growth = 0
        if previous_week_orders > 0:
            order_growth = round(((current_week_orders - previous_week_orders) / previous_week_orders) * 100, 1)
        
        # Calculate revenue growth
        current_week_revenue = order.objects.filter(
            order_date__gte=week_ago,
            status=order.STATUS_DELIVERED
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        previous_week_revenue = order.objects.filter(
            order_date__gte=two_weeks_ago,
            order_date__lt=week_ago,
            status=order.STATUS_DELIVERED
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        revenue_growth = 0
        if previous_week_revenue > 0:
            revenue_growth = round(((current_week_revenue - previous_week_revenue) / previous_week_revenue) * 100, 1)
        
    except OperationalError:
        db_error = 'Order data is unavailable. Run migrations to create required tables.'
    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        db_error = f'An error occurred loading dashboard data: {str(e)}'

    return render(request, 'dashboard.html', {
        'recent_orders': recent_orders,
        'db_error': db_error,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'processing_orders': processing_orders,
        'delivered_orders': delivered_orders,
        'order_growth': order_growth,
        'revenue_growth': revenue_growth,
    })

def products(request):
    """Display available products for purchase - requires authentication"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    all_products = []
    db_error = None
    
    try:
        all_products = product.objects.filter(is_active=True)
    except OperationalError:
        db_error = 'Products are temporarily unavailable. Please try again later.'
    except Exception as e:
        logger.error(f"Products view error: {str(e)}")
        db_error = f'An error occurred loading products: {str(e)}'
    
    return render(request, 'products.html', {
        'all_products': all_products,
        'db_error': db_error,
    })

def orders(request):
    """Orders management view - requires authentication"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    db_error = None
    all_orders = []
    all_customers = []
    all_products = []
    status_choices = []

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

            try:
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
            except OperationalError:
                messages.error(request, 'Cannot create customer. Database tables are missing.')
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

        try:
            selected_customer = get_object_or_404(customer, pk=customer_id)
            selected_product = get_object_or_404(product, pk=product_id)

            order.objects.create(
                customer=selected_customer,
                product=selected_product,
                number_of_trays=trays,
                status=status,
            )
            messages.success(request, 'Order created successfully.')
        except OperationalError:
            messages.error(request, 'Cannot create order. Database tables are missing.')
        return redirect('orders')

    try:
        all_orders = list(order.objects.select_related('customer', 'product').order_by('-order_date'))
        all_customers = list(customer.objects.order_by('name', 'surname'))
        all_products = list(product.objects.filter(is_active=True).order_by('name'))
        status_choices = order.STATUS_CHOICES
    except OperationalError:
        db_error = 'Order system is unavailable. Run migrations to create required tables.'

    return render(request, 'order.html', {
        'orders': all_orders,
        'customers': all_customers,
        'products': all_products,
        'status_choices': status_choices,
        'db_error': db_error,
    })

def register(request):
    """User registration view with enhanced validation and modern UI"""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        fullname = request.POST.get('fullname', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        terms_agreed = request.POST.get('terms') == 'on' or request.POST.get('terms') == True

        # Validate inputs
        validation_errors = []
        
        if not fullname:
            validation_errors.append('Full name is required')
        elif len(fullname) < 2:
            validation_errors.append('Full name must be at least 2 characters')
        
        if not email:
            validation_errors.append('Email address is required')
        elif '@' not in email or '.' not in email:
            validation_errors.append('Please enter a valid email address')
        
        if not password:
            validation_errors.append('Password is required')
        elif len(password) < 6:
            validation_errors.append('Password must be at least 6 characters')
        
        if password != confirm_password:
            validation_errors.append('Passwords do not match')
        
        if not terms_agreed:
            validation_errors.append('You must agree to the Terms & Conditions')
        
        if validation_errors:
            for error in validation_errors:
                messages.error(request, error)
            return render(request, 'register.html', {'fullname': fullname, 'email': email})

        # Check if user already exists
        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists. Please login or use a different email.')
            return render(request, 'register.html', {'fullname': fullname, 'email': email})

        try:
            # Create new user
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=fullname.split()[0],
                last_name=' '.join(fullname.split()[1:]) if len(fullname.split()) > 1 else '',
            )
            
            # Log the user in immediately after registration
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome {fullname}! Your account has been created successfully.')
                return redirect('products')  # Redirect to products page
            else:
                # If auto-login fails, ask user to login manually
                messages.success(request, 'Account created successfully! Please login with your credentials.')
                return redirect('login')
                
        except Exception as e:
            logger.error(f'Registration error: {str(e)}')
            messages.error(request, 'An unexpected error occurred during registration. Please try again.')
            return render(request, 'register.html', {'fullname': fullname, 'email': email})

    return render(request, 'register.html')

   
def login_user(request):
    """User login view with enhanced validation and modern UI"""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == "POST":
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember', False)

        # Validate inputs
        if not email or not password:
            messages.error(request, 'Email and password are required')
            return render(request, 'login.html', {'email': email})

        # Check email format
        if '@' not in email:
            messages.error(request, 'Please enter a valid email address')
            return render(request, 'login.html', {'email': email})

        # Authenticate user
        user = authenticate(request, username=email, password=password)

        # Check if the user exists
        if user is not None:
            login(request, user)
            
            # Set session timeout based on remember_me
            if remember_me:
                request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days
            
            messages.success(request, f'Welcome back, {user.first_name or email}!')
            
            # Redirect based on user type
            if user.is_superuser or user.is_staff:
                return redirect('dashboard')
            else:
                # Check if user has a next parameter
                next_page = request.GET.get('next', 'products')
                return redirect(next_page)
        else:
            messages.error(request, 'Invalid email or password. Please check and try again.')
            return render(request, 'login.html', {'email': email})

    return render(request, 'login.html')


@login_required(login_url='login')
def logout_user(request):
    """Log out the current user"""
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('index')


@require_http_methods(["POST"])
def process_payment(request):
    """
    Process payment from the payment modal.
    Creates customer and order(s) with payment information.
    """
    try:
        # Get customer information
        customer_name = request.POST.get('customer_name', '').strip()
        customer_email = request.POST.get('customer_email', '').strip()
        customer_phone = request.POST.get('customer_phone', '').strip()
        customer_location = request.POST.get('customer_location', '').strip()
        
        # Get payment information
        payment_method = request.POST.get('payment_method', '')
        order_notes = request.POST.get('order_notes', '').strip()
        
        # Get payment phone based on method
        payment_phone = ''
        if payment_method == 'mpesa':
            payment_phone = request.POST.get('mpesa_phone', '').strip()
        elif payment_method == 'airtel_money':
            payment_phone = request.POST.get('airtel_phone', '').strip()
        else:  # cash
            payment_phone = customer_phone
        
        # Get cart data
        cart_data_str = request.POST.get('cart_data', '[]')
        cart_data = json.loads(cart_data_str)
        
        # Validate inputs
        if not customer_name or not customer_email or not customer_phone or not customer_location:
            return JsonResponse({
                'success': False,
                'message': 'Please fill in all customer information fields.'
            }, status=400)
        
        if not payment_method:
            return JsonResponse({
                'success': False,
                'message': 'Please select a payment method.'
            }, status=400)
        
        if len(cart_data) == 0:
            return JsonResponse({
                'success': False,
                'message': 'Cart is empty. Please add items before checkout.'
            }, status=400)
        
        # Split customer name into name and surname
        name_parts = customer_name.split(' ', 1)
        name = name_parts[0]
        surname = name_parts[1] if len(name_parts) > 1 else ''
        
        # Find or create customer
        try:
            cust = customer.objects.filter(email=customer_email).first()
            if not cust:
                # Create new customer with a default password
                cust = customer.objects.create(
                    name=name,
                    surname=surname,
                    email=customer_email,
                    password=make_password('default123'),  # Default password
                    phone=customer_phone,
                    location=customer_location,
                    message=order_notes
                )
            else:
                # Update existing customer info
                cust.phone = customer_phone
                cust.location = customer_location
                if order_notes:
                    cust.message = order_notes
                cust.save()
        except Exception as e:
            logger.error(f"Error creating/updating customer: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': 'Failed to process customer information.'
            }, status=500)
        
        # Create orders for each cart item
        created_orders = []
        first_order = None
        total_amount = 0
        
        for item in cart_data:
            try:
                # Find the product
                prod = product.objects.filter(name__icontains=item['product']).first()
                
                if not prod:
                    # Create a generic product if not found
                    prod = product.objects.create(
                        name=item['product'],
                        price=item['price'],
                        description=f"Product from cart: {item['product']}"
                    )
                
                # Calculate order amount
                item_amount = float(item['price']) * int(item['count'])
                total_amount += item_amount
                
                # Create order
                new_order = order.objects.create(
                    customer=cust,
                    product=prod,
                    number_of_trays=int(item['count']),
                    amount=item_amount,
                    payment_method=payment_method,
                    payment_status=order.PAYMENT_STATUS_PENDING if payment_method != 'cash' else order.PAYMENT_STATUS_COMPLETED,
                    payment_phone=payment_phone,
                    message=order_notes,
                    status=order.STATUS_PROCESSING
                )
                
                if first_order is None:
                    first_order = new_order
                
                created_orders.append(new_order.order_code)
                
            except Exception as e:
                logger.error(f"Error creating order for item {item['product']}: {str(e)}")
                continue
        
        if len(created_orders) == 0:
            return JsonResponse({
                'success': False,
                'message': 'Failed to create orders. Please try again.'
            }, status=500)
        
        # If payment method is M-Pesa, initiate STK Push
        if payment_method == 'mpesa' and payment_phone and first_order:
            try:
                mpesa_result = initiate_mpesa_payment(
                    phone_number=payment_phone,
                    amount=total_amount,
                    order_code=first_order.order_code,
                    description=f'Payment for {len(created_orders)} order(s)'
                )
                
                if mpesa_result.get('success'):
                    # Save M-Pesa transaction details
                    first_order.mpesa_checkout_request_id = mpesa_result.get('checkout_request_id', '')
                    first_order.mpesa_merchant_request_id = mpesa_result.get('merchant_request_id', '')
                    first_order.payment_reference = mpesa_result.get('checkout_request_id', '')
                    first_order.save()
                    
                    return JsonResponse({
                        'success': True,
                        'message': 'STK Push sent to your phone. Please enter your M-Pesa PIN to complete payment.',
                        'order_code': first_order.order_code,
                        'total_amount': total_amount,
                        'payment_method': payment_method,
                        'mpesa_sent': True
                    })
                else:
                    # M-Pesa failed, but order is created
                    logger.warning(f"M-Pesa STK Push failed: {mpesa_result.get('message')}")
                    return JsonResponse({
                        'success': True,
                        'message': f"Order created but M-Pesa payment failed: {mpesa_result.get('message')}. Please contact us to complete payment.",
                        'order_code': first_order.order_code,
                        'total_amount': total_amount,
                        'payment_method': payment_method,
                        'mpesa_sent': False
                    })
                    
            except Exception as e:
                logger.error(f"M-Pesa initiation error: {str(e)}")
                return JsonResponse({
                    'success': True,
                    'message': f'Order created but M-Pesa payment could not be initiated. Please contact us at +254 725551199.',
                    'order_code': first_order.order_code,
                    'total_amount': total_amount,
                    'payment_method': payment_method,
                    'mpesa_sent': False
                })
        
        # Return success response for non-M-Pesa payments
        return JsonResponse({
            'success': True,
            'message': 'Order(s) placed successfully!',
            'order_code': created_orders[0] if len(created_orders) == 1 else f"{len(created_orders)} orders",
            'total_amount': total_amount,
            'payment_method': payment_method
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid cart data format.'
        }, status=400)
    except Exception as e:
        logger.error(f"Payment processing error: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'An unexpected error occurred. Please try again.'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def mpesa_callback(request):
    """
    M-Pesa callback endpoint to receive payment confirmation
    This endpoint receives STK Push payment results from Safaricom
    """
    try:
        # Parse callback data
        callback_data = json.loads(request.body.decode('utf-8'))
        
        logger.info(f'M-Pesa callback received: {json.dumps(callback_data, indent=2)}')
        
        # Extract data from callback
        stk_callback = callback_data.get('Body', {}).get('stkCallback', {})
        
        merchant_request_id = stk_callback.get('MerchantRequestID')
        checkout_request_id = stk_callback.get('CheckoutRequestID')
        result_code = stk_callback.get('ResultCode')
        result_desc = stk_callback.get('ResultDesc')
        
        # Find the order by checkout request ID
        try:
            order_obj = order.objects.get(mpesa_checkout_request_id=checkout_request_id)
        except order.DoesNotExist:
            logger.error(f'Order not found for CheckoutRequestID: {checkout_request_id}')
            return JsonResponse({
                'ResultCode': 0,
                'ResultDesc': 'Accepted'
            })
        
        # Check if payment was successful
        if result_code == 0:
            # Payment successful
            callback_metadata = stk_callback.get('CallbackMetadata', {}).get('Item', [])
            
            # Extract payment details
            receipt_number = ''
            amount = 0
            phone_number = ''
            transaction_date = ''
            
            for item in callback_metadata:
                name = item.get('Name')
                value = item.get('Value')
                
                if name == 'MpesaReceiptNumber':
                    receipt_number = value
                elif name == 'Amount':
                    amount = value
                elif name == 'PhoneNumber':
                    phone_number = value
                elif name == 'TransactionDate':
                    transaction_date = value
            
            # Update order with payment details
            order_obj.payment_status = order.PAYMENT_STATUS_COMPLETED
            order_obj.mpesa_receipt_number = receipt_number
            order_obj.payment_reference = receipt_number
            order_obj.save()
            
            logger.info(f'Payment successful for order {order_obj.order_code}. Receipt: {receipt_number}')
            
        else:
            # Payment failed or cancelled
            order_obj.payment_status = order.PAYMENT_STATUS_FAILED
            order_obj.message += f'\n\nM-Pesa payment failed: {result_desc}'
            order_obj.save()
            
            logger.warning(f'Payment failed for order {order_obj.order_code}. Reason: {result_desc}')
        
        # Acknowledge receipt of callback
        return JsonResponse({
            'ResultCode': 0,
            'ResultDesc': 'Accepted'
        })
        
    except Exception as e:
        logger.error(f'M-Pesa callback error: {str(e)}')
        return JsonResponse({
            'ResultCode': 1,
            'ResultDesc': 'Failed to process callback'
        })


@require_http_methods(["POST"])
def check_payment_status(request):
    """
    Check M-Pesa payment status for an order
    """
    try:
        order_code = request.POST.get('order_code', '')
        
        if not order_code:
            return JsonResponse({
                'success': False,
                'message': 'Order code is required'
            }, status=400)
        
        # Find the order
        try:
            order_obj = order.objects.get(order_code=order_code)
        except order.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Order not found'
            }, status=404)
        
        # Return payment status
        return JsonResponse({
            'success': True,
            'order_code': order_obj.order_code,
            'payment_status': order_obj.payment_status,
            'payment_method': order_obj.payment_method,
            'amount': str(order_obj.amount),
            'receipt_number': order_obj.mpesa_receipt_number,
            'status_display': order_obj.get_payment_status_display()
        })
        
    except Exception as e:
        logger.error(f'Payment status check error: {str(e)}')
        return JsonResponse({
            'success': False,
            'message': 'Failed to check payment status'
        }, status=500)


def show_orders(request):
    """Admin view to display all orders with edit and delete functionality"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Check if user is admin
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('products')
    
    db_error = None
    all_orders = []
    total_revenue = 0
    
    try:
        all_orders = list(
            order.objects.select_related('customer', 'product')
            .order_by('-order_date')
        )
        
        # Calculate total revenue from all orders
        revenue_data = order.objects.aggregate(total=Sum('amount'))
        total_revenue = revenue_data['total'] or 0
        
    except OperationalError:
        db_error = 'Order data is unavailable. Please try again later.'
    except Exception as e:
        logger.error(f"Show orders error: {str(e)}")
        db_error = f'An error occurred: {str(e)}'
    
    context = {
        'all_orders': all_orders,
        'db_error': db_error,
        'total_revenue': total_revenue,
        'status_choices': order.STATUS_CHOICES,
        'payment_method_choices': order.PAYMENT_METHOD_CHOICES,
        'payment_status_choices': order.PAYMENT_STATUS_CHOICES,
    }
    
    return render(request, 'show.html', context)


def edit_order(request, order_id):
    """Edit order details - admin only"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Check if user is admin
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('products')
    
    try:
        order_obj = get_object_or_404(order, pk=order_id)
    except:
        messages.error(request, 'Order not found.')
        return redirect('show_orders')
    
    if request.method == 'POST':
        # Update order details
        try:
            order_obj.number_of_trays = int(request.POST.get('number_of_trays', order_obj.number_of_trays))
            order_obj.status = request.POST.get('status', order_obj.status)
            order_obj.payment_method = request.POST.get('payment_method', order_obj.payment_method)
            order_obj.payment_status = request.POST.get('payment_status', order_obj.payment_status)
            order_obj.payment_phone = request.POST.get('payment_phone', order_obj.payment_phone)
            order_obj.payment_reference = request.POST.get('payment_reference', order_obj.payment_reference)
            order_obj.message = request.POST.get('message', order_obj.message)
            
            # Recalculate amount if trays changed
            if order_obj.product:
                order_obj.amount = order_obj.product.price * order_obj.number_of_trays
            
            order_obj.save()
            messages.success(request, 'Order updated successfully.')
            return redirect('show_orders')
        except ValueError:
            messages.error(request, 'Invalid number of trays.')
            return redirect('show_orders')
        except Exception as e:
            logger.error(f"Edit order error: {str(e)}")
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('show_orders')
    
    context = {
        'order_obj': order_obj,
        'status_choices': order.STATUS_CHOICES,
        'payment_method_choices': order.PAYMENT_METHOD_CHOICES,
        'payment_status_choices': order.PAYMENT_STATUS_CHOICES,
    }
    
    return render(request, 'edit_order.html', context)


def delete_order(request, order_id):
    """Delete an order - admin only"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Check if user is admin
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete orders.')
        return redirect('products')
    
    try:
        order_obj = get_object_or_404(order, pk=order_id)
        order_code = order_obj.order_code
        order_obj.delete()
        messages.success(request, f'Order {order_code} has been deleted successfully.')
    except Exception as e:
        logger.error(f"Delete order error: {str(e)}")
        messages.error(request, f'Failed to delete order: {str(e)}')
    
    return redirect('show_orders')

