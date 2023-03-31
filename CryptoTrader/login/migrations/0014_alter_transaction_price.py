# Generated by Django 4.1.7 on 2023-03-31 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0013_coin_price_change_24h_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=16),
        ),
    ]