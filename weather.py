import requests
import json
from datetime import datetime
from numpy import round


def localTime(utc_with_tz):
    local_time = datetime.utcfromtimestamp(utc_with_tz)
    return local_time.time()


def getWeather(place):
    response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={place}&appid=460de012b0fd52774245f52ed38c4888')
    response = response.json()
    
    if response['cod']==200:
        temperature = round((response['main']['temp'] - 273.15),2)
        feels_like_temp = round((response['main']['feels_like'] - 273.15),2)
        pressure = response['main']['pressure']
        humidity = response['main']['humidity']
        wind = response['wind']['speed']
        timezone = response['timezone']
        sunrise = localTime(response['sys']['sunrise'] + timezone)
        sunset = localTime(response['sys']['sunset'] + timezone)
        cloudy = response['clouds']['all']
        description = response['weather'][0]['description']

        weather = place, temperature, feels_like_temp, pressure ,humidity, sunrise, sunset, cloudy, wind, description

    else:
        weather = response['cod'], response['message']
    
    return weather


def getForecast(place):
    response = requests.get(f'http://api.openweathermap.org/data/2.5/forecast?q={place}&appid=460de012b0fd52774245f52ed38c4888')
    response = response.json()
    
    if response['cod']==200:
        temperature = int(response['main']['temp'] - 273)
        feels_like_temp = int(response['main']['feels_like'] - 273)
        pressure = response['main']['pressure']
        humidity = response['main']['humidity']
        wind = response['wind']['speed']
        timezone = response['timezone']
        sunrise = localTime(response['sys']['sunrise'] + timezone)
        sunset = localTime(response['sys']['sunset'] + timezone)
        cloudy = response['clouds']['all']
        description = response['weather'][0]['description']

        weather = place, temperature, feels_like_temp, pressure ,humidity, sunrise, sunset, cloudy, wind, description

    else:
        weather = response['cod'], response['message']
    
    return weather


def getWeatherMap(x, y, z, layer):
    pass


print(datetime.utcfromtimestamp(1702922166+19800))
