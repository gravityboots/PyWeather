import tkinter as tk
from tkinter import ttk


class App(tk.Tk): # App class inherits from Tk
    def __init__(self, title, size):
        super().__init__()
        self.title(title)
        self.minsize(size[0],size[1])

        self.mainloop()


class Weather(tk.Frame):
    pass


class Forecast(tk.Frame):
    pass


App('Yo',(500,300))