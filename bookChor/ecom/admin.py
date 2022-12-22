from django.contrib import admin
from .models import *


admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Coupon)
admin.site.register(Payment)
admin.site.register(Address)
