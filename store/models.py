from django.db import models

class Product(models.Model):
    active = models.BooleanField(default=True)
    description = models.TextField(max_length=250)
    stock_quantity = models.IntegerField(default=0)
    price = models.BigIntegerField()
    name = models.CharField(max_length=100)

class User(models.Model):
    address = models.CharField(max_length=250, null=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=60)
    email = models.CharField(max_length=320, unique=True)
    is_staff = models.BooleanField(default=False)

class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)


# Relations

class Contains(models.Model):
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey('Product')
    order = models.ForeignKey('Order')

class Orders(models.Model):
    user = models.ForeignKey('User')
    order = models.ForeignKey('Order')

class Supplies(models.Model):
    product = models.ForeignKey('Product')
    supplier = models.ForeignKey('Supplier')
