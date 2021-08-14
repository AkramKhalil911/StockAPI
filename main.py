STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = 'newsAPI KEY'
STOCK_API_KEY = 'stockAPI Key'
TWILIO_SID = 'twilioAPI sid'
TWILIO_AUTH = 'twilio auth key'

import requests
import datetime as dt
from twilio.rest import Client

today = dt.datetime.now()
day = today.day
yesterday = today.strftime(f"%Y-%m-{day - 1}")
day_before = today.strftime(f"%Y-%m-{day - 2}")

stock_parameter = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': 'TSLA',
    'interval': '60min',
    'apikey': STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, stock_parameter)
response.raise_for_status()
data = response.json()
yesterday_price = float(data['Time Series (Daily)'][yesterday]['4. close'])
day_before_price = float(data['Time Series (Daily)'][day_before]['4. close'])
price_difference = yesterday_price - day_before_price
price_procent = price_difference / yesterday_price * 100

news_parameter = {
    'q': 'tesla',
    'language': 'en',
    'from': 'us',
    'apiKey': NEWS_API_KEY
}

response = requests.get(NEWS_ENDPOINT, params=news_parameter)
response.raise_for_status()
data = response.json()
news_array = data['articles'][:3]

if price_procent < 0:
    news_layout = [f"\n📈TSLA:{round(price_procent)}%\n\n{newsarr['title']}\n\n{newsarr['description']}" for newsarr in news_array]
else:
    news_layout = [f"\n📉TSLA:{round(price_procent)}%\n\n{newsarr['title']}\n\n{newsarr['description']}" for newsarr in news_array]

client = Client(TWILIO_SID, TWILIO_AUTH)
for article in news_layout:
    if price_procent >= 5 or price_procent <= -5:
        message = client.messages \
            .create(body=article,
                    from_='+12107873196',
                    to='+310640709263'
                    )

        print(message.status)