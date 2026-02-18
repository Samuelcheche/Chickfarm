from django.contrib import admin
from chickapp.models import customer, product, order, register


@admin.register(customer)
class CustomerAdmin(admin.ModelAdmin):
	exclude = ('password',)


admin.site.register(product)
admin.site.register(order)
admin.site.register(register)
