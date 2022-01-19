from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'bonus_balance', 'is_admin',
                  'is_active', 'is_staff', 'is_superuser']
        read_only_fields = ['bonus_balance', 'is_admin',
                            'is_active', 'is_staff', 'is_superuser']
