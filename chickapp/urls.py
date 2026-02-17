    
from django.contrib import admin
from django.urls import path
from chickapp import views




urlpatterns = [
    path('admin/', admin.site.urls),

    path('index/', views.index, name='index'),

    path('about/', views.about, name='about'),

    path('delivery/', views.delivery, name='delivery'),


    path('dashboard/', views.dashboard, name='dashboard'),

    path('products/', views.products, name='products'),

     path('', views.register, name='register'),
    
    path('login/', views.login_user, name='login'), 
]
