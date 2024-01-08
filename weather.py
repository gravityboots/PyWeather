# PyWeather™: A modern weather app in python using OpenWeather API, and customtkinter

import requests
from datetime import datetime


def get_weather(place):
    response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={place}&appid=460de012b0fd52774245f52ed38c4888')
    response = response.json()
    return response


def get_forecast(place):
    response = requests.get(f'http://api.openweathermap.org/data/2.5/forecast?q={place}&appid=460de012b0fd52774245f52ed38c4888')
    response = response.json()    
    return response
