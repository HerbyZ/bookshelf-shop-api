from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['products', 'customer', 'status', 'address', 'date']
        read_only_fields = ['products', 'customer', 'status', 'date']
