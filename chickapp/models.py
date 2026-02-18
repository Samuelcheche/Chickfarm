from django.db import models
import secrets

# Create your models here.
class customer(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=20)
    phone = models.CharField(max_length=10)
    location = models.CharField(max_length=20)
    message = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name + " " + self.surname

class product(models.Model):
    name = models.CharField(max_length=50)
    size = models.CharField(max_length=30, blank=True, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, default="")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


def generate_order_code():
    return "ORD-" + "".join(secrets.choice("0123456789") for _ in range(4))


class order(models.Model):
    STATUS_PROCESSING = "processing"
    STATUS_IN_TRANSIT = "in_transit"
    STATUS_DELIVERED = "delivered"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_PROCESSING, "Processing"),
        (STATUS_IN_TRANSIT, "In Transit"),
        (STATUS_DELIVERED, "Delivered"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    order_code = models.CharField(max_length=12, unique=True, editable=False)
    customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.PROTECT)
    number_of_trays = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PROCESSING)
    order_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=True, default="")

    def save(self, *args, **kwargs):
        if not self.order_code:
            code = generate_order_code()
            while order.objects.filter(order_code=code).exists():
                code = generate_order_code()
            self.order_code = code

        if self.amount <= 0 and self.product_id and self.number_of_trays:
            self.amount = self.product.price * self.number_of_trays

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_code} - {self.customer.name} {self.customer.surname}"


class register(models.Model):
    FullName = models.CharField(max_length=20)
    Email_address = models.EmailField(max_length=50)
    Password = models.CharField(max_length=20)
    Confirm_password = models.CharField(max_length=20)

    def __str__(self):
        return self.FullName







