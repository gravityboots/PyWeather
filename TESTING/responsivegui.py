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



window.mainloop()
