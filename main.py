import requests
import datetime as dt
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY ="******"
NEWS_API_KEY ="*********"
parameters = {
    "function": "TIME_SERIES_INTRADAY",
    "symbol": STOCK,
    "interval": "60min",
    "apikey": STOCK_API_KEY
}

# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
response = requests.get(url="https://www.alphavantage.co/query", params = parameters)
response.raise_for_status()
data = response.json()

yesterday = dt.date.today() - dt.timedelta(days=1)
day_before_yesterday = dt.date.today() - dt.timedelta(days=2)

yesterday_data = float(data["Time Series (60min)"][f"{yesterday} 16:00:00"]["4. close"])
day_before_yesterday_data = float(data["Time Series (60min)"][f"{day_before_yesterday} 16:00:00"]["4. close"])

five_percent = day_before_yesterday_data*0.001
if yesterday_data>day_before_yesterday_data+five_percent or yesterday_data<day_before_yesterday_data-five_percent:
    print("get news")

# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

parameters_news = {
    "q":"Tesla",
    "apiKey": NEWS_API_KEY,
}
responce_news = requests.get(url="https://newsapi.org/v2/top-headlines",params=parameters_news)
responce_news.raise_for_status()

news_data = responce_news.json()

if yesterday_data > day_before_yesterday_data:
    icon = "🔺"
else:
    icon = "🔻"
percent = abs(round(((yesterday_data/day_before_yesterday_data) - 1)*100))

print(news_data)

list_of_massages = []
for i in range(0,2):
    title = news_data["articles"][i]["title"]
    description = news_data["articles"][i]["description"]
    message =  (f"TSLA: {icon} {percent}%\nHedline:{title}\nBrief: {description}")
    list_of_massages.append(message)

for i in list_of_massages:
    print (i)




# STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

import os
from twilio.rest import Client


Find your Account SID and Auth Token at twilio.com/console
and set the environment variables. See http://twil.io/secure
account_sid = "*******"
auth_token = "*****"
client = Client(account_sid, auth_token)
for i in range(0,2):
    message = client.messages \
        .create(
                body=f"{list_of_massages[i]}",
                from_='*****',
                to='*****'
         )



#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

