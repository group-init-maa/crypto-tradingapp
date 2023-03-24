import requests
import pandas as pd
import mplfinance as mpf

#checks if crytpo exists

def availableCrypto():
    url = f'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin%2Cethereum%2Cdogecoin%2Csolana&vs_currencies=gbp'
    response = requests.get(url)
    data = response.json()

    cryptoids = []

    for asset in data:
        cryptoids.append(asset)

    return cryptoids



#retrive chart data for curreency

def getMarketCharts(coinId='bitcoin', vsCurrency='gbp', days='max', interval='daily'):
    cryptoIds = availableCrypto()

    if coinId in cryptoIds:
        url = f'https://api.coingecko.com/api/v3/coins/{coinId}/market_chart?vs_currency={vsCurrency}&days={days}'
        response = requests.get(url)
        data = response.json()
    
    return data

print(getMarketCharts())