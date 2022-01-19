from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path('token', views.CustomTokenObtainPairView.as_view(), name='obtain token'),
    path('token/refresh', TokenRefreshView.as_view(), name='refresh token'),
    path('register', views.register_view, name='register user'),
    path('user/<int:pk>', views.user_detail, name='user detail'),
    path('change-password/<int:pk>', views.change_password, name='change password'),
    path('delete-account/<int:pk>', views.delete_user, name='delete user'),
]
