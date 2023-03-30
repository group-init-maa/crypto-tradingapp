from django.core.management.base import BaseCommand
import requests
from login.models import Coin

class Command(BaseCommand):
    help = 'Updates cryptocurrency prices in the database.'

    def handle(self, *args, **kwargs):
        Coin.update_prices()
