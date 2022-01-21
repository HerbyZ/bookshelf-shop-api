from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from accounts.models import User

from .serializers import BookSerializer, OrderSerializer
from .models import Book, Order, OrderStatus, Product


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTTokenUserAuthentication])
def get_orders_for_user(request, pk):
    user = get_object_or_404(User, id=pk)

    if request.user.id != user.id:
        return Response({'detail': 'Access denied'}, 401)

    orders = user.order_set.order_by('-date')
    serializer = OrderSerializer(orders, many=True)

    return Response(serializer.data, 200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTTokenUserAuthentication])
def create_order(request):
    data = request.data

    products = []
    for product_id in data['products']:
        product = get_object_or_404(Product, id=product_id)
        products.append(product)

    address = data['address']

    order = Order.objects.create(
        products=products, customer=request.user, address=address)
    serializer = OrderSerializer(order)

    return Response(serializer.data, 201)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTTokenUserAuthentication])
def pay_order(request):
    order_id = request.data['order']
    order = get_object_or_404(Order, id=order_id)

    if order.customer.id != request.user.id:
        return Response({'detail': 'Access denied'}, 401)

    try:
        order.pay()
    except ValueError as e:
        return Response({'detail': str(e)})

    serializer = OrderSerializer(order)

    return Response(serializer.data, 200)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTTokenUserAuthentication])
def change_order_address(request, pk):
    order = get_object_or_404(Order, id=pk)
    address = request.data['address']

    if order.customer.id != request.user.id:
        return Response({'detail': 'Access denied'}, 401)

    if order.status not in [OrderStatus.WAITING_FOR_PAYMENT, OrderStatus.DELIVERING]:
        return Response({'detail': 'Order already delivered, cancelled or returned'}, 400)

    order.address = address
    order.save()

    serializer = OrderSerializer(order)

    return Response(serializer.data, 200)
