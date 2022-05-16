import requests
from twilio.rest import Client
import datetime as date
from dotenv import load_dotenv
import os

load_dotenv()

ACC_SID = os.getenv("ACC_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
PHONE_NUM = os.getenv("PHONE_NUM")

STOCK_URL = "https://www.alphavantage.co/query"
NEWS_URL = "https://newsapi.org/v2/everything"

STOCK_API = os.getenv("STOCK_API")
NEWS_API = os.getenv("NEWS_API")

MY_PHONE_NUM = os.getenv("MY_PHONE_NUM")

STOCK_PARAMS = {
    "function": "TIME_SERIES_daily",
    "symbol": "IBM",
    "apikey": STOCK_API
}

news_params = {
    "apiKey": NEWS_API,
    "q": "IBM",
    "sources": "reuters",
    "from": date.datetime.now().date(),
    "language": "en"
}

news_response = requests.get(NEWS_URL, news_params)
news_data = news_response.json()["articles"]

#print(date.datetime.now().date())


stock_response = requests.get(STOCK_URL, STOCK_PARAMS)
stock_response.raise_for_status()
stock_data = stock_response.json()["Time Series (Daily)"]

data_list = [value for (key, value) in stock_data.items()]

opening_price = float(data_list[0]["1. open"])
closing_price = float(data_list[1]["4. close"])

percent_difference = abs(opening_price - closing_price) / abs(closing_price) * 100.0

percent = round(percent_difference, 2)

client = Client(ACC_SID, AUTH_TOKEN)

if len(news_data) > 0:
    news_title = news_data[0]["title"]
    news_url = news_data[0]["url"]

    if opening_price > closing_price:
        percent = percent * -1
        message = client.messages.create(
            body=f"Stock name: IBM\nPrice:{percent}\nNews Title: {news_title}\nNew URL: {news_url}",
            from_=PHONE_NUM,
            to=MY_PHONE_NUM
        )
    else:
        message = client.messages.create(
            body=f"Stock name: IBM\nPrice:{percent}\nNews Title: {news_title}\nNew URL: {news_url}",
            from_=PHONE_NUM,
            to=MY_PHONE_NUM
        )
else:
    if opening_price > closing_price:
        percent = percent * -1
        message = client.messages.create(
            body=f"Stock name: IBM\nPrice:{percent}\nNo News reported",
            from_=PHONE_NUM,
            to=MY_PHONE_NUM
        )
    else:
        message = client.messages.create(
            body=f"Stock name: IBM\nPrice:{percent}\nNo News reported",
            from_=PHONE_NUM,
            to=MY_PHONE_NUM
        )
