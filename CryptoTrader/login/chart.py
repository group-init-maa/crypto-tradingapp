import requests
import pandas as pd
import datetime
import matplotlib.pyplot as plt

#checks if crytpo exists

def availableCrypto():
    url = f'https://api.coingecko.com/api/v3/coins'
    response = requests.get(url)
    data = response.json()

    cryptoids = []

    for asset in data:
        cryptoids.append(asset['id'])

    return cryptoids

print(availableCrypto())