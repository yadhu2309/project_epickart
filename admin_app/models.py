from statistics import mode
from django.db import models


# Create your models here.


class Category(models.Model):
    cate_name = models.CharField(max_length=100)

class Brand(models.Model):
    Brand_name = models.CharField(max_length=100)

class Product(models.Model):
    
    series = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8,decimal_places=2)
    price_actual = models.DecimalField(max_digits=8,decimal_places=2,default=True)
    stock = models.CharField(max_length=100)
    descrip = models.TextField()
    p_brand = models.CharField(max_length=100)
    p_name = models.CharField(max_length=100)
    ssd = models.BooleanField(max_length=20)
    mem = models.CharField(max_length=100)
    ram = models.CharField(max_length=100)
    rtype = models.CharField(max_length=100,default=True)
    os = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/images', null=True, blank=True)
    image1 = models.ImageField(upload_to='static/images', null=True, blank=True)
    image2 = models.ImageField(upload_to='static/images', null=True, blank=True)
    image3 = models.ImageField(upload_to='static/images', null=True, blank=True)
    cid = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_offer_apply = models.BooleanField(max_length=20,default=True)


class AdminDetail(models.Model):
    email = models.CharField(max_length=100)
    psw = models.CharField(max_length=100)


class Coupon(models.Model):
    discount_amount = models.IntegerField() 
    discountpercentage = models.IntegerField()
    valid_till = models.DateTimeField()
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.BooleanField(max_length=20,default=True)



class CategoryOffer(models.Model):
    cid = models.ForeignKey(Category,on_delete=models.CASCADE)
    valid_till = models.DateField()
    Name = models.CharField(max_length=100)
    percentage = models.IntegerField()
    description = models.TextField()
    status = models.BooleanField(max_length=20,default=True)
    
class ProductOffer(models.Model):
    pid = models.ForeignKey(Product,on_delete=models.CASCADE)
    valid_till = models.DateField()
    Name = models.CharField(max_length=100,unique=True)
    percentage = models.IntegerField()
    description = models.TextField()
    status = models.BooleanField(max_length=100,default=True)

class FrontBanner(models.Model):
    head = models.CharField(max_length=100)
    description = models.TextField()
    banner1 = models.ImageField(upload_to='static/images', null=True, blank=True)
    banner2 = models.ImageField(upload_to='static/images', null=True, blank=True)
    banner3 = models.ImageField(upload_to='static/images', null=True, blank=True)
    select = models.BooleanField(max_length=20,default=False)
    status = models.BooleanField(max_length=20,default=False)

class BannerApplied(models.Model):
    banner = models.ForeignKey(FrontBanner,on_delete=models.CASCADE)
    status = models.BooleanField(max_length=20,default=False)

class SubBanner(models.Model):
    head1 = models.CharField(max_length=100)
    head2 = models.TextField()
    head3 = models.CharField(max_length=100,default=True)
    banner1 = models.ImageField(upload_to='static/images', null=True, blank=True)
    banner2 = models.ImageField(upload_to='static/images', null=True, blank=True)
    banner3 = models.ImageField(upload_to='static/images', null=True, blank=True)
    select = models.BooleanField(max_length=20,default=False)

class SubBannerApplied(models.Model):
    subbanner = models.ForeignKey(SubBanner,on_delete=models.CASCADE)
    status = models.BooleanField(max_length=20,default=False)

class SalesReport(models.Model):
    productName = models.CharField(max_length=100)
    categoryName = models.CharField(max_length=100)
    date = models.DateField()
    quantity = models.IntegerField()
    productPrice = models.FloatField()
    