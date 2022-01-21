from django.db import models

from accounts.models import User
from catalog.models import Product


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


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField('amount', default=1)

    def __str__(self):
        return self.product.name


class Cart(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct)

    def __str__(self):
        return self.owner.email
