from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=16, decimal_places=2, default=1000.00)

    def __str__(self):
        return self.user.username

class Coin(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    current_price = models.DecimalField(max_digits=16, decimal_places=2)

    def __str__(self):
        return self.symbol

class Portfolio(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=True, default=None)
    coins = models.ManyToManyField(Coin, through='Transaction')

    def __str__(self):
        if self.user_profile is not None:
            return f"{self.user_profile.user.username} - Portfolio"
        else:
            return "No user profile associated - Portfolio"

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('BUY', 'Buy'),
        ('SELL', 'Sell')
    )

    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    quantity = models.DecimalField(max_digits=16, decimal_places=8)
    price = models.DecimalField(max_digits=16, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.portfolio.user_profile.user.username} - {self.transaction_type} - {self.coin.symbol}"
