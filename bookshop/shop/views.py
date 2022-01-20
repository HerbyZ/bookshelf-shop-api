from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import BookSerializer
from .models import Book


@api_view(['GET'])
@permission_classes([AllowAny])
def book_list(request):
    books = Book.objects.order_by('-appear_date')
    serializer = BookSerializer(books, many=True)

    return Response(serializer.data, 200)


@api_view(['GET'])
@permission_classes([AllowAny])
def book_retrieve(request, pk):
    book = get_object_or_404(Book, id=pk)
    serializer = BookSerializer(book)

    return Response(serializer.data, 200)

# TODO: Buy product view
