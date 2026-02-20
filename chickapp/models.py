from django.db import models
import secrets

# Create your models here.
class customer(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
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

    PAYMENT_MPESA = "mpesa"
    PAYMENT_AIRTEL = "airtel_money"
    PAYMENT_CASH = "cash"

    PAYMENT_METHOD_CHOICES = [
        (PAYMENT_MPESA, "M-Pesa"),
        (PAYMENT_AIRTEL, "Airtel Money"),
        (PAYMENT_CASH, "Cash on Delivery"),
    ]

    PAYMENT_STATUS_PENDING = "pending"
    PAYMENT_STATUS_COMPLETED = "completed"
    PAYMENT_STATUS_FAILED = "failed"

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, "Pending"),
        (PAYMENT_STATUS_COMPLETED, "Completed"),
        (PAYMENT_STATUS_FAILED, "Failed"),
    ]

    order_code = models.CharField(max_length=12, editable=False, default='TEMP')
    customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.PROTECT, null=True, blank=True)
    number_of_trays = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PROCESSING)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True, default="")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    payment_phone = models.CharField(max_length=15, blank=True, default="")
    payment_reference = models.CharField(max_length=50, blank=True, default="")
    mpesa_checkout_request_id = models.CharField(max_length=100, blank=True, default="")
    mpesa_merchant_request_id = models.CharField(max_length=100, blank=True, default="")
    mpesa_receipt_number = models.CharField(max_length=50, blank=True, default="")
    order_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=True, default="")

    def save(self, *args, **kwargs):
        if not self.order_code or self.order_code == 'TEMP':
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
    FullName = models.CharField(max_length=100)
    Email_address = models.EmailField(max_length=100)
    Password = models.CharField(max_length=255)
    Confirm_password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.FullName


class contact_message(models.Model):
    """Store contact form submissions from customers"""
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']







