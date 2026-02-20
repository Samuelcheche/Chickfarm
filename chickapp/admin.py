from django.contrib import admin
from chickapp.models import customer, product, order, register


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


admin.site.register(product)
admin.site.register(register)
