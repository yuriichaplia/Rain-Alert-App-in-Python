import requests
from os import environ
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

parameters = {
    "lat": float(environ.get("LAT")),
    "lon": float(environ.get("LON")),
    "appid": environ.get("APP_ID"),
    "cnt": 4
}

account_sid = environ.get("ACCOUNT_SID")
auth_token = environ.get("AUTH_TOKEN")

data = requests.get(url="https://api.openweathermap.org/data/2.5/forecast", params=parameters)
data.raise_for_status()
status = data.status_code
data = data.json()

print(f"Status code: {status}")
print(data)

will_rain = False
for element in data['list']:
    if element['weather'][0]['id'] < 2000:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.api.account.messages.create(
        from_ = environ.get("TWILIO_NUMBER"),
        body='今日は雨が降りそうです。傘を忘れないでくださいね！',
        to=environ.get("PHONE_NUMBER")
    )

    print(message.status)