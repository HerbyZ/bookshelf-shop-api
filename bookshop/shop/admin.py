from django.contrib import admin

from .models import Order, Cart, CartProduct

admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartProduct)
