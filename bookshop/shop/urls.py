from django.urls import path

from . import views

urlpatterns = [
    path('books', views.book_list, name='list books'),
    path('books/<int:pk>', views.book_retrieve, name='retrieve book'),
    path('order', views.create_order, name='create order'),
    path('order/pay', views.pay_order, name='pay order'),
    path('order/<int:pk>', views.change_order_address, name='change order address'),
]
