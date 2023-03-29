from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Portfolio(models.Model):
    username = models.CharField(max_length=150)
    balance = models.IntegerField(default=1000)
    transactions = []
    assets = []

    def init(self, args, **kwargs):
        super(Portfolio, self).init(args, **kwargs)
        self.transactions = []
        self.assets = []

    def str(self):
        return self.username


class Coin(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10)
    description = models.TextField(blank=True)
    current_price = models.DecimalField(max_digits=20, decimal_places=10)
    logo_url = models.URLField(blank=True)

    def __str__(self):
        return self.name