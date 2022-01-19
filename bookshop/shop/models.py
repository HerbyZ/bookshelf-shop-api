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


class CoverMaterial(models.TextChoices):
    HARDCOVER = ('HC', 'hardcover')
    PAPERBACK = ('PB', 'paperback')


class Book(Product):
    name = models.CharField('name', max_length=255, default='')
    description = models.TextField('description', default='')
    genre = models.ForeignKey(
        Genre, verbose_name='genre', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(
        Author, verbose_name='author', on_delete=models.CASCADE)
    rating = models.FloatField('rating', default=0)
    cover_material = models.CharField(
        'cover material', max_length=20, choices=CoverMaterial.choices)
    image = models.ImageField('image', upload_to='books')
