# Generated by Django 4.1.7 on 2023-03-29 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_alter_coin_symbol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coin',
            name='symbol',
            field=models.CharField(max_length=10),
        ),
    ]
