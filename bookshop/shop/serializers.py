from rest_framework import serializers

from .models import Cart, CartProduct, Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['products', 'customer', 'status', 'address', 'date']
        read_only_fields = ['products', 'customer', 'status', 'date']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['products', 'owner']
        read_only_fields = ['products', 'owner']


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ['product', 'amount']
        read_only_fields = ['product']
