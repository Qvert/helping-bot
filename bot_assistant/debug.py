'''from tzwhere import tzwhere
import pytz
import datetime
import requests

params = {
    'apikey': '0585a3a6-e7df-499d-83ea-573e16a5dd16',
    'kind': 'locality',
    'geocode': 'Чита',
    'format': 'json',
    'lang': 'ru_RU',
}

response = requests.get('https://geocode-maps.yandex.ru/1.x', params=params).json()
print(response)

tz_NY = pytz.timezone('Asia/Yakutsk')
datetime_NY = datetime.datetime.now(tz_NY)
print(datetime_NY)
'''
