from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=200)
    detail = models.CharField(max_length=400)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    modelname = models.CharField(max_length=300)
    detail = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=50,decimal_places=2)
    image1 = models.ImageField(upload_to='product_image')
    image2 = models.ImageField(upload_to='product_image')
    image3 = models.ImageField(upload_to='product_image')
    image4 = models.ImageField(upload_to='product_image')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    house_society_name = models.CharField(max_length=255)
    landmark_area = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=10)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=255)
    modelname = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(max_length=500, null=True, blank=True)
    
    def get_total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return self.name
    
