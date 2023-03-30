# Generated by Django 4.1.7 on 2023-03-30 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0012_transaction_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='coin',
            name='price_change_24h',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='coin',
            name='price_change_percentage_24h',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]
