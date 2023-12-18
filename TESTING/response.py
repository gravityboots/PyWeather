import requests
from weather import getWeather

#response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={input("City: ")}&appid=460de012b0fd52774245f52ed38c4888')
#response = response.json()

#print(response)

print(getWeather('Bangalore,IN'))