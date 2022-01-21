from django.contrib import admin

from .models import User


class UserModelAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_joined', 'bonus_balance',
                    'is_admin', 'is_active', 'is_staff', 'is_superuser')
    fields = ('email', 'bonus_balance', 'date_joined', 'last_login',
              'is_admin', 'is_active', 'is_staff', 'is_superuser', 'balance', 'password')
    readonly_fields = ('date_joined', 'last_login', 'password')


admin.site.register(User, UserModelAdmin)
