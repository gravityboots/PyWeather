# Source: https://www.askpython.com/python/examples/gui-weather-app-in-python

from tkinter import *
import requests
import json
from datetime import datetime

# WINDOW INITIALIZATION
root = Tk()
root.title("Weather App - AskPython.com")
root.geometry("400x400")
root.resizable(0,0)


# FUNCTIONS
def time_format_for_location(utc_with_tz):
    local_time = datetime.utcfromtimestamp(utc_with_tz)
    return local_time.time()

city = StringVar()

def showWeather():
    #Enter you api key, copies from the OpenWeatherMap dashboard
    api_key = "460de012b0fd52774245f52ed38c4888"  # MY API: 460de012b0fd52774245f52ed38c4888
  
    # API url
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
 
    # Get the response from fetched url
    response = requests.get(weather_url)
 
    # changing response from json to python readable 
    weather_info = response.json()
 
 
    outputText.delete("1.0", "end")   #to clear the text field for every new output
 
#as per API documentation, if the cod is 200, it means that weather data was successfully fetched
 
 
    if weather_info['cod'] == 200:
        kelvin = 273 # value of kelvin
 
#-----------Storing the fetched values of weather of a city
 
        temp = int(weather_info['main']['temp'] - kelvin)                                     #converting default kelvin value to Celcius
        feels_like_temp = int(weather_info['main']['feels_like'] - kelvin)
        pressure = weather_info['main']['pressure']
        humidity = weather_info['main']['humidity']
        wind_speed = weather_info['wind']['speed'] * 3.6
        sunrise = weather_info['sys']['sunrise']
        sunset = weather_info['sys']['sunset']
        timezone = weather_info['timezone']
        cloudy = weather_info['clouds']['all']
        description = weather_info['weather'][0]['description']
 
        sunrise_time = time_format_for_location(sunrise + timezone)
        sunset_time = time_format_for_location(sunset + timezone)
 
#assigning Values to our weather varaible, to display as output
         
        weather = f"\nWeather of: {city}\nTemperature: {temp}°C\nFeels like: {feels_like_temp}°C\nPressure: {pressure} hPa\nHumidity: {humidity}%\nSunrise at {sunrise_time} and Sunset at {sunset_time}\nCloud: {cloudy}%\nInfo: {description}"
    else:
        weather = f"\n\tWeather for '{city}' not found!\n\tKindly Enter valid City Name !!"
 
 
 
    outputText.insert(INSERT, weather)   #to insert or send value in our Text Field to display output


# INTERFACE

# Location Input
cityLabel = Label(root,text='Enter City, EG (where EG is country code)',font=('Arial',12,'bold')).pack(pady=10)
cityEntry = Entry(root,width=24,font='Arial 14 bold').pack()

# Check weather button
checkButton = Button(root,command=showWeather,text="Check Weather",font="Arial 10",bg='lightblue',fg='black',activebackground="teal",padx=5,pady=5).pack(pady=20)

# Output textbox
weatherLabel = Label(root,text="The Weather is:",font='arial 12 bold').pack(pady=10)
outputText = Text(root,width=46,height=10).pack()


root.mainloop()