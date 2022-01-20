from django.db import models
from polymorphic.models import PolymorphicModel


class Product(PolymorphicModel):
    name = models.CharField('name', max_length=255, default='')
    description = models.TextField('description', default='')
    appear_date = models.DateTimeField('appear date', auto_now_add=True)
    price = models.FloatField('price', default=0)

    class Meta:
        app_label = 'shop'


class Author(models.Model):
    first_name = models.CharField('first name', max_length=255, default='')
    last_name = models.CharField(
        'last name', max_length=255, null=True, blank=True)
    add_date = models.DateTimeField('add date', auto_now_add=True)

    class Meta:
        app_label = 'shop'

    def __str__(self):
        s = self.first_name
        if self.last_name:
            s += f' {self.last_name}'

        return s


class Genre(models.Model):
    name = models.CharField('name', max_length=255, unique=True)

    class Meta:
        app_label = 'shop'

    def __str__(self):
        return self.name


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


class OrderStatus(models.TextChoices):
    WAITING_FOR_PAYMENT = 'Waiting for payment'
    DELIVERING = 'In deliver'
    DELIVERED = 'Delivered'
    CANCELED = 'Canceled'
    RETURNED = 'Returned'


class Order(models.Model):
    products = models.ManyToManyField(Product)
    customer = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE, default=0)
    status = models.CharField(
        'status', choices=OrderStatus.choices, max_length=25, default=OrderStatus.WAITING_FOR_PAYMENT)
    address = models.CharField('address', max_length=255, default='')
    date = models.DateTimeField('date', auto_now_add=True)

    def pay(self):
        price = 0
        for p in self.products:
            price += p.price

        sum_to_pay_by_bonuses = price / 2
        if sum_to_pay_by_bonuses > self.customer.bonus_balance:
            sum_to_pay_by_bonuses = self.customer.bonus_balance

        sum_to_pay_by_balance = price - sum_to_pay_by_bonuses
        if sum_to_pay_by_balance > self.customer.balance:
            raise ValueError(
                'There are not enough funds on your account to pay this order')

        self.customer.bonus_balance -= sum_to_pay_by_bonuses
        self.customer.balance -= sum_to_pay_by_balance

        self.customer.save()

        self.status = OrderStatus.DELIVERING
        self.save()

    def __str__(self):
        date = self.date.strftime('%H:%M %d.%m.%Y')
        return f"{self.customer} - {date}"
