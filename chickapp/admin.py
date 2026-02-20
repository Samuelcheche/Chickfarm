from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from chickapp.models import customer, product, order, register


# Unregister default User admin and re-register with custom configuration
admin.site.unregister(User)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
	list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'date_joined')
	list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
	search_fields = ('username', 'email', 'first_name', 'last_name')
	date_hierarchy = 'date_joined'


@admin.register(customer)
class CustomerAdmin(admin.ModelAdmin):
	exclude = ('password',)
	list_display = ('id', 'name', 'surname', 'email', 'phone', 'location')
	search_fields = ('name', 'surname', 'email', 'phone')


@admin.register(order)
class OrderAdmin(admin.ModelAdmin):
	list_display = (
		'order_code',
		'customer',
		'product',
		'number_of_trays',
		'amount',
		'status',
		'payment_method',
		'payment_status',
		'order_date',
	)
	list_filter = ('status', 'payment_method', 'payment_status', 'order_date')
	search_fields = ('order_code', 'customer__name', 'customer__surname', 'customer__email', 'payment_reference')
	ordering = ('-order_date',)


@admin.register(register)
class RegisterAdmin(admin.ModelAdmin):
	list_display = ('FullName', 'Email_address', 'created_at')
	search_fields = ('FullName', 'Email_address')
	list_filter = ('created_at',)
	date_hierarchy = 'created_at'
	readonly_fields = ('created_at',)


admin.site.register(product)
