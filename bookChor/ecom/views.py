from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.utils import timezone
# Create your views here.


def home(r):
    return render(r, "home.html",{"books":Book.objects.all()})

def category(r, cat_id):
    pass 

def viewBook(r, b_id):
    return render(r, "viewBook.html",{"book": Book.objects.get(pk=b_id), "books":Book.objects.exclude(id=b_id)}) 


def cart(r):
    return render(r,"cart.html")


def addToCart(r,item):
    book = get_object_or_404(Book, id=item)
    orderitem, created = OrderItem.objects.get_or_create(item=book,ordered=False,user=r.user)
    order_qs = Order.objects.filter(user=r.user,ordered=False)
    
    if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item=book).exists():
                orderitem.qty += 1
                orderitem.save()
            else:
                order.items.add(orderitem)
    else:
        order_time = timezone.now()
        order = Order.objects.create(user=r.user, ordered_date=order_time)

        order.items.add(orderitem)
    return redirect(cart)


def search(r):
    pass 

