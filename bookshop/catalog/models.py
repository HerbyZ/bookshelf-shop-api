from django.db import models
from polymorphic.models import PolymorphicModel


class Product(PolymorphicModel):
    name = models.CharField('name', max_length=255, default='')
    description = models.TextField('description', default='')
    appear_date = models.DateTimeField('appear date', auto_now_add=True)
    price = models.FloatField('price', default=0)

    class Meta:
        app_label = 'catalog'


class Genre(models.Model):
    name = models.CharField('name', max_length=255, unique=True)

    class Meta:
        app_label = 'catalog'

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField('first name', max_length=255, default='')
    last_name = models.CharField(
        'last name', max_length=255, null=True, blank=True)
    add_date = models.DateTimeField('add date', auto_now_add=True)

    class Meta:
        app_label = 'catalog'

    def __str__(self):
        s = self.first_name
        if self.last_name:
            s += f' {self.last_name}'

        return s


class CoverMaterial(models.TextChoices):
    HARDCOVER = 'hardcover'
    PAPERBACK = 'paperback'


class Book(Product):
    genre = models.ForeignKey(
        Genre, verbose_name='genre', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(
        Author, verbose_name='author', on_delete=models.CASCADE)
    rating = models.FloatField('rating', default=0)
    cover_material = models.CharField(
        'cover material', max_length=20, choices=CoverMaterial.choices)
    release_year = models.PositiveIntegerField('release year', null=True)
    image = models.ImageField('image', upload_to='books')

    def __str__(self):
        return f'{self.author} - {self.name}'

    class Meta:
        app_label = 'catalog'
