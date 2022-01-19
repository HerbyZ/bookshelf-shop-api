from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from .models import User
from .serializers import CustomTokenObtainPairSerializer, UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request: Request):
    user_data = request.data
    serializer = UserSerializer(data=user_data)

    try:
        User.objects.get(email=user_data['email'])
        return Response({'detail': 'User with specified email already exists'})
    except User.DoesNotExist:
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data, 201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTTokenUserAuthentication])
def user_detail(request: Request, pk):
    user = get_object_or_404(User, id=pk)

    if request.user.id != user.id:
        return Response({'detail': 'Access denied'}, 401)

    serializer = UserSerializer(user)

    return Response(serializer.data, 200)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTTokenUserAuthentication])
def change_password(request: Request, pk):
    data = request.data
    old_password = data['old_password']
    new_password = data['new_password']

    user = get_object_or_404(User, id=pk)

    if request.user.id != user.id:
        return Response({'detail': 'Access denied'}, 401)

    if not user.check_password(old_password):
        return Response({'detail': 'Wrong previous password'}, 400)

    user.set_password(new_password)
    user.save()

    return Response({'detail': 'Password changed successfully'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTTokenUserAuthentication])
def delete_user(request: Request, pk):
    user = get_object_or_404(User, id=pk)

    if request.user.id != user.id:
        return Response({'detail': 'Access denied'}, 401)

    user.delete()
    serializer = UserSerializer(user)

    return Response(serializer.data, 200)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
