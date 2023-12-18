import customtkinter as ctk
from PIL import Image
from ctypes import windll, byref, sizeof, c_int
from weather import getWeather, getForecast, getWeatherMap
import json


# INITIALIZATION


window = ctk.CTk(fg_color='#3F68DD')
window.title('Weather')
window.geometry('1024x640')
window.iconbitmap('./icon.ico')

titlebar_color = 0x00DD683F
HWND = windll.user32.GetParent(window.winfo_id())
windll.dwmapi.DwmSetWindowAttribute(HWND,35,byref(c_int(titlebar_color)),sizeof(c_int))

colormodes = 'light', 'dark'
ctk.set_appearance_mode(colormodes[0])
#ctk.set_default_color_theme("./assets/theme/weathertheme.json")

scale = 0.125
weather_icons = {}
for code in ["01","02","03","04","09","10","11","13","50"]:
    for dn in ('d','n'):
        weather_icons[f'{code}{dn}'] = ctk.CTkImage(Image.open(f"assets/icons/{code}{dn}.png"),size=(1660*scale,1660*scale))

info01n = ctk.CTkImage(Image.open("assets/icons/info01n.png"),size=(20,20))
info01d = ctk.CTkImage(Image.open("assets/icons/info01d.png"),size=(20,20))
info02d = ctk.CTkImage(Image.open("assets/icons/info02d.png"),size=(25,20))
info02n = ctk.CTkImage(Image.open("assets/icons/info02n.png"),size=(25,20))
info03d = ctk.CTkImage(Image.open("assets/icons/info03d.png"),size=(22,20))
info03n = ctk.CTkImage(Image.open("assets/icons/info03n.png"),size=(22,20))


# CURRENT WEATHER


# Frame
weatherFrame = ctk.CTkFrame(window,fg_color='#C9E5FF',corner_radius=12)
weatherFrame.grid(row=0,column=0,padx=12,pady=12)

# Icon
weatherIconLabel = ctk.CTkLabel(
    weatherFrame,
    image=weather_icons['03d'],
    text=f'27°    ',
    font=('Plus Jakarta Sans', 60, 'bold'),
    text_color='#2B6398',
    compound='left')
weatherIconLabel.grid(row=0,column=0,padx=4,pady=4)

# Temperature
#weatherTemperatureLabel = ctk.CTkLabel(weatherFrame,)
#weatherTemperatureLabel.grid(row=0,column=1,padx=4,pady=4)

# Info Frame: wind, cloud, extra
weatherInfo = ctk.CTkFrame(weatherFrame,fg_color='transparent')
weatherInfo.grid(row=1,column=0,columnspan=3,padx=4,pady=24)

windInfoLabel = ctk.CTkLabel(weatherInfo,image=info01d,text='11 m/s',compound='top',font=('DM Sans', 16))
windInfoLabel.grid(row=0,column=0,padx=36,ipadx=4,ipady=4)

cloudInfoLabel = ctk.CTkLabel(weatherInfo,image=info02d,text='40%',compound='top',font=('DM Sans', 16))
cloudInfoLabel.grid(row=0,column=1,padx=36,ipadx=4,ipady=4)

humidityInfoLabel = ctk.CTkLabel(weatherInfo,image=info03d,text='88%',compound='top',font=('DM Sans', 16))
humidityInfoLabel.grid(row=0,column=2,padx=36,ipadx=4,ipady=4)


window.mainloop()
