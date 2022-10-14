import requests
from twilio.rest import Client
import os


using_lat = 33.306160
using_lon = -111.841248

OWM_Endpoint = "https://api.openweathermap.org/data/3.0/onecall"
api_key = os.environ.get("api_key")
account_sid = os.environ.get("account_sid")
auth_token = os.environ.get("auth_token")

weather_params = {
    "lat": using_lat,
    "lon": using_lon,
    "appid": api_key,
    "exclude": "current,minutely,daily,alerts",
    "units": "imperial",
}

response = requests.get(url=OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if condition_code < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
            body="It's going to rain today. Remember to bring an ☔",
            from_='+12675505424',
            to='+14806123427'
        )
    print(message.status)
