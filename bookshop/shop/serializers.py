from rest_framework import serializers

from .models import Book, Order


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['name', 'description', 'appear_date', 'price',
                  'genre', 'author', 'rating', 'cover_material', 'image']
        read_only_fields = ['name', 'description', 'appear_date', 'price',
                            'genre', 'author', 'rating', 'cover_material', 'image']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['products', 'customer', 'status', 'address', 'date']
        read_only_fields = ['products', 'customer', 'status', 'date']
