
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from ecom.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="homepage"),
    path("<int:b_id>/book/",viewBook,name="view"),
    path("cart/",cart,name="cart"),
    path("add-to-cart/<int:item>",addToCart,name="addToCart"),

] 

urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


