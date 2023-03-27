import datetime
from matplotlib import pyplot as plt
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



#retrieve chart data for curreency

def getMarketCharts(coinId='bitcoin', vsCurrency='gbp', days='max', interval='daily'):
    cryptoIds = availableCrypto()

    if coinId in cryptoIds:
        url = f'https://api.coingecko.com/api/v3/coins/{coinId}/market_chart?vs_currency={vsCurrency}&days={days}&interval={interval}'
        payload = {"vsCurrency": vsCurrency, "days": days, "interval": interval}
        response = requests.get(url, params=payload)
        data = response.json()

        timestamp_list, price_list = [], []
        for price in data['prices']:
            timestamp_list.append(datetime.datetime.fromtimestamp(price[0]/1000))
            price_list.append(price[1])
        
        raw_data = {
            'timestamp' : timestamp_list,
            'price': price_list
        }
        df = pd.DataFrame(raw_data)
        return df
    else:
        print("Crypto selected is not available")
    
    return data

market_info = getMarketCharts('bitcoin', 'gbp', '30')

market_info.plot(y='price', x='timestamp', color='#4285F4')
plt.show()
print(market_info)