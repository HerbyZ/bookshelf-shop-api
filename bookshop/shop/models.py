from django.db import models


class Product(models.Model):
    name = models.CharField('name', max_length=255, default='')
    description = models.TextField('description', default='')
    appear_date = models.DateTimeField('appear date', auto_now_add=True)
    price = models.FloatField('price', default=0)

    class Meta:
        abstract = True
        app_label = 'shop'


class Author(models.Model):
    first_name = models.CharField('first name', max_length=255, default='')
    last_name = models.CharField(
        'last name', max_length=255, null=True, blank=True)
    add_date = models.DateTimeField('add date', auto_now_add=True)

    class Meta:
        app_label = 'shop'


class Genre(models.Model):
    name = models.CharField('name', max_length=255, unique=True)

    class Meta:
        app_label = 'shop'
