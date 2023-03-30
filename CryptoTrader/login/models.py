from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import requests

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=16, decimal_places=2, default=1000.00)

    def __str__(self):
        return self.user.username
    
    def balance_history(self):
        transactions = Transaction.objects.filter(portfolio=self.portfolio).order_by('timestamp')
        balance_history = []
        balance = self.balance
        for transaction in transactions:
            if transaction.transaction_type == 'BUY':
                balance -= transaction.quantity * transaction.price
            elif transaction.transaction_type == 'SELL':
                balance += transaction.quantity * transaction.price
            balance_history.append((transaction.timestamp.date(), balance))
        return balance_history

class Coin(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=20)
    image_url = models.URLField(default="")
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    market_cap = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    price_change_24h = models.DecimalField(max_digits=20, decimal_places=2,default=0)
    price_change_percentage_24h = models.DecimalField(max_digits=20, decimal_places=2,default=0)
    last_updated = models.DateTimeField(default="2022-03-02")

    @classmethod
    def update_prices(cls):
        """
        Retrieves the latest cryptocurrency prices from an API and updates the database.
        """
        url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=gbp&order=market_cap_desc&per_page=100&page=1&sparkline=false&locale=en'
        response = requests.get(url)
        data = response.json()
        for coin_data in data:
            name = coin_data["name"]
            symbol = coin_data["symbol"]
            try:
                price = coin_data['current_price']
                image_url = coin_data['image']
                last_updated = coin_data['last_updated']
                price_change_24h = coin_data['price_change_24h']
                price_change_percentage_24h = coin_data['price_change_percentage_24h']
            except KeyError:
                print(f"data for {name} went wrong somewhere")
                continue
            try:
                coin = cls.objects.get(name=name)
                coin.price = price
                coin.save()
            except cls.DoesNotExist:
                coin = cls(name=name, symbol=symbol, price=price, image_url=image_url, last_updated=last_updated, price_change_24h=price_change_24h, price_change_percentage_24h=price_change_percentage_24h)
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
    balance = models.DecimalField(max_digits=16, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.portfolio.user_profile.user.username} - {self.transaction_type} - {self.coin.symbol}"

    def save(self, *args, **kwargs):
        """
        Override the default save method to update the balance after each transaction.
        """
        if self.transaction_type == 'BUY':
            self.balance = self.portfolio.user_profile.balance - (Decimal(str(self.price)) * Decimal(str(self.quantity)))
        elif self.transaction_type == 'SELL':
            self.balance = self.portfolio.user_profile.balance + (Decimal(str(self.price)) * Decimal(str(self.quantity)))
        self.portfolio.user_profile.balance = self.balance
        self.portfolio.user_profile.save()
        super().save(*args, **kwargs)