from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import requests

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=16, decimal_places=2, default=1000.00)

    def __str__(self):
        return self.user.username

class Coin(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=20)
    image_url = models.URLField(default="")
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    market_cap = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    last_updated = models.DateTimeField(default="2022-03-02")

    @classmethod
    def update_prices(cls):
        """
        Retrieves the latest cryptocurrency prices from an API and updates the database.
        """
        url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin%2Cethereum%2Cdogecoin%2Csolana&vs_currencies=gbp'
        # params = {
        #     'vs_currency': 'gbp',
        #     'order': 'market_cap_desc',
        #     'per_page': 100,
        #     'page': 1,
        #     'sparkline': False,
        # }
        response = requests.get(url)
        data = response.json()
        for coin_id in data.keys():
            name = coin_id
            price = data[coin_id]['gbp']
            coin, created = cls.objects.get_or_create(name=name, price=price)
            coin.save()



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
