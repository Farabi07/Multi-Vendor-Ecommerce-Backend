from django.db import models
from django.contrib.auth.models import User
from authentication.models import *


class ProductCategory(models.Model):
    title = models.CharField(max_length=250,null=True,blank=True)
    details = models.TextField(null=True)

    def __str__(self):
        return self.title
    
class Product(models.Model):
    category = models.ForeignKey(ProductCategory,on_delete = models.SET_NULL,null=True,related_name='category_product')
    vendor = models.ForeignKey(Vendor,on_delete = models.SET_NULL,null=True,blank=True)
    title = models.CharField(max_length=250,null=True,blank=True) 
    details = models.TextField(null=True)
    price = models.FloatField(max_length=250,null=True,blank=True)
    
    def __str__(self):
        return self.title
    
class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='products_customer',)
    phone = models.CharField(max_length=250,null=True,blank=True)

    def __str__(self):
        return self.user.username
    
class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,related_name='customer_order')
    order_time = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,related_name='odered_product')

    def __str__(self):
        return self.product.title