from django.db import models
from django.contrib.auth.models import User


# PRODUCTS
class Products(models.Model):
    pname = models.CharField(max_length=25)
    pdesc = models.CharField(max_length=100)
    price = models.IntegerField()
    pcategory = models.CharField(max_length=30)
    trending = models.BooleanField(default=False)
    offer = models.BooleanField(default=False)
    pimage = models.ImageField(upload_to='uploads', default='Default.jpg')

    def __str__(self):
        return self.pname


# CART
class CartModel(models.Model):
    pname = models.CharField(max_length=25)
    price = models.IntegerField()
    pcategory = models.CharField(max_length=30)
    quatity = models.IntegerField()
    totalprice = models.IntegerField()
    host = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.pname


# ORDER
class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    quantity = models.IntegerField(default=1)

    price = models.IntegerField()

    status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("Shipped", "Shipped"),
            ("Delivered", "Delivered")
        ],
        default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.pname}"