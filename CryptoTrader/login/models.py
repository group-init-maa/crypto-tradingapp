from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Portfolio(models.Model):
    username = models.CharField(max_length=150)
    transactions = []

    def __str__(self):
        return self.name


class Coin(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    current_price = models.DecimalField(max_digits=20, decimal_places=10)
    logo_url = models.URLField(blank=True)

    def __str__(self):
        return self.name