# Generated by Django 4.0.1 on 2022-01-21 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_cartproduct_cart'),
        ('accounts', '0002_user_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cart',
            field=models.OneToOneField(auto_created=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.cart'),
        ),
    ]
