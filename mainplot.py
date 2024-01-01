import customtkinter as ctk
from PIL import Image
from ctypes import windll, byref, sizeof, c_int
from weather import getWeather, getForecast
from datetime import datetime
import random
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SideFrame(ctk.CTkFrame): # Don't make this a scrollable frame, the weather frame doesn't expand
    def __init__(self, parent, fg_color):
        super().__init__(parent,fg_color=fg_color)

        # populate frame
        self.populate(parent.c,parent.icons,parent.bfont,parent.mfont,parent.sfont,parent.efont)

        # place frame
        self.place(relx=0.01,rely=0.01,relwidth=0.33,relheight=0.98)
    
    def populate(self,c,icons,bfont,mfont,sfont,efont):
        # create widgets
        self.locationFrame = ctk.CTkFrame(self,fg_color='transparent')
        self.locationEntry = ctk.CTkEntry(self.locationFrame,font=efont,fg_color=(c['white'],c['dark_bg']),border_color=(c['white'],c['dark_bg']),placeholder_text='Enter city (e.g. London, GB)')
        self.runButton = ctk.CTkButton(self.locationFrame,image=icons['run'],text='',width=16)

        self.weatherFrame = ctk.CTkFrame(self,fg_color='transparent')
        self.weatherIconLabel = ctk.CTkLabel(self.weatherFrame,fg_color='transparent',font=bfont,text_color=(c['light_mfont'],c['dark_mfont']),image=icons['null'],text='')
        self.temperatureLabel = ctk.CTkLabel(self.weatherFrame,fg_color='transparent',font=bfont,text_color=(c['light_bfont'],c['dark_bfont']),text='—')
        self.weatherTypeLabel = ctk.CTkLabel(self.weatherFrame,fg_color='transparent',font=sfont,text_color=(c['light_mfont'],c['dark_mfont']),text='Enter a city to get\nits current weather.')

        self.timeFrame = ctk.CTkFrame(self,fg_color='transparent')
        self.dayLabel = ctk.CTkLabel(self.timeFrame,text='',font=sfont,text_color=(c['light_sfont'],c['dark_sfont']))
        self.timeLabel = ctk.CTkLabel(self.timeFrame,text='',font=sfont,text_color=(c['light_sfont'],c['dark_sfont']))
        self.locationLabel = ctk.CTkLabel(self.timeFrame,font=sfont,text_color=(c['light_sfont'],c['dark_sfont']),text='—')

        # place widgets
        self.locationFrame.pack(fill='x',side='top',pady=12)
        self.locationEntry.pack(expand=True,fill='x',side='left',anchor='w',padx=(25,0),pady=25)
        self.runButton.pack(side='right',anchor='e',padx=(0,25),pady=25)

        self.weatherFrame.pack(expand=True,fill='both')
        self.weatherIconLabel.pack(expand=True,padx=25)
        self.temperatureLabel.pack(padx=25)
        self.weatherTypeLabel.pack(padx=25,pady=(0,25))

        self.timeFrame.pack(side='bottom',anchor='e',padx=25,pady=25)
        self.dayLabel.pack(expand=True,anchor='e')
        self.timeLabel.pack(expand=True,anchor='e')
        self.locationLabel.pack(expand=True,anchor='e')


class MainFrame(ctk.CTkFrame):
    def __init__(self,parent,fg_color):
        super().__init__(parent,fg_color=fg_color)

        # populate frame
        self.populate(parent.c,parent.icons,parent.bfont,parent.mfont,parent.sfont,parent.efont)

        # place frame
        self.place(relx=0.35,rely=0.01,relwidth=0.64,relheight=0.98)
    

    def populate(self,c,icons,bfont,mfont,sfont,efont):
        # create info widgets
        self.infoFrame = ctk.CTkFrame(self,fg_color='transparent')

        self.sunFrame = ctk.CTkFrame(self.infoFrame,fg_color=(c['light_frame'],c['dark_frame']))
        self.sunIconLabel = ctk.CTkLabel(self.sunFrame,image=icons['sun_d'],text='')
        self.sunLabel = ctk.CTkLabel(self.sunFrame,font=sfont,text_color=(c['light_mfont'],c['dark_mfont']),text='Rise ——\nSet ——')

        self.windFrame = ctk.CTkFrame(self.infoFrame,fg_color=(c['light_frame'],c['dark_frame']))
        self.windIconLabel = ctk.CTkLabel(self.windFrame,image=icons['wind_d'],text='')
        self.windLabel = ctk.CTkLabel(self.windFrame,font=sfont,text_color=(c['light_mfont'],c['dark_mfont']),text='Wind\n——')

        self.rainFrame = ctk.CTkFrame(self.infoFrame,fg_color=(c['light_frame'],c['dark_frame']))
        self.rainIconLabel = ctk.CTkLabel(self.rainFrame,image=icons['rain_d'],text='')
        self.rainLabel = ctk.CTkLabel(self.rainFrame,font=sfont,text_color=(c['light_mfont'],c['dark_mfont']),text='Chance of Rain\n——')

        self.cloudFrame = ctk.CTkFrame(self.infoFrame,fg_color=(c['light_frame'],c['dark_frame']))
        self.cloudIconLabel = ctk.CTkLabel(self.cloudFrame,image=icons['cloud_d'],text='')
        self.cloudLabel = ctk.CTkLabel(self.cloudFrame,font=sfont,text_color=(c['light_mfont'],c['dark_mfont']),text='Cloud Cover \n——')

        # place info widgets
        self.infoFrame.pack(fill='both',pady=(0,12))

        self.sunFrame.pack(expand=True,fill='both',side='left',padx=(0,12))
        self.sunIconLabel.pack(padx=25,pady=25)
        self.sunLabel.pack(padx=25,pady=(0,25))

        self.windFrame.pack(expand=True,fill='both',side='left',padx=(0,12))
        self.windIconLabel.pack(padx=25,pady=25)
        self.windLabel.pack(padx=25,pady=(0,25))

        self.rainFrame.pack(expand=True,fill='both',side='left',padx=(0,12))
        self.rainIconLabel.pack(padx=25,pady=25)
        self.rainLabel.pack(padx=25,pady=(0,25))

        self.cloudFrame.pack(expand=True,fill='both',side='left',padx=0)
        self.cloudIconLabel.pack(padx=25,pady=25)
        self.cloudLabel.pack(padx=25,pady=(0,25))

        # create forecast widgets
        self.forecastsFrame = ctk.CTkFrame(self,fg_color=(c['light_box'],c['dark_box']))
        self.colorModeButton = ctk.CTkButton(self.forecastsFrame,font=efont,text='Force Dark Mode')

        # place forecast widgets
        self.forecastsFrame.pack(expand=True,fill='both')
        self.colorModeButton.pack(side='top',anchor='w',padx=12,pady=12)

        # prepare data
        data = {
            '0:00': 0,
            '3:00': 0,
            '6:00': 0,
            '9:00': 0,
            '12:00': 0,
            '15:00': 0,
            '18:00': 0,
            '21:00': 0
        }
        self.times = data.keys()
        self.temperatures = data.values()

        # create a figure
        figure = Figure(figsize=(6, 4), dpi=100, layout='tight')
        figure_canvas = FigureCanvasTkAgg(figure, self.forecastsFrame) # create FigureCanvasTkAgg object
        axes = figure.add_subplot() # create axes
        axes.plot(self.times, self.temperatures) # create line chart
        figure.set_facecolor(c['light_box'])
        axes.set_facecolor(c['light_frame'])
        
        axes.set_ylabel('Temperature (°C)',fontdict={'fontsize':12,'color':c['white']})
        axes.tick_params(axis='x',colors=c['white'])
        axes.tick_params(axis='y',colors=c['white'])
        for spine in axes.spines.values():
            spine.set_edgecolor(c['light_frame'])

        figure_canvas.get_tk_widget().pack(expand=True,fill='both',padx=12,pady=(0,12))
        

class App(ctk.CTk):
    def __init__(self):
        # colors
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

        # initialization
        super().__init__(fg_color=(self.c['light_bg'],self.c['dark_bg']))
        self.title('PyWeather™')
        self.minsize(512,300)
        self.iconbitmap('./assets/icons/dayicon.ico')
        self.bind_all("<Button-1>", lambda event: event.widget.focus_set()) # lets you defocus from entry widget

        # fonts
        self.bfont = ctk.CTkFont('Plus Jakarta Sans', 60, 'bold')
        self.mfont = ctk.CTkFont('DM Sans',25)
        self.sfont = ctk.CTkFont('Space Mono',16)
        self.efont = ctk.CTkFont('Space Mono', 12)

        # light/dark modes
        self.colormodes = 'light', 'dark'
        self.colormode = self.colormodes[0]
        ctk.set_appearance_mode(self.colormode)

        self.titlecolors = 0x00D2B391, 0x003D1C0F
        self.titlecolor = self.titlecolors[0]
        self.HWND = windll.user32.GetParent(self.winfo_id())
        windll.dwmapi.DwmSetWindowAttribute(self.HWND,35,byref(c_int(self.titlecolor)),sizeof(c_int))


        def toggleMode():
            if self.colormode==self.colormodes[0]:
                self.colormode = self.colormodes[1]
                self.titlecolor = self.titlecolors[1]
                self.iconbitmap('./assets/icons/nighticon.ico')
                self.main_frame.colorModeButton.configure(text='Force Light Mode')
                self.main_frame.sunIconLabel.configure(image=self.icons['sun_n'])
                self.main_frame.windIconLabel.configure(image=self.icons['wind_n'])
                self.main_frame.rainIconLabel.configure(image=self.icons['rain_n'])
                self.main_frame.cloudIconLabel.configure(image=self.icons['cloud_n'])
            else:
                self.colormode = self.colormodes[0]
                self.titlecolor = self.titlecolors[0]
                self.iconbitmap('./assets/icons/dayicon.ico')
                self.main_frame.colorModeButton.configure(text='Force Dark Mode')
                self.main_frame.sunIconLabel.configure(image=self.icons['sun_d'])
                self.main_frame.windIconLabel.configure(image=self.icons['wind_d'])
                self.main_frame.rainIconLabel.configure(image=self.icons['rain_d'])
                self.main_frame.cloudIconLabel.configure(image=self.icons['cloud_d'])

            windll.dwmapi.DwmSetWindowAttribute(self.HWND,35,byref(c_int(self.titlecolor)),sizeof(c_int))
            ctk.set_appearance_mode(self.colormode)


        # icons
        scale1 = 0.1875
        scale2 = 0.125

        self.icons = {}
        for code in ["01","02","03","04","09","10","11","13","50"]:
            for dn in ('d','n'):
                self.icons[f'{code}{dn}'] = ctk.CTkImage(Image.open(f"assets/icons/{code}{dn}.png"),size=(1660*scale1,1660*scale1))

        self.icons['blank'] = ctk.CTkImage(Image.open(f"assets/icons/blank.png"),size=(1660*scale1,1660*scale1))
        self.icons['null'] = ctk.CTkImage(Image.open(f"assets/icons/null.png"),size=(1660*scale1,1660*scale1))
        self.icons['sun_d'] = ctk.CTkImage(Image.open(f"assets/icons/sun_d.png"),size=(512*scale2,320*scale2))
        self.icons['sun_n'] = ctk.CTkImage(Image.open(f"assets/icons/sun_n.png"),size=(512*scale2,320*scale2))
        self.icons['wind_d'] = ctk.CTkImage(Image.open(f"assets/icons/wind_d.png"),size=(320*scale2,320*scale2))
        self.icons['wind_n'] = ctk.CTkImage(Image.open(f"assets/icons/wind_n.png"),size=(320*scale2,320*scale2))
        self.icons['rain_d'] = ctk.CTkImage(Image.open(f"assets/icons/rain_d.png"),size=(360*scale2,320*scale2))
        self.icons['rain_n'] = ctk.CTkImage(Image.open(f"assets/icons/rain_n.png"),size=(360*scale2,320*scale2))
        self.icons['cloud_d'] = ctk.CTkImage(Image.open(f"assets/icons/cloud_d.png"),size=(400*scale2,320*scale2))
        self.icons['cloud_n'] = ctk.CTkImage(Image.open(f"assets/icons/cloud_n.png"),size=(400*scale2,320*scale2))
        self.icons['run'] = ctk.CTkImage(Image.open(f"assets/icons/run.png"),size=(15,15))

        # create frames
        self.side_frame = SideFrame(self,(self.c['light_frame'],self.c['dark_frame']))
        self.main_frame = MainFrame(self,'transparent')

        # update window
        self.weather = getWeather(self.side_frame.locationEntry.get())


        def update(event):
            self.location = self.side_frame.locationEntry.get()
            self.weather = getWeather(self.location)
            self.forecast = getForecast(self.location)

            if self.weather['cod']==200:

                self.side_frame.weatherIconLabel.configure(text='',image=self.icons[self.weather['weather'][0]['icon']])
                self.side_frame.weatherTypeLabel.configure(font=self.mfont,text=f'''{self.weather['weather'][0]['description'].title()} ({int(self.weather['main']['temp_max']-273.15)}° / {int(self.weather['main']['temp_min']-273.15)}°)''')
                self.side_frame.temperatureLabel.configure(text=f"{int(self.weather['main']['temp']-273.15)}°")
                self.side_frame.locationLabel.configure(text=f"{self.weather['name']},{self.weather['sys']['country']}")
                self.main_frame.sunLabel.configure(text=f'''
Rise {datetime.utcfromtimestamp(self.weather['sys']['sunrise']+self.weather['timezone']).strftime('%H:%M')}
Set {datetime.utcfromtimestamp(self.weather['sys']['sunset']+self.weather['timezone']).strftime('%H:%M')}''')

                self.wind_dir = self.weather['wind']['deg']
                if 337.5 < self.wind_dir or self.wind_dir <= 22.5:
                    self.wind_dir = 'North'
                elif 22.5 < self.wind_dir <= 67.5:
                    self.wind_dir = 'North-East'
                elif 67.5 < self.wind_dir <= 112.5:
                    self.wind_dir = 'East'
                elif 112.5 < self.wind_dir <= 157.5:
                    self.wind_dir = 'South-East'
                elif 157.5 < self.wind_dir <= 202.5:
                    self.wind_dir = 'South'
                elif 202.5 < self.wind_dir <= 247.5:
                    self.wind_dir = 'South-West'
                elif 247.5 < self.wind_dir <= 292.5:
                    self.wind_dir = 'West'
                elif 292.5 < self.wind_dir <= 337.5:
                    self.wind_dir = 'North-West'
                else:
                    self.wind_dir = '—'
                
                self.main_frame.windLabel.configure(text=f"\n{self.weather['wind']['speed']*3.6:.2f}km/h Wind\n{self.wind_dir}")
                self.main_frame.rainLabel.configure(text=f"\nChance of Rain\n{self.forecast['list'][0]['pop']*100:.2f}%")
                self.main_frame.cloudLabel.configure(text=f"\nCloud Cover\n{self.weather['clouds']['all']}%")

                if self.weather['weather'][0]['icon'][2]=='d':
                    if self.colormode==self.colormodes[1]:
                        toggleMode()
                else:
                    if self.colormode==self.colormodes[0]:
                        toggleMode()

            else:

                self.side_frame.weatherIconLabel.configure(image=self.icons['null'])
                self.side_frame.weatherTypeLabel.configure(font=self.mfont,text=self.weather['message'].title())
                self.side_frame.temperatureLabel.configure(text='—')
                self.side_frame.locationLabel.configure(text='—')
                self.main_frame.sunLabel.configure(text='Rise ——\nSet ——')
                self.main_frame.windLabel.configure(text='Wind\n——')
                self.main_frame.rainLabel.configure(text='Chance of Rain\n——')
                self.main_frame.cloudLabel.configure(text='Cloud Cover \n——')


        def updateTime():
            if self.weather['cod']==200:
                self.time = datetime.fromtimestamp(datetime.utcnow().timestamp()+self.weather['timezone'])
                self.side_frame.dayLabel.configure(text=self.time.strftime('%A'))
                self.side_frame.timeLabel.configure(text=self.time.strftime('%H:%M:%S'))
            else:
                self.side_frame.dayLabel.configure(text='')
                self.side_frame.timeLabel.configure(text='')

            self.side_frame.after(1000, updateTime)


        self.main_frame.colorModeButton.configure(command=toggleMode)
        self.side_frame.runButton.configure(command=lambda: update(1))
        self.side_frame.locationEntry.bind("<Return>",update,add='+')

        updateTime()

        # run
        self.mainloop()


app = App()
