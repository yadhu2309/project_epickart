import email
from statistics import mode
from unicodedata import decimal
from django.db import models
from admin_app.models import *

# Create your models here.


class UserSignUp(models.Model):
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    psw = models.CharField(max_length=50)
    psw1 = models.CharField(max_length=50)
    status = models.BooleanField(max_length=20)
    logstatus = models.BooleanField(max_length=20)



class Cart_view(models.Model):
    uid = models.ForeignKey(UserSignUp, on_delete=models.CASCADE)
    pid = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    tot_amt = models.DecimalField(max_digits=8, decimal_places=2)

class CartGuestUser(models.Model):
    pid = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    user_session = models.CharField(max_length=100)

class Cart_total(models.Model):
    uid = models.ForeignKey(UserSignUp, on_delete=models.CASCADE)
    cid = models.ForeignKey(Cart_view, on_delete=models.CASCADE)
    total_amt = models.DecimalField(max_digits=8, decimal_places=2)


class Wish(models.Model):
    uid = models.ForeignKey(UserSignUp, on_delete=models.CASCADE)
    pid = models.ForeignKey(Product, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)


class Payment(models.Model):
    user = models.ForeignKey(UserSignUp,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('Out of delivery', 'Out of delivery'),
        ('Cancelled', 'Cancelled'),
        ('Returned', 'Returned')
    )
    user = models.ForeignKey(UserSignUp, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.IntegerField(null=True)
    order_total = models.FloatField()
    status = models.CharField(max_length=50, choices=STATUS, default='Confirmed')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderProduct(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('Out of delivery', 'Out of delivery'),
        ('Cancelled', 'Cancelled'),
        ('Returned', 'Returned')
    )
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL,null=True,blank=True)
    user = models.ForeignKey(UserSignUp, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=True)
    status = models.CharField(max_length=50, choices=STATUS, default='Confirmed')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)



class Address(models.Model):
    user = models.ForeignKey(UserSignUp,on_delete=models.CASCADE,default=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address_line_1 = models.CharField(max_length=100)
    address_line_2 =  models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.IntegerField()
    phone = models.CharField(max_length=10)
    email = models.CharField(max_length=100)

class ReferralCode(models.Model):
    user = models.ForeignKey(UserSignUp,on_delete=models.CASCADE)
    refer_code = models.CharField(max_length=100)
    status = models.BooleanField(max_length=20,default=True)

class Wallet(models.Model):
    user = models.ForeignKey(UserSignUp,on_delete=models.CASCADE)
    status = models.BooleanField(max_length=20,default=True)
    money = models.IntegerField()
    
class CouponApplied(models.Model):
    coupon_id = models.ForeignKey(Coupon,on_delete=models.CASCADE)
    user = models.ForeignKey(UserSignUp,on_delete=models.CASCADE)

    status = models.BooleanField(max_length=20,default=False)

class ReturnedOrder(models.Model):
    pid = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(UserSignUp,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.BooleanField(max_length=20,default=True)
