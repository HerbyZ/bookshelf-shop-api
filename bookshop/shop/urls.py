from django.urls import path

from . import views

urlpatterns = [
    path('books', views.book_list, name='list books'),
    path('books/<int:pk>', views.book_retrieve, name='retrieve book'),
]
