from django.urls import path

from . import views

urlpatterns = [
    path('order', views.create_order, name='create order'),
    path('order/pay', views.pay_order, name='pay order'),
    path('order/<int:pk>', views.change_order_address,
         name='change order address'),
    path('orders/<int:pk>', views.get_orders_for_user, name='get user orders'),
    path('cart/add', views.add_product_to_cart, name='add to cart'),
    path('cart/remove/<int:pk>', views.update_cart_product,
         name='update cart product'),
    path('cart/empty', views.empty_cart, name='empty cart'),
]
