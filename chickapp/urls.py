    
from django.urls import path
from chickapp import views




urlpatterns = [
    path('index/', views.index, name='index'),

    path('about/', views.about, name='about'),
    
    path('contact/', views.contact, name='contact'),

    path('delivery/', views.delivery, name='delivery'),


    path('dashboard/', views.dashboard, name='dashboard'),

    path('products/', views.products, name='products'),

    path('orders/', views.orders, name='orders'),

    path('show-orders/', views.show_orders, name='show_orders'),
    
    path('edit-order/<int:order_id>/', views.edit_order, name='edit_order'),
    
    path('delete-order/<int:order_id>/', views.delete_order, name='delete_order'),

    path('process-payment/', views.process_payment, name='process_payment'),

    path('mpesa/callback/', views.mpesa_callback, name='mpesa_callback'),

    path('check-payment-status/', views.check_payment_status, name='check_payment_status'),

     path('', views.register, name='register'),
    
    path('login/', views.login_user, name='login'),
    
    path('logout/', views.logout_user, name='logout'), 
]
