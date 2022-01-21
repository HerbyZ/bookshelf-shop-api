from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'balance', 'bonus_balance', 'is_admin',
                  'is_active', 'is_staff', 'is_superuser']
        read_only_fields = ['id', 'bonus_balance', 'balance', 'is_admin',
                            'is_active', 'is_staff', 'is_superuser']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({'user_id': self.user.id})

        return data
