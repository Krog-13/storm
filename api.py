import requests
import json
import api_key

CONVERT_BAR = 0.75
api_url = 'https://api.weatherbit.io/v2.0/forecast/daily'

def city(name='Petropavlovsk'):
    params = {
        'city': name,
        'country': 'KZ',
        'lang': 'eu',
        'days': 16,
        'key': api_key.TOKEN
    }
    res = requests.get(api_url, params=params)
    weather = res.json()
    return weather

def send_weather(day, town='Astana'):
    '''
    :param day: inspect of date
    :return: list of weather parametrs:
    temp - average temperature
    pop - probablity of precipitation
    pres - average pressure
    rh - average relative humidity
    '''
    weather = city(town)
    weather_param = ['temp', 'pop', 'rh', 'valid_date', 'pres']
    weather_data = []
    for param in weather_param:
        weather_data.append(str(weather['data'][day][param]))
    #Преобразуем милибар в мм рт.ст.
    pres = weather_data.pop()
    pres = float(pres)*CONVERT_BAR
    weather_data.append(int(pres))
    return weather_data
