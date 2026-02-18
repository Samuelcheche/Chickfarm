from django.db import models

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
    

class order(models.Model):
    number_of_trays =  models.IntegerField()
    customer = models.ForeignKey(customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True, default="")

    
    def __str__(self):
        return self.customer.name + " " + self.customer.surname + " - " + str(self.order_date)


class register(models.Model):
    FullName = models.CharField(max_length=20)
    Email_address = models.EmailField(max_length=50)
    Password = models.CharField(max_length=20)
    Confirm_password = models.CharField(max_length=20)

    def __str__(self):
        return self.FullName







