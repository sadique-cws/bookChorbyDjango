from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    cat_title = models.CharField(max_length=200)
    cat_descr = models.TextField()

    def __str__(self):
        return self.cat_title
    

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    ISBN = models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)
    price = models.FloatField()
    discount_price = models.FloatField(null=True)
    cover = models.ImageField(upload_to="books/image/")

    

    
    def __str__(self):
        return self.title

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,blank=True, null=True) 
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Book, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)

    def __str__(self):
        return self.item.title
    
    def getPrice(self):
        return self.item.price * self.qty
    
    def getDiscountPrice(self):
        return self.item.discount_price * self.qty
        
    def getDiscountPercent(self):
        discount_amount = self.item.price - self.item.discount_price
        percent = discount_amount * 100 / 500
        return percent
    

ADDRESS_TYPE  = (
    ("H", "Home"),
    ("O", "Office"),
)

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,blank=True, null=True) 
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=200)
    pincode = models.IntegerField()
    street = models.CharField(max_length=300)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    landmark = models.CharField(max_length=200)
    address_type = models.CharField(max_length=200,choices=ADDRESS_TYPE)
    default = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
    

class Coupon(models.Model):
    code = models.CharField(max_length=200)
    amount = models.FloatField()

    def __str__(self):
        return self.code

class Payment(models.Model):
    txn_id = models.CharField(max_length=400)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,blank=True, null=True) 
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=200, null=True, blank=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(null=True,blank=True)
    address = models.ForeignKey(Address,on_delete=models.CASCADE,null=True,blank=True)
    ordered = models.BooleanField(default=False)
    coupon =  models.ForeignKey(Coupon,on_delete=models.SET_NULL, null=True, blank=True)
    payment =  models.ForeignKey(Payment,on_delete=models.SET_NULL, null=True, blank=True)
    being_delivered = models.BooleanField(default=False)
    recieved = models.BooleanField(default=False)


    def getTotalPrice(self):
        total = 0
        for oi in self.items.all():
            total += oi.getPrice()
        return total
    
    def getTotalAfterDiscountPrice(self):
        total = 0
        for oi in self.items.all():
            total += oi.getDiscountPrice()
        if self.coupon:
            total -= self.coupon.amount
        return total
    
    def getTotalDiscountPrice(self):
        return self.getTotalPrice() - self.getTotalAfterDiscountPrice()

    def getTax(self):
        return self.getTotalAfterDiscountPrice() * 0.18

    def getPayableAmount(self):
        return self.getTotalAfterDiscountPrice() + self.getTax()

    def __str__(self):
        return self.user.username
    


