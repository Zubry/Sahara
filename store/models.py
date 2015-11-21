from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.core.mail import send_mass_mail

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
    def __str__(self):
        return self.name

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

#Trigger/Signals and handlers

@receiver(pre_save, sender=Contains)
def Contains_save_handler(sender, instance, *args, **kwargs):
    p = Product.objects.get(id=instance.product.id)
    q = int(instance.quantity)
    r = int(p.stock_quantity)
    if q>r:
        instance.quantity = p.stock_quantity
    return 0

@receiver(post_save, sender=Product)
def Low_stock_notification(sender, instance, *args, **kwargs):
    u = User.objects.filter(is_staff=True).values_list('email', flat=True)
    newlist = [t.encode('utf8') for t in u]
    s = int(instance.stock_quantity)
    if s < 10:
        for z in newlist:
            send_mail('Sahara Automated Alert: Product low on stock', ''.join((instance.name, ' is low on stock')), 'SaharaAutoEmailer@yahoo.com', [z])
    return 0;
