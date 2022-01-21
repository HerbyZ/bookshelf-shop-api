from rest_framework import serializers

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['name', 'description', 'appear_date', 'price', 'genre',
                  'author', 'rating', 'cover_material', 'image', 'release_year']
        read_only_fields = ['name', 'description', 'appear_date', 'price', 'genre',
                            'author', 'rating', 'cover_material', 'image', 'release_year']
