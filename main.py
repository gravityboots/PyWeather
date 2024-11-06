# PyWeather (v4.5): A modern weather app in python using OpenWeatherMap Weather API, and customtkinter

from ctypes import windll, byref, sizeof, c_int
import sys, os
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from datetime import datetime
import requests
import webbrowser
from geopy.geocoders import Nominatim
import geopy
import random
import json

if getattr(sys, 'frozen', False):
    import pyi_splash # type: ignore # ignore this error, the module will be imported in the frozen executable


key = '460de012b0fd52774245f52ed38c4888'
#paid_key = 'bd5e378503939ddaee76f12ad7a97608'  # "startup" plan key; https://openweathermap.org/price


def resource_path(relative_path:str):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
 
    return os.path.join(base_path, relative_path)


def get_weather(lat:float|int, lon:float|int):
    response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?lat={lat:.4f}&lon={lon:.4f}&appid={key}')
    response = dict(response.json())
    return response


def get_forecast(lat:float|int, lon:float|int):
    response = requests.get(f'http://api.openweathermap.org/data/2.5/forecast?lat={lat:.4f}&lon={lon:.4f}&appid={key}')
    response = dict(response.json())    
    return response


class SideFrame(ctk.CTkFrame):
    def __init__(self,parent,fg_color):
        super().__init__(parent,fg_color=fg_color)  # method must be called to create widget instance

        # populate frame
        self.populate(parent.c,parent.icons,parent.fonts)

        # place frame
        self.place(relx=0.01,rely=0.01,relwidth=0.33,relheight=0.98)

    def populate(self,c,icons,fonts):
        # create widgets
        self.locationFrame = ctk.CTkFrame(self,fg_color='transparent')
        self.locationEntry = ctk.CTkEntry(self.locationFrame,font=fonts['e'],fg_color=(c['white'],c['dark_bg']),border_color=(c['white'],c['dark_bg']),placeholder_text='Enter location (e.g. Bangalore)')
        self.runButton = ctk.CTkButton(self.locationFrame,image=icons['run'],text='',width=16)
        self.locationButton = ctk.CTkButton(self.locationFrame,image=icons['location'],text='',width=16)

        self.weatherFrame = ctk.CTkFrame(self,fg_color='transparent')
        self.weatherIconLabel = ctk.CTkLabel(self.weatherFrame,fg_color='transparent',font=fonts['b'],text_color=(c['light_mfont'],c['dark_mfont']),image=icons['null'],text='')
        self.temperatureLabel = ctk.CTkLabel(self.weatherFrame,fg_color='transparent',font=fonts['b'],text_color=(c['light_bfont'],c['dark_bfont']),text='—')
        self.weatherTypeLabel = ctk.CTkLabel(self.weatherFrame,fg_color='transparent',font=fonts['s'],text_color=(c['light_mfont'],c['dark_mfont']),text='Enter a location to get\nits current weather.')

        self.timeFrame = ctk.CTkFrame(self,fg_color='transparent')
        self.timeLabel = ctk.CTkLabel(self.timeFrame,text='',font=fonts['s'],text_color=(c['light_sfont'],c['dark_sfont']))
        self.dayLabel = ctk.CTkLabel(self.timeFrame,text='',font=fonts['s'],text_color=(c['light_sfont'],c['dark_sfont']))
        self.locationLabel = ctk.CTkLabel(self.timeFrame,font=fonts['s'],text_color=(c['light_sfont'],c['dark_sfont']),text='')

        # place widgets
        self.locationFrame.pack(fill='x',side='top',pady=12)
        self.locationEntry.pack(expand=True,fill='x',side='left',anchor='w',padx=(25,2),pady=25)
        self.runButton.pack(side='right',anchor='e',padx=(0,25),pady=25)
        self.locationButton.pack(side='right',anchor='w',padx=0,pady=25)

        self.weatherFrame.pack(expand=True,fill='both')
        self.weatherIconLabel.pack(expand=True,padx=25)
        self.temperatureLabel.pack(padx=25)
        self.weatherTypeLabel.pack(padx=25,pady=(0,25))

        self.timeFrame.pack(fill='x',side='bottom',anchor='w',padx=25,pady=25)
        self.timeLabel.pack(anchor='w')
        self.dayLabel.pack(anchor='w')
        self.locationLabel.pack(anchor='w')


class MainFrame(ctk.CTkFrame):
    def __init__(self,parent,fg_color):
        super().__init__(parent,fg_color=fg_color) # method must be called to create widget instance

        # populate frame
        self.populate(parent.c,parent.icons,parent.fonts)

        # place frame
        self.place(relx=0.35,rely=0.01,relwidth=0.64,relheight=0.98)
    

    def populate(self,c,icons,fonts):
        # create options widgets
        self.optionsFrame = ctk.CTkFrame(self,fg_color=(c['light_box'],c['dark_box']))
        self.unitsMenu = ctk.CTkOptionMenu(
            self.optionsFrame,
            font=fonts['e'],
            text_color=(c['light_sfont'],c['dark_sfont']),
            fg_color=(c['light_frame'],c['dark_bg']),
            button_color=(c['light_frame'],c['dark_bg']),
            button_hover_color=(c['white'],c['dark_frame']),
            dropdown_font=fonts['e'],
            dropdown_fg_color=(c['white'],c['black']),
            dropdown_hover_color=c['blue'],
            dropdown_text_color=(c['black'],c['white']),
            values=['Metric (°C, km/h)','Metric (K, m/s)','Imperial (°F, mph)'],
            state='disabled'
        )
        self.hourFormatButton = ctk.CTkButton(
            self.optionsFrame,
            font=fonts['e'],
            text='12-Hour Format',
            width=14,
            text_color=(c['light_frame'],c['dark_sfont']),
            fg_color=(c['light_box'],c['dark_box']),
            border_width=1,
            border_color=(c['light_frame'],c['dark_frame']),
            hover_color=(c['light_bg'],c['dark_bg']),
            state='disabled'
        )
        self.colorModeButton = ctk.CTkButton(
            self.optionsFrame,
            font=fonts['e'],
            text='Light Mode',
            width=10,
            text_color=(c['light_frame'],c['dark_sfont']),
            fg_color=(c['light_box'],c['dark_box']),
            border_width=1,
            border_color=(c['light_frame'],c['dark_frame']),
            hover_color=(c['light_bg'],c['dark_bg'])
        )
        self.mapButton = ctk.CTkButton(
            self.optionsFrame,
            font=fonts['e'],
            text='Open Location ↗',
            width=15,
            text_color=(c['light_frame'],c['dark_sfont']),
            fg_color=(c['light_box'],c['dark_box']),
            border_width=1,
            border_color=(c['light_frame'],c['dark_frame']),
            hover_color=(c['light_bg'],c['dark_bg']),
            state='disabled'
        )
        self.weatherMapButton = ctk.CTkButton(
            self.optionsFrame,
            font=fonts['e'],
            text='Weather Map ↗',
            width=15,
            text_color=(c['light_frame'],c['dark_sfont']),
            fg_color=(c['light_box'],c['dark_box']),
            border_width=1,
            border_color=(c['light_frame'],c['dark_frame']),
            hover_color=(c['light_bg'],c['dark_bg']),
            state='disabled'
        )
        self.aboutButton = ctk.CTkButton(
            self.optionsFrame,
            font=fonts['e'],
            text='About',
            width=5,
            text_color=(c['light_sfont'],c['dark_sfont']),
            fg_color=(c['light_frame'],c['dark_bg']),
            hover_color=(c['white'],c['dark_frame'])
        )
        self.downloadButton = ctk.CTkButton(
            self.optionsFrame,
            font=fonts['e'],
            text='⬇️',
            width=1,
            text_color=(c['light_frame'],c['dark_sfont']),
            fg_color=(c['light_box'],c['dark_box']),
            border_width=1,
            border_color=(c['light_frame'],c['dark_frame']),
            hover_color=(c['light_bg'],c['dark_bg']),
            state='disabled'
        )

        # place options widgets
        self.optionsFrame.pack(fill='x',pady=(0,12))
        self.unitsMenu.pack(side='left',padx=6,pady=6)
        self.hourFormatButton.pack(side='left',padx=(0,6),pady=6)
        self.colorModeButton.pack(side='left',padx=(0,6),pady=6)
        self.mapButton.pack(side='left',padx=(0,6),pady=6)
        self.weatherMapButton.pack(side='left',padx=(0,6),pady=6)
        self.aboutButton.pack(side='right',padx=(0,6),pady=6)
        self.downloadButton.pack(side='right',padx=(0,6),pady=6)

        # create info widgets
        self.infoFrame = ctk.CTkFrame(self,fg_color='transparent')

        self.sunFrame = ctk.CTkFrame(self.infoFrame,fg_color=(c['light_frame'],c['dark_frame']))
        self.sunIconLabel = ctk.CTkLabel(self.sunFrame,image=icons['sun'],text='')
        self.sunLabel = ctk.CTkLabel(self.sunFrame,font=fonts['s'],text_color=(c['light_mfont'],c['dark_mfont']),text='Rise ——\nSet ——')

        self.windFrame = ctk.CTkFrame(self.infoFrame,fg_color=(c['light_frame'],c['dark_frame']))
        self.windIconLabel = ctk.CTkLabel(self.windFrame,image=icons['wind'],text='')
        self.windLabel = ctk.CTkLabel(self.windFrame,font=fonts['s'],text_color=(c['light_mfont'],c['dark_mfont']),text='Wind\n——')

        self.humidityFrame = ctk.CTkFrame(self.infoFrame,fg_color=(c['light_frame'],c['dark_frame']))
        self.humidityIconLabel = ctk.CTkLabel(self.humidityFrame,image=icons['drop'],text='')
        self.humidityLabel = ctk.CTkLabel(self.humidityFrame,font=fonts['s'],text_color=(c['light_mfont'],c['dark_mfont']),text='Humidity\n——')

        self.cloudFrame = ctk.CTkFrame(self.infoFrame,fg_color=(c['light_frame'],c['dark_frame']))
        self.cloudIconLabel = ctk.CTkLabel(self.cloudFrame,image=icons['cloud'],text='')
        self.cloudLabel = ctk.CTkLabel(self.cloudFrame,font=fonts['s'],text_color=(c['light_mfont'],c['dark_mfont']),text='Cloud Cover \n——')

        # place info widgets
        self.infoFrame.pack(fill='both',pady=(0,12))

        self.sunFrame.pack(expand=True,fill='both',side='left',padx=(0,12))
        self.sunIconLabel.pack(padx=25,pady=25)
        self.sunLabel.pack(padx=25,pady=(0,25))

        self.windFrame.pack(expand=True,fill='both',side='left',padx=(0,12))
        self.windIconLabel.pack(padx=25,pady=25)
        self.windLabel.pack(padx=25,pady=(0,25))

        self.humidityFrame.pack(expand=True,fill='both',side='left',padx=(0,12))
        self.humidityIconLabel.pack(padx=25,pady=25)
        self.humidityLabel.pack(padx=25,pady=(0,25))

        self.cloudFrame.pack(expand=True,fill='both',side='left',padx=0)
        self.cloudIconLabel.pack(padx=25,pady=25)
        self.cloudLabel.pack(padx=25,pady=(0,25))

        # create & place forecast widgets
        self.forecastsFrame = ctk.CTkScrollableFrame(
            self,
            fg_color=(c['light_box'],c['dark_box']),
            scrollbar_button_color=(c['light_bg'],c['dark_bg']),
            scrollbar_button_hover_color=(c['white'],c['dark_sfont'])
        )
        self.forecastsFrame.pack(expand=True,fill='both')

        self.forecasts = {} # create all 40 weather forecast frames & widgets in a dictionary for easy of access, and remaining modular
        for i in range(40):
            self.forecasts[i] = ForecastFrame(self.forecastsFrame,(c['light_frame'],c['dark_frame']),c,icons,fonts)


class ForecastFrame(ctk.CTkFrame):  # forecast frame to modularize creation of all 40 weather forecast reports
    def __init__(self,parent,fg_color,c,icons,fonts):
        super().__init__(parent,fg_color=fg_color)  # method must be called to create widget instance

        self.grid_columnconfigure(2,weight=3)  # configure frame layout (using grid geometry manager)

        # populate frame: create widgets
        self.forecastIconLabel = ctk.CTkLabel(self,text='',image=icons['null_small'])
        self.forecastTimeLabel = ctk.CTkLabel(self,font=fonts['s'],text_color=(c['light_sfont'],c['dark_sfont']),text='')
        self.forecastTypeLabel = ctk.CTkLabel(self,font=fonts['s'],text_color=(c['light_mfont'],c['dark_mfont']),text='——')
        self.forecastDataLabel = ctk.CTkLabel(self,font=fonts['s'],text_color=(c['light_sfont'],c['dark_sfont']),text='')

        # populate frame: place widgets
        self.forecastIconLabel.grid(row=0,column=0,padx=(12,0))
        self.forecastTimeLabel.grid(row=0,column=1)
        self.forecastTypeLabel.grid(row=0,column=2)
        self.forecastDataLabel.grid(row=0,column=3,padx=(0,25))

        # place frame
        self.pack(expand=True,fill='x',pady=(0,6))


class AboutWindow(ctk.CTkToplevel):  # toplevel window for information about the app
    def __init__(self,parent,c,icons,fonts):
        super().__init__(parent)  # method must be called to create widget instance
        self.title('About PyWeather')
        self.minsize(640,512)
        self.attributes('-topmost', True)
        self.update()

        self.aboutWindowFrame = ctk.CTkScrollableFrame(self,fg_color='transparent')
        self.aboutWindowFrame.pack(expand=True,fill='both')

        self.titleLabel = ctk.CTkLabel(self.aboutWindowFrame,font=fonts['r'],text='PyWeather (v4.5)',image=icons['11n'],compound='top')
        self.titleLabel.pack(expand=True,fill='both',padx=25,pady=25)

        self.textbox = ctk.CTkTextbox(self.aboutWindowFrame,font=fonts['s'],fg_color='transparent',wrap='word',height=1920)
        self.textbox.pack(expand=True,fill='both',padx=25,pady=(0,25))
        self.textbox.insert('0.0','''
A modern weather app built in python (compatible with Python 3.10 onwards), using the customtkinter library by Tom Schimansky, with data sourced from OpenWeather current weather, and 5-day, 3-hour weather forecast APIs.

To use the app, simply type in either the desired city/locality name or coordinates (as latitude, longitude) into the search bar and run via the button, or by pressing return. Upon a successful geocoding of the location (using the geopy module's Nominatim geocoder for OpenSreetMap's address data) you will find many details about the current weather info, local time and basic info about the weather for the next 5 days at 3-hour intervals. In each forecast, the probability of precipitation (PoP) is given for the sake of accuracy.

The app will automatically convert to light/dark mode depending on the time of day in the given location, however you can change the colour mode from the toolbar at the top of the application. From the toolbar you can also choose to customise the units used from a dropdown menu, and toggle between clock-hour formats from a button as well as display some information. If the location result is successful you can also click on the "Open Location ↗" button to check the location on google maps, or the "Weather Map ↗" button to find a detailed and interactive weather map for precipitation, clouds, et cetera.

It is possible that when searching for the location, the app will raise an error which can be due to several possible reasons. Here are some possible error cases:
1. No location entered (user will be prompted with 'Please provide a location.')
2. Invalid location/coordinates entered (user will be prompted with 'Could not get location!')
3. No internet connection/request timed out (user will be prompted with 'No connection!')

The source code for this project can be found at https://github.com/gravityboots/PyWeather.                   


[ Data Attribution ]

Weather data sourced from OpenWeatherMap
https://api.openweathermap.org

Geocoding by geopy and OpenStreetMap
https://pypi.org/project/geopy

App built using Tom Schimansky's CustomTkinter
https://customtkinter.tomschimansky.com

Weather icons sourced from Bilal Arve on Figma
https://www.figma.com/community/file/1126777451931792118
(Icons have been added and tweaked in good faith.)''')
        self.textbox.configure(state="disabled")


class App(ctk.CTk):
    def __init__(self):


        # WINDOW INITALIZATION


        # app colors
        self.c = {
            'light_bg':'#91B3D2',
            'dark_bg':'#0F1C3D',
            'light_frame':'#C8E4FE',
            'dark_frame':'#1F2E54',
            'light_box':'#6B92B2',
            'dark_box':'#000C2B',
            'light_bfont':'#296399',
            'dark_bfont':'#E2E3E8',
            'light_mfont':'#3A72A3',
            'dark_mfont':'#8497C9',
            'light_sfont':'#658CAF',
            'dark_sfont':'#5972B2',
            'white':'#FFFFFF',
            'black':'#000000',
            'blue':'#3F68DA',
        }

        # app window initialization
        super().__init__(fg_color=(self.c['light_bg'],self.c['dark_bg']))
        self.title('PyWeather')
        self.minsize(1200,720)  # Originally 512x300, can work on adding responsive GUI in the future
        self.iconbitmap(resource_path('assets/nighticon.ico'))
        self.bind_all("<Button-1>", lambda event: event.widget.focus_set())  # lets the user defocus from entry widget

        # app fonts
        self.fonts = {
            'b': ctk.CTkFont('Plus Jakarta Sans',60,'bold'),
            'r': ctk.CTkFont('Plus Jakarta Sans',36,'bold'),
            'm': ctk.CTkFont('DM Sans',25),
            's': ctk.CTkFont('Space Mono',16),
            'e': ctk.CTkFont('Space Mono',12),
        }

        # app light & dark modes
        self.colormodes = 'light', 'dark'
        self.colormode = self.colormodes[1]
        ctk.set_appearance_mode(self.colormode)

        # interact with windows's window-attributes to change titlebar color
        self.titlecolors = 0x00D2B391, 0x003D1C0F
        self.titlecolor = self.titlecolors[1]
        self.HWND = windll.user32.GetParent(self.winfo_id())
        windll.dwmapi.DwmSetWindowAttribute(self.HWND,35,byref(c_int(self.titlecolor)),sizeof(c_int))

        # app icons
        scale1 = 0.1875
        scale2 = 0.125
        scale3 = 0.0625

        self.icons = {}
        for code in ["01","02","03","04","09","10","11","13","50"]:
            for dn in ('d','n'):
                self.icons[f'{code}{dn}'] = ctk.CTkImage(Image.open(resource_path(f"assets/{code}{dn}.png")),size=(1660*scale1,1660*scale1))
                self.icons[f'{code}{dn}_small'] = ctk.CTkImage(Image.open(resource_path(f"assets/{code}{dn}.png")),size=(1660*scale3,1660*scale3))
        
        self.icons['null'] = ctk.CTkImage(
            Image.open(resource_path(f"assets/null.png")),
            size=(1660*scale1,1660*scale1)
        )
        self.icons['null_small'] = ctk.CTkImage(
            Image.open(resource_path(f"assets/null.png")),
            size=(1660*scale3,1660*scale3)
        )
        self.icons['sun'] = ctk.CTkImage(
            light_image=Image.open(resource_path(f"assets/sun_d.png")),
            dark_image=Image.open(resource_path(f"assets/sun_n.png")),
            size=(512*scale2,320*scale2)
        )
        self.icons['wind'] = ctk.CTkImage(
            light_image=Image.open(resource_path(f"assets/wind_d.png")),
            dark_image=Image.open(resource_path(f"assets/wind_n.png")),
            size=(320*scale2,320*scale2)
        )
        self.icons['drop'] = ctk.CTkImage(
            light_image=Image.open(resource_path(f"assets/drop_d.png")),
            dark_image=Image.open(resource_path(f"assets/drop_n.png")),
            size=(240*scale2,320*scale2)
        )
        self.icons['cloud'] = ctk.CTkImage(
            light_image=Image.open(resource_path(f"assets/cloud_d.png")),
            dark_image=Image.open(resource_path(f"assets/cloud_n.png")),
            size=(400*scale2,320*scale2)
        )
        self.icons['run'] = ctk.CTkImage(
            Image.open(resource_path(f"assets/run.png")),
            size=(15,15)
        )
        self.icons['location'] = ctk.CTkImage(
            Image.open(resource_path(f"assets/location.png")),
            size=(15,15)
        )

        # create frames for window — where all the widgets are created
        self.side_frame = SideFrame(self,(self.c['light_frame'],self.c['dark_frame']))
        self.main_frame = MainFrame(self,'transparent')
        self.about_window = None

        # create geolocator (before calling update function)
        self.geolocator = Nominatim(user_agent="PyWeather")


        # FUNCTIONS


        # light-dark mode toggle function
        def toggle_color_mode():
            if self.colormode==self.colormodes[0]:
                self.colormode = self.colormodes[1]
                self.titlecolor = self.titlecolors[1]
                self.iconbitmap(resource_path('assets/nighticon.ico'))
                self.main_frame.colorModeButton.configure(text='Light Mode')
            else:
                self.colormode = self.colormodes[0]
                self.titlecolor = self.titlecolors[0]
                self.iconbitmap(resource_path('assets/dayicon.ico'))
                self.main_frame.colorModeButton.configure(text='Dark Mode')

            windll.dwmapi.DwmSetWindowAttribute(self.HWND,35,byref(c_int(self.titlecolor)),sizeof(c_int))
            ctk.set_appearance_mode(self.colormode)


        # toggle units functions
        self.unit_scheme = 'Metric (°C, km/h)'


        def toggle_units(scheme):
            self.unit_scheme = scheme
            update(None)


        def format_units(value, quantity):
            if quantity=='T': # convert temperature from metric-kelvin into current unit scheme
                if self.unit_scheme=='Metric (°C, km/h)':
                    return f"{int(value-273.15)}°"
                elif self.unit_scheme=='Imperial (°F, mph)':
                    return f"{int((1.8*(value-273.15))+32)}°"
                else:
                    return f"{int(value)}K"

            elif quantity=='V': # convert velocity from metric-m/s into current unit scheme
                if self.unit_scheme=='Metric (°C, km/h)':
                    return f"{value*3.6:.2f}km/h"
                elif self.unit_scheme=='Imperial (°F, mph)':
                    return f"{value*2.2369362920544:.2f}mph"
                else:
                    return f"{value:.2f}m/s"

            else: return None


        # toggle clock hour format function
        self.hour_format = 24


        def toggle_hour_format():
            if self.hour_format==24:
                self.hour_format = 12
                self.main_frame.hourFormatButton.configure(text='24-Hour Format')
            else:
                self.hour_format = 24
                self.main_frame.hourFormatButton.configure(text='12-Hour Format')
            update(None)


        # open map function
        def open_map():
            try:
                webbrowser.open(f"https://www.google.com/maps/place/{self.location.latitude},{self.location.longitude}")
            except:
                self.main_frame.mapButton.configure(state='disabled')


        # open weather map function
        def open_weather_map():
            try:
                webbrowser.open(f"https://openweathermap.org/weathermap?basemap=map&cities=false&layer=precipitation&lat={self.location.latitude}&lon={self.location.longitude}")
            except:
                self.main_frame.weatherMapButton.configure(state='disabled')
        

        def download_data():
            try:
                time = datetime.now().strftime('%Y-%m-%d %H%M%S')
                cwd = "/".join(os.getcwd().split("\\"))
                path = f'{cwd}/{time}.txt'
                with open(path,'w') as file:
                    file.writelines((
                        f'LOCATION: {self.location}',
                        f'\nTIME & DATE: {datetime.now().strftime("%Y-%m-%d at %H:%M:%S")}',
                        f'\n\nCURRENT WEATHER:\n{json.dumps(self.weather, indent=4)}',
                        f'\n\nWEATHER FORECAST:\n{json.dumps(self.forecast, indent=4)}',
                    ))
                messagebox.showinfo('Successful Download',f'The weather data has been saved to "{path}".')
            except Exception as exc:
                if os.path.exists(path): os.remove(path)
                else: pass
                messagebox.showerror('Download failed',f'The weather data could not be saved!\n{str(type(exc))[8:-2]}: {exc}')


        # open about window function
        def open_about_window():
            if self.about_window is None or not self.about_window.winfo_exists():
                self.about_window = AboutWindow(self,self.c,self.icons,self.fonts)  # create window if its None or destroyed
            else:
                self.about_window.focus()  # if window exists focus it


        # update the app widgets functions (core of the app's working)
        self.weather = {'cod':0,'message':'Initialising...'}
        self.forecast = {}
        self.location = None


        def update(use_ip):  # main function that updates all the app widgets with weather & forecast data
            
            try:
                if use_ip:
                    ip_located = dict(requests.get('http://ipinfo.io/json').json())['city']
                    self.location = self.geolocator.geocode(ip_located,addressdetails=True,language='en')
                    self.side_frame.locationEntry.delete(0,len(self.side_frame.locationEntry.get()))
                    self.side_frame.locationEntry.insert(0,ip_located)
                else:
                    self.location = self.geolocator.geocode(self.side_frame.locationEntry.get(),addressdetails=True,language='en')
                
                if self.location is not None:
                    self.weather = get_weather(self.location.latitude, self.location.longitude)
                    self.forecast = get_forecast(self.location.latitude, self.location.longitude)
                    forecast_temperatures = [self.forecast['list'][i]['main']['temp'] for i in range(8)] + [self.weather['main']['temp']]
                    self.daily = {'min':min(forecast_temperatures),'max':max(forecast_temperatures)}
                elif self.side_frame.locationEntry.get()=='':
                    self.weather = {'cod':404,'message':'Please provide a location.'}
                    self.forecast = {}
                    self.daily = {}
                else:
                    self.weather = {'cod':404,'message':'Could not get location!'}
                    self.forecast = {}
                    self.daily = {}
            except (requests.exceptions.ConnectionError, geopy.exc.GeocoderUnavailable) as e:
                self.weather = {'cod':504,'message':'No connection!'} # HTTP gateway timeout error code: 504
                self.forecast = {}
                self.daily = {}
                print(f'\nCONNECTION ERROR! {type(e)} -> {e}')
            except Exception as e:
                self.weather = {'cod':500,'message':'Skill issue.'} # generic internal server error code: 500
                self.forecast = {}
                self.daily = {}
                print(f'\nERROR CAPTURED WHILE RUNNING! {type(e)} -> {e}')
                           
            if self.weather['cod']==200:  # 200 is the success, code; error codes such as 404, 400, etc. will not yield any data
                self.main_frame.unitsMenu.configure(state='normal')
                self.main_frame.hourFormatButton.configure(state='normal')
                self.main_frame.mapButton.configure(state='normal')
                self.main_frame.weatherMapButton.configure(state='normal')
                self.main_frame.downloadButton.configure(state='normal')

                self.side_frame.weatherIconLabel.configure(image=self.icons[self.weather['weather'][0]['icon']])
                self.side_frame.temperatureLabel.configure(text=format_units(self.weather['main']['temp'],quantity='T'))
                self.side_frame.weatherTypeLabel.configure(font=self.fonts['m'],text=f'''{self.weather['weather'][0]['description'].title()}, {format_units(self.daily['min'],quantity='T')} to {format_units(self.daily['max'],quantity='T')}''')
                
                if self.weather['timezone']%3600==0:
                    if self.weather['timezone']>=0:
                        tz = f"UTC+{self.weather['timezone']//3600}:00"
                    else:
                        tz = f"UTC-{abs(self.weather['timezone'])//3600}:00"
                else:
                    if self.weather['timezone']>=0:
                        tz = f"UTC+{self.weather['timezone']//3600}:{self.weather['timezone']%3600//60}"
                    else:
                        tz = f"UTC-{abs(self.weather['timezone'])//3600}:{abs(self.weather['timezone'])%3600//60}"
                try:
                    if self.location.raw['name'] == self.location.raw['address']['country']:
                        self.side_frame.locationLabel.configure(text=f"{self.location.raw['address']['country']} ({tz})")
                    else:
                        self.side_frame.locationLabel.configure(text=f"{self.location.raw['name']}, {self.location.raw['address']['country']} ({tz})")
                except:
                    self.side_frame.locationLabel.configure(text=f"{self.location.raw['display_name']} ({tz})")

                if self.hour_format==12:
                    self.main_frame.sunLabel.configure(text=f'''
Rise {datetime.utcfromtimestamp(self.weather['sys']['sunrise']+self.weather['timezone']).strftime('%I:%M%p')}
Set {datetime.utcfromtimestamp(self.weather['sys']['sunset']+self.weather['timezone']).strftime('%I:%M%p')}''')
                else:
                    self.main_frame.sunLabel.configure(text=f'''
Rise {datetime.utcfromtimestamp(self.weather['sys']['sunrise']+self.weather['timezone']).strftime('%H:%M')}
Set {datetime.utcfromtimestamp(self.weather['sys']['sunset']+self.weather['timezone']).strftime('%H:%M')}''')

                wind_direction = self.weather['wind']['deg']
                if 337.5 < wind_direction or wind_direction <= 22.5:
                    wind_direction = 'North (↑)'
                elif 22.5 < wind_direction <= 67.5:
                    wind_direction = 'North-East (↗)'
                elif 67.5 < wind_direction <= 112.5:
                    wind_direction = 'East (→)'
                elif 112.5 < wind_direction <= 157.5:
                    wind_direction = 'South-East (↘)'
                elif 157.5 < wind_direction <= 202.5:
                    wind_direction = 'South (↓)'
                elif 202.5 < wind_direction <= 247.5:
                    wind_direction = 'South-West (↙)'
                elif 247.5 < wind_direction <= 292.5:
                    wind_direction = 'West (←)'
                elif 292.5 < wind_direction <= 337.5:
                    wind_direction = 'North-West (↖)'
                else:
                    wind_direction = '—'

                self.main_frame.windLabel.configure(text=f"\n{format_units(self.weather['wind']['speed'],quantity='V')} Wind\n{wind_direction}")
                self.main_frame.humidityLabel.configure(text=f"\nHumidity\n{self.weather['main']['humidity']}%")
                self.main_frame.cloudLabel.configure(text=f"\nCloud Cover\n{self.weather['clouds']['all']}%")

                local_tz_offset = datetime.now().astimezone().tzinfo.utcoffset(None).total_seconds()  # gives number of seconds local time is offset from UTC
                for r in range(40):
                    if self.hour_format==12:
                        strtime = datetime.fromtimestamp(self.forecast['list'][r]['dt']-local_tz_offset+self.weather['timezone']).strftime('%A, %I:%M%p')
                    else:
                        strtime = datetime.fromtimestamp(self.forecast['list'][r]['dt']-local_tz_offset+self.weather['timezone']).strftime('%A, %H:%M')
                    self.main_frame.forecasts[r].forecastIconLabel.configure(image=self.icons[f"{self.forecast['list'][r]['weather'][0]['icon']}_small"])
                    self.main_frame.forecasts[r].forecastTimeLabel.configure(text=strtime)
                    self.main_frame.forecasts[r].forecastTypeLabel.configure(text=self.forecast['list'][r]['weather'][0]['description'].title())
                    self.main_frame.forecasts[r].forecastDataLabel.configure(text=f"(PoP {int(self.forecast['list'][r]['pop']*100)}%) {format_units(self.forecast['list'][r]['main']['temp'],quantity='T')}")

                if self.weather['weather'][0]['icon'][2]=='d':
                    if self.colormode==self.colormodes[1]:
                        toggle_color_mode()
                else:
                    if self.colormode==self.colormodes[0]:
                        toggle_color_mode()

            else:
                self.main_frame.unitsMenu.configure(state='disabled')
                self.main_frame.hourFormatButton.configure(state='disabled')
                self.main_frame.mapButton.configure(state='disabled')
                self.main_frame.weatherMapButton.configure(state='disabled')
                self.main_frame.downloadButton.configure(state='disabled')

                self.side_frame.weatherIconLabel.configure(image=self.icons['null'])
                self.side_frame.weatherTypeLabel.configure(font=self.fonts['s'],text=self.weather['message'])
                self.side_frame.temperatureLabel.configure(text=random.choice(('¯\(°_o)/¯', '(。﹏。)', '(´。＿。｀)','＞﹏＜','⊙.☉','(˘･_･˘)','>_<',':/')))
                self.side_frame.locationLabel.configure(text='')

                self.main_frame.sunLabel.configure(text='Rise ——\nSet ——')
                self.main_frame.windLabel.configure(text='Wind\n——')
                self.main_frame.humidityLabel.configure(text='Humidity\n——')
                self.main_frame.cloudLabel.configure(text='Cloud Cover \n——')

                for r in range(40):
                    self.main_frame.forecasts[r].forecastIconLabel.configure(image=self.icons['null_small'])
                    self.main_frame.forecasts[r].forecastTimeLabel.configure(text='')
                    self.main_frame.forecasts[r].forecastTypeLabel.configure(text='——')
                    self.main_frame.forecasts[r].forecastDataLabel.configure(text='')


        def update_time():  # constantly update local time, timezone and location display
            if self.weather['cod']==200:

                self.time = datetime.fromtimestamp(datetime.utcnow().timestamp()+self.weather['timezone'])
                self.side_frame.dayLabel.configure(text=self.time.strftime('%A, %e %B %Y'))
                if self.hour_format==12:
                    self.side_frame.timeLabel.configure(text=self.time.strftime("%I:%M:%S%p"))
                else:
                    self.side_frame.timeLabel.configure(text=self.time.strftime("%H:%M:%S"))

            else:
                self.side_frame.dayLabel.configure(text='')
                self.side_frame.timeLabel.configure(text='')

            self.side_frame.after(1000, update_time)


        # configure and bind functions to widgets that were created before any functions was defined
        self.main_frame.colorModeButton.configure(command=toggle_color_mode)
        self.main_frame.hourFormatButton.configure(command=toggle_hour_format)
        self.main_frame.unitsMenu.configure(command=toggle_units)
        self.main_frame.mapButton.configure(command=open_map)
        self.main_frame.weatherMapButton.configure(command=open_weather_map)
        self.main_frame.downloadButton.configure(command=download_data)
        self.main_frame.aboutButton.configure(command=open_about_window)
        self.side_frame.runButton.configure(command=lambda: update(None))
        self.side_frame.locationButton.configure(command=lambda: update(True))
        self.side_frame.locationEntry.bind("<Return>",lambda event: update(None),add='+')


        update_time()

        # run the app
        self.mainloop()


if getattr(sys, 'frozen', False):
    pyi_splash.close()

if __name__ == '__main__':
    app = App()
