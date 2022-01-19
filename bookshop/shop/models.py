from django.db import models


class Product(models.Model):
    name = models.CharField('name', max_length=255, default='')
    description = models.TextField('description', default='')
    appear_date = models.DateTimeField('appear date', auto_now_add=True)
    price = models.FloatField('price', default=0)

    class Meta:
        abstract = True
        app_label = 'shop'
