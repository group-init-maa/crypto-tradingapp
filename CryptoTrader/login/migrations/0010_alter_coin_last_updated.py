# Generated by Django 4.1.7 on 2023-03-29 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_alter_coin_last_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coin',
            name='last_updated',
            field=models.DateTimeField(default='2022-03-02'),
        ),
    ]
