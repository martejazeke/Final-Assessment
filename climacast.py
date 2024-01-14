from tkinter import *
from tkinter import ttk, messagebox
import customtkinter, tkinter
from PIL import Image, ImageTk
import requests
from configparser import ConfigParser
import pytz
from datetime import datetime, timedelta

#Import the widgets used from customtkinter
from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkImage, CTkSwitch

class WeatherApp(Tk):
    def __init__(self):
        
        super().__init__()
        
        #configuration of colors for different elements
        self.light_bg_color = "#E5E4E2"
        self.light_box_color = "#D3D2D1"
        self.dark_bg_color = "#100C08"
        self.dark_box_color = "#2D2D2D"
        
        self.title("ClimaCast")
        self.geometry("650x670")
        self.config(bg=self.light_bg_color)
        self.resizable(False, False)
        
        #set the icon of the window
        logo_icon = PhotoImage(file='images/logo.png')
        self.iconphoto(False,logo_icon)
        
        #Extracts the API Key from the config.ini file
        self.config_file = 'config.ini'
        self.config_parser = ConfigParser()
        self.config_parser.read(self.config_file)
        self.api_key = self.config_parser['api_key']['key'] #retrieves the key from the config.ini file
        
        self.create_widgets()
    
    def get_weather(self, city):
        
        url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(city, self.api_key)
        try:
            result = requests.get(url)

            if result.status_code == 200:
                json_data = result.json()
                #Extract relevant data from JSON
                city = json_data['name']
                country = json_data['sys']['country']

                # Temperature
                temp_kelvin = json_data['main']['temp']
                temp_celsius = temp_kelvin - 273.15 #converts from kelvin to farenheit

                # Current Weather
                icon = json_data['weather'][0]['icon']
                weather = json_data['weather'][0]['description']

                # Time
                timezone = json_data['timezone']

                utc_time = datetime.utcnow() #returns the current date and time
                local_time = utc_time + timedelta(seconds=timezone)

                # Conditions
                wind_speed = json_data['wind']['speed']
                clouds = json_data['clouds']['all']
                visibility = json_data['visibility']
                humidity = json_data['main']['humidity']
                pressure = json_data['main']['pressure']
                feels_like_kelv = json_data['main']['feels_like']
                feels_like_celsius = feels_like_kelv - 273.15

                # Sunrise and Sunset
                sunrise = json_data['sys']['sunrise']
                sunset = json_data['sys']['sunset']

                final = (city, country, temp_celsius,icon,weather,timezone,local_time,wind_speed,visibility,humidity,pressure,feels_like_celsius,sunrise,sunset)
                return final
            else:
                
                #Shows an error when there is no weather data available.
                messagebox.showerror("Error", f"Failed to fetch weather data. Status code: {result.status_code}")
                return None
            
        except requests.exceptions.RequestException as e:
            #shows when there is an error
            messagebox.showerror("Error", "Failed to fetch weather data. Check your internet connection.")
            return None

    def get_forecast(self, city):
        url = ("https://api.openweathermap.org/data/2.5/forecast?q={}&appid={}".format(city, self.api_key))
        
        try:
            result = requests.get(url)
        
            if result.status_code == 200:
                json_data = result.json()
            
                first_day_img = json_data['list'][0]['weather'][0]['icon']

                first_min_temp_data = json_data['list'][0]['main']['temp_min']
                first_min_temp = first_min_temp_data - 273.15

                first_max_temp_data = json_data['list'][0]['main']['temp_max']
                first_max_temp = first_max_temp_data - 273.15


                second_day_img = json_data['list'][1]['weather'][0]['icon']

                second_min_temp_data = json_data['list'][1]['main']['temp_min']
                second_min_temp = second_min_temp_data - 273.15

                second_max_temp_data = json_data['list'][1]['main']['temp_max']
                second_max_temp = second_max_temp_data - 273.15

                third_day_img = json_data['list'][2]['weather'][0]['icon']

                third_min_temp_data = json_data['list'][2]['main']['temp_min']
                third_min_temp = third_min_temp_data - 273.15

                third_max_temp_data = json_data['list'][2]['main']['temp_max']
                third_max_temp = third_max_temp_data - 273.15

                forecast_data = (first_day_img, second_day_img, third_day_img, first_min_temp, first_max_temp, second_min_temp, second_max_temp,third_min_temp,third_max_temp)
            
                return forecast_data
            else:
                messagebox.showerror("Error",  f"Error in fetching forecast data. Status code: {result.status_code}")
                return None
        
        except requests.exceptions.RequestException as e:
            #Display an error message to the user if there was an error
            messagebox.showerror("Error", "Failed to fetch forecast data. Check your internet connection.")
            return None
            
    def search_weather(self):
        city = self.city_text.get()
        
        if not city:
            messagebox.showerror("Error", "Please type in a city before searching.")
            return
        
        weather = self.get_weather(city)
        forecast_data = self.get_forecast(city)
        
        if weather and forecast_data:
            print("Weather Data:", weather)  # Added this line for debugging

            city_info = '{}, {}'.format(weather[0], weather[1])
            self.city_lbl.configure(text=city_info)

            #icons
            icon_path = 'icons/{}@2x.png'.format(weather[3])
            try:
                icon_img = Image.open(icon_path)
            except IOError:
                icon_img = Image.open('icons/01d.png')
            
            icon_img = icon_img.resize((80,80), Image.LANCZOS)
            icon_img = ImageTk.PhotoImage(icon_img)
            self.icon_img = icon_img
            self.icon_lbl.configure(image=icon_img)
            
            first_day_icon = ImageTk.PhotoImage(file=f"icons/{forecast_data[0]}@2x.png")
            self.first_icon.configure(image=first_day_icon)
            
            second_day_icon = ImageTk.PhotoImage(file=f"icons/{forecast_data[1]}@2x.png")
            self.second_icon.configure(image=second_day_icon)
            
            third_day_icon = ImageTk.PhotoImage(file=f"icons/{forecast_data[2]}@2x.png")
            self.third_icon.configure(image=third_day_icon)

            #Time and Timezone
            time_info = '{}'.format(weather[6].strftime('%H:%M:%S'))
            self.time_lbl.configure(text=time_info)

            timezone_info = 'UTC {:+.0f}'.format(weather[5] / 3600)  # converts timezone
            self.timezone_lbl.configure(text=timezone_info)

            #Weather Conditions
            temp_info = '{:.2f} °C'.format(weather[2])
            self.temp_lbl.configure(text=temp_info)

            first_min_temp_info = 'Minimum Temp.: {:.2f} °C'.format(forecast_data[3])
            self.first_min_temp_lbl.configure(text=first_min_temp_info)
            
            first_max_temp_info = 'Maximum Temp.: {:.2f} °C'.format(forecast_data[4])
            self.first_max_temp_lbl.configure(text=first_max_temp_info)
            
            second_min_temp_info = 'Minimum Temp.: {:.2f} °C'.format(forecast_data[5])
            self.second_min_temp_lbl.configure(text=second_min_temp_info)
            
            second_max_temp_info = 'Maximum Temp.: {:.2f} °C'.format(forecast_data[6])
            self.second_max_temp_lbl.configure(text=second_max_temp_info)
            
            third_min_temp_info = 'Minimum Temp.: {:.2f} °C'.format(forecast_data[7])
            self.third_min_temp_lbl.configure(text=third_min_temp_info)
            
            third_max_temp_info = 'Maximum Temp.: {:.2f} °C'.format(forecast_data[8])
            self.third_max_temp_lbl.configure(text=third_max_temp_info)
            
            weat_desc_info = '{}'.format(weather[4])
            self.weat_desc_lbl.configure(text=weat_desc_info.capitalize())

            wind_spd_info = '{:.2f} km/h'.format(weather[7] * 3.6)  # converts from m/s to km/h
            self.wind_spd_val.configure(text=wind_spd_info)

            visibility_info = '{:.2f} km'.format(weather[8] / 1000)  # converts from m to km
            self.visibility_val.configure(text=visibility_info)

            humidity_info = '{:.2f} %'.format(weather[9])
            self.humidity_val.configure(text=humidity_info)

            pressure_info = '{} mb'.format(weather[10])
            self.pressure_val.configure(text=pressure_info)

            feels_like_info = '{:.2f} °C'.format(weather[11])
            self.feels_like_val.configure(text=feels_like_info)

            #Sunrise
            sunrise_utc = int(weather[12])
            sunrise_local = datetime.utcfromtimestamp(sunrise_utc + int(weather[5])).strftime('%H:%M:%S')
            sunrise_info = '{}'.format(sunrise_local)
            self.sunrise_time_lbl.configure(text=sunrise_info)

            #Sunset
            sunset_utc = int(weather[13])
            sunset_local = datetime.utcfromtimestamp(sunset_utc + int(weather[5])).strftime('%H:%M:%S')
            sunset_info = '{}'.format(sunset_local)
            self.sunset_time_lbl.configure(text=sunset_info)
            
            #days 
            
            current_day = datetime.now()
            self.current_day_lbl.configure(text=current_day.strftime('%m-%d-%Y (%A)'))
            
            first = current_day + timedelta(days=1)
            self.first_day_lbl.configure(text=first.strftime('%d  %A')) #displays the date and the day
            
            second = current_day + timedelta(days=2)
            self.second_day_lbl.configure(text=second.strftime('%d  %A'))
            
            third = current_day + timedelta(days=3)
            self.third_day_lbl.configure(text=third.strftime('%d  %A'))

        else:
            print("No weather data found.")  # Added this line for debugging

    
    def create_widgets(self):
        self.create_search_frame()
        self.create_main_frame()
        self.create_sunrise_frame()
        self.create_sunset_frame()
        self.create_firstday_frame()
        self.create_secondday_frame()
        self.create_thirdday_frame()
        self.switch()

    def switch_event(self):
        
        #Sets to dark mode
        if self.switch_var_1.get() == 'off':
            self.config(bg =self.dark_bg_color)
            
            self.switch_toggle.configure(text="Toggle Light Mode", text_color = "white")
            #changing the main frame colors
            self.main_frm.configure(bg_color = self.dark_box_color, fg_color = self.dark_box_color)
            self.city_entry.configure(bg_color = self.dark_bg_color, text_color = "white")
            self.city_lbl.configure(bg_color = self.dark_box_color, fg_color=self.dark_box_color, text_color = "white")
            self.icon_lbl.configure(bg_color = self.dark_box_color)
            self.current_day_lbl.configure(bg_color = self.dark_box_color, fg_color=self.dark_box_color, text_color = "white")
            self.time_lbl.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color,text_color="white")
            self.timezone_lbl.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color,text_color="white")
            self.temp_lbl.configure(bg_color = self.dark_box_color, fg_color=self.dark_box_color, text_color="white")
            self.weat_desc_lbl.configure(bg_color = self.dark_box_color, fg_color=self.dark_box_color, text_color="white")
            self.wind_spd_lbl.configure(bg_color = self.dark_box_color, fg_color=self.dark_box_color, text_color="white")
            self.wind_spd_val.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color, text_color="white")
            self.visibility_lbl.configure(bg_color = self.dark_box_color, fg_color=self.dark_box_color, text_color="white")
            self.visibility_val.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color, text_color="white")
            self.humidity_lbl.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color, text_color="white")
            self.humidity_val.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color, text_color="white")
            self.pressure_lbl.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color, text_color="white")
            self.pressure_val.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color, text_color="white")
            self.feels_like_lbl.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color, text_color="white")
            self.feels_like_val.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color, text_color="white")
            
            #sunrise frame
            self.sunrise_frm.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color)
            self.sunrise_lbl.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color, text_color="white")
            self.sunrise_icon.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color, text_color="white")
            self.sunrise_time_lbl.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color, text_color="white")
            
            #sunset
            self.sunset_frm.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color)
            self.sunset_lbl.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color, text_color="white")
            self.sunset_icon.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color, text_color="white")
            self.sunset_time_lbl.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color, text_color="white")
            
            #first_day frm
            self.first_frm.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color)
            self.first_day_lbl.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color, text_color="white")
            self.first_icon.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color)
            self.first_min_temp_lbl.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color, text_color="white")
            self.first_max_temp_lbl.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color, text_color="white")
            
            #second_day frm
            self.second_frm.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color)
            self.second_day_lbl.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color, text_color="white")
            self.second_icon.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color)
            self.second_min_temp_lbl.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color, text_color="white")
            self.second_max_temp_lbl.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color, text_color="white")
            
            #third_day frm
            self.third_frm.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color)
            self.third_day_lbl.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color, text_color="white")
            self.third_icon.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color)
            self.third_min_temp_lbl.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color, text_color="white")
            self.third_max_temp_lbl.configure(bg_color = self.dark_box_color,  fg_color=self.dark_box_color, text_color="white")
        else:
            self.config(bg = self.light_bg_color)
            
            #main frame
            self.switch_toggle.configure(text="Toggle Dark Mode", text_color = "black")
            self.main_frm.configure(bg_color = self.light_box_color, fg_color = self.light_box_color)
            self.city_entry.configure(bg_color = self.light_bg_color,fg_color = self.light_box_color, text_color = "black")
            self.icon_lbl.configure(bg_color = self.light_box_color)
            self.city_lbl.configure(bg_color = self.light_box_color, fg_color=self.light_box_color, text_color = "black")
            self.current_day_lbl.configure(bg_color = self.light_box_color, fg_color=self.light_box_color, text_color = "black")
            self.time_lbl.configure(bg_color = self.light_box_color, fg_color=self.light_box_color, text_color = "black")
            self.timezone_lbl.configure(bg_color = self.light_box_color, fg_color=self.light_box_color, text_color = "black")
            self.temp_lbl.configure(bg_color = self.light_box_color, fg_color=self.light_box_color, text_color = "black")
            self.weat_desc_lbl.configure(bg_color = self.light_box_color, fg_color=self.light_box_color, text_color = "black")
            self.wind_spd_lbl.configure(bg_color = self.light_box_color, fg_color=self.light_box_color, text_color = "black")
            self.wind_spd_val.configure(bg_color = self.light_box_color, fg_color=self.light_box_color, text_color = "black")
            self.visibility_lbl.configure(bg_color = self.light_box_color, fg_color=self.light_box_color, text_color = "black")
            self.visibility_val.configure(bg_color = self.light_box_color, fg_color=self.light_box_color, text_color = "black")
            self.humidity_lbl.configure(bg_color = self.light_box_color, fg_color=self.light_box_color, text_color = "black")
            self.humidity_val.configure(bg_color = self.light_box_color, fg_color=self.light_box_color, text_color = "black")
            self.pressure_lbl.configure(bg_color = self.light_box_color, fg_color=self.light_box_color, text_color = "black")
            self.pressure_val.configure(bg_color = self.light_box_color, fg_color=self.light_box_color, text_color = "black")
            self.feels_like_lbl.configure(bg_color = self.light_box_color, fg_color=self.light_box_color, text_color = "black")
            self.feels_like_val.configure(bg_color = self.light_box_color, fg_color=self.light_box_color, text_color = "black")

            #sunrise frame
            self.sunrise_frm.configure(bg_color = self.light_box_color,  fg_color=self.light_box_color)
            self.sunrise_lbl.configure(bg_color = self.light_box_color,  fg_color=self.light_box_color, text_color="black")
            self.sunrise_icon.configure(bg_color = self.light_box_color, fg_color=self.light_box_color, text_color = "black")
            self.sunrise_time_lbl.configure(bg_color = self.light_box_color, fg_color=self.light_box_color, text_color = "black")
            
            #sunset frame
            self.sunset_frm.configure(bg_color = self.light_box_color,  fg_color=self.light_box_color)
            self.sunset_lbl.configure(bg_color = self.light_box_color,  fg_color=self.light_box_color, text_color="black")
            self.sunset_icon.configure(bg_color = self.light_box_color, fg_color=self.light_box_color, text_color = "black")
            self.sunset_time_lbl.configure(bg_color = self.light_box_color, fg_color=self.light_box_color, text_color = "black")
            
            #first_day frame
            self.first_frm.configure(bg_color = self.light_box_color,  fg_color=self.light_box_color)
            self.first_day_lbl.configure(bg_color = self.light_box_color,  fg_color=self.light_box_color, text_color="black")
            self.first_icon.configure(bg_color = self.light_box_color,  fg_color=self.light_box_color)
            self.first_min_temp_lbl.configure(bg_color = self.light_box_color,  fg_color=self.light_box_color, text_color="black")
            self.first_max_temp_lbl.configure(bg_color = self.light_box_color,  fg_color=self.light_box_color, text_color="black")
            
            #second_day frame
            self.second_frm.configure(bg_color = self.light_box_color,  fg_color=self.light_box_color)
            self.second_day_lbl.configure(bg_color = self.light_box_color,  fg_color=self.light_box_color, text_color="black")
            self.second_icon.configure(bg_color = self.light_box_color,  fg_color=self.light_box_color)
            self.second_min_temp_lbl.configure(bg_color = self.light_box_color,  fg_color=self.light_box_color, text_color="black")
            self.second_max_temp_lbl.configure(bg_color = self.light_box_color,  fg_color=self.light_box_color, text_color="black")
            
            #third day frame
            self.third_frm.configure(bg_color = self.light_box_color,  fg_color=self.light_box_color)
            self.third_day_lbl.configure(bg_color = self.light_box_color,  fg_color=self.light_box_color, text_color="black")
            self.third_icon.configure(bg_color = self.light_box_color,  fg_color=self.light_box_color)
            self.third_min_temp_lbl.configure(bg_color = self.light_box_color,  fg_color=self.light_box_color, text_color="black")
            self.third_max_temp_lbl.configure(bg_color = self.light_box_color,  fg_color=self.light_box_color, text_color="black")
    def switch(self):
        
        self.switch_var_1 = StringVar(value="on")
        
        self.switch_toggle = CTkSwitch( master = self, command = self.switch_event, variable = self.switch_var_1, onvalue = "off", offvalue = "on")
        
        self.switch_toggle.configure( text = "Toggle Dark Mode", text_color = "black", font = ("Helvetica", 12, "bold"))
        self.switch_toggle.place(x=425, y=20)
        
    def create_search_frame(self):
        #Search frame for entering the city
        self.search_frm = customtkinter.CTkFrame(master = self)

        self.search_frm.place(x=50, y=20)

        self.city_text = StringVar()

        #Entry widget for the city
        self.city_entry = customtkinter.CTkEntry( master = self.search_frm, width = 250, height = 25, border_width = 0, corner_radius = 20, textvariable = self.city_text, fg_color = self.light_box_color, bg_color = self.light_bg_color, text_color = "black", font = ("Helvetica", 14, "bold"))
        self.city_entry.pack()

        self.search_img = customtkinter.CTkImage( Image.open('images/search.png'), size = (15,15))

        self.search_img.configure(bg_color = self.light_bg_color)
        #Button to initiate to search the weather for the given city
        self.search_img_btn = customtkinter.CTkButton( master = self.search_frm, image = self.search_img, border_width = 0,  text="", fg_color = self.light_box_color, bg_color = self.light_box_color, height = 15, width = 15, hover_color = "#CECECE", command = self.search_weather)
        self.search_img_btn.place(x=210, y=1)
        
    def create_main_frame(self):
        #Main frame to display the weather data of the searched city
        self.main_frm = CTkFrame( master = self, width = 350, height = 300)
        self.main_frm.configure( bg_color = self.light_box_color, fg_color = self.light_box_color,)
        self.main_frm.place(x=50,y=70)
        
        #Label for displaying city information
        self.city_lbl = CTkLabel( master = self.main_frm, text_color = "black", text="", font = ("Helvetica", 16, "bold"))
        self.city_lbl.configure( bg_color = self.light_box_color, fg_color = self.light_box_color)
        self.city_lbl.place(x=10, y=10)
        
        self.current_day_lbl = CTkLabel( master = self.main_frm, text_color = "black", bg_color = self.light_box_color, fg_color = self.light_box_color, text="", font = ("Helvetica", 12))
        self.current_day_lbl.place(x=10, y=32)
        
        self.time_lbl = CTkLabel( master = self.main_frm, text_color = "black", bg_color = self.light_box_color, fg_color = self.light_box_color, text="", font = ("Helvetica", 12))
        self.time_lbl.place(x=175,y=32)

        self.timezone_lbl = CTkLabel(master = self.main_frm,text_color = "black",bg_color = self.light_box_color,fg_color = self.light_box_color,text="",font = ("Helvetica", 12))
        self.timezone_lbl.place(x=250, y=32)

        self.icon_lbl = CTkLabel(master = self.main_frm, image="",bg_color = self.light_box_color,text= "")
        self.icon_lbl.place(x=10, y= 60)

        self.temp_lbl = CTkLabel(master = self.main_frm,text_color = "black",bg_color = self.light_box_color,fg_color = self.light_box_color,text="",font = ("Helvetica", 20, "bold"))
        self.temp_lbl.place(x=110, y=80)

        self.weat_desc_lbl = CTkLabel( master = self.main_frm, text_color = "black", bg_color = self.light_box_color, fg_color = self.light_box_color, text="", font = ("Helvetica", 12)) 
        self.weat_desc_lbl.place(x=110, y=105)
        
        #CONDITIONS
        
        #
        self.wind_spd_lbl = CTkLabel( master = self.main_frm, text_color = "black", bg_color = self.light_box_color, fg_color = self.light_box_color, text="Wind Speed", font = ("Helvetica", 12, "bold"))
        self.wind_spd_lbl.place(x=20, y=150)

        self.wind_spd_val = CTkLabel(master = self.main_frm,text_color = "black",bg_color = self.light_box_color,fg_color = self.light_box_color,text="",font = ("Helvetica", 12))
        self.wind_spd_val.place(x=26, y=170)

        self.visibility_lbl = CTkLabel( master = self.main_frm, text_color = "black", bg_color = self.light_box_color, fg_color = self.light_box_color, text="Visibility", font = ("Helvetica", 12,"bold"))
        self.visibility_lbl.place(x=150, y=150)

        self.visibility_val = CTkLabel(master=self.main_frm,text_color = "black",bg_color = self.light_box_color,fg_color = self.light_box_color,text="",font = ("Helvetica", 12))
        self.visibility_val.place(x=147, y=170)

        self.humidity_lbl = CTkLabel(master=self.main_frm,text_color = "black",bg_color = self.light_box_color,fg_color = self.light_box_color,text="Humidity",font = ("Helvetica", 12, "bold"))
        self.humidity_lbl.place(x=280, y=150)

        self.humidity_val = CTkLabel(master=self.main_frm,text_color = "black",bg_color = self.light_box_color,fg_color = self.light_box_color,text="",font = ("Helvetica", 12))
        self.humidity_val.place(x=284, y=170)

        self.pressure_lbl = CTkLabel(master=self.main_frm,text_color = "black",bg_color = self.light_box_color,fg_color = self.light_box_color,text="Pressure",font = ("Helvetica", 12, "bold"))
        self.pressure_lbl.place(x=90, y=210)

        self.pressure_val = CTkLabel(master=self.main_frm,text_color = "black",bg_color = self.light_box_color,fg_color = self.light_box_color,text="",font = ("Helvetica", 12))
        self.pressure_val.place(x=90, y=230)

        self.feels_like_lbl = CTkLabel(master=self.main_frm,text_color = "black",bg_color = self.light_box_color,fg_color = self.light_box_color,text="Feels like",font = ("Helvetica", 12, "bold"))
        self.feels_like_lbl.place(x=210, y=210)

        self.feels_like_val = CTkLabel(master=self.main_frm,text_color = "black",bg_color = self.light_box_color,fg_color = self.light_box_color,text="",font = ("Helvetica", 12))
        self.feels_like_val.place(x=215, y=230)
        
    def create_sunrise_frame(self):
        
        self.sunrise_frm = CTkFrame(master = self,width = 170,height = 141)
        self.sunrise_frm.configure(bg_color = self.light_box_color,fg_color = self.light_box_color,)
        self.sunrise_frm.place(x=420, y=70)

        self.sunrise_lbl = CTkLabel(master = self.sunrise_frm,text = "Sunrise",font = ("Helvetica", 12, "bold"),text_color = "black",bg_color = self.light_box_color,fg_color = self.light_box_color)
        self.sunrise_lbl.place(x=63)

        self.sunrise_img = CTkImage(Image.open('images/sunrise.png'),size = (70,70))

        self.sunrise_icon = CTkLabel(master = self.sunrise_frm,image = self.sunrise_img,bg_color = self.light_box_color,text = "")
        
        self.sunrise_icon.place(x=50, y=25)

        self.sunrise_time_lbl = CTkLabel(master = self.sunrise_frm,text_color = "black",bg_color = self.light_box_color,fg_color = self.light_box_color,text="",font = ("Helvetica", 20, "bold"))
        self.sunrise_time_lbl.place(x=47, y=100)

    def create_sunset_frame(self):
        self.sunset_frm = CTkFrame(master = self,width = 170,height = 145,)
        self.sunset_frm.configure(bg_color = self.light_box_color,fg_color = self.light_box_color)
        self.sunset_frm.place(x=420, y=225)

        self.sunset_lbl = CTkLabel(master = self.sunset_frm,text = "Sunset",font = ("Helvetica", 12, "bold"),text_color = "black",bg_color = self.light_box_color,fg_color = self.light_box_color)
        self.sunset_lbl.place(x=63)

        self.sunset_img = CTkImage(Image.open('images/sunset.png'),size = (70,70))

        self.sunset_icon = CTkLabel(master = self.sunset_frm,image = self.sunset_img,text = "")
        self.sunset_icon.configure(bg_color = self.light_box_color)
        self.sunset_icon.place(x=50, y=25)

        self.sunset_time_lbl = CTkLabel(master = self.sunset_frm,text_color = "black",bg_color = self.light_box_color,fg_color = self.light_box_color,text="",font = ("Helvetica", 20, "bold"))
        self.sunset_time_lbl.place(x=47, y=100)
        
    def create_firstday_frame(self):
        self.first_frm = CTkFrame(master = self,width = 165,height = 270,)
        self.first_frm.configure(bg_color = self.light_box_color,fg_color = self.light_box_color)
        self.first_frm.place(x=50, y=380)
        
        self.first_day_lbl = CTkLabel(master = self.first_frm,font = ("Helvetica", 14, "bold"),text_color = "black",bg_color = self.light_box_color,fg_color = self.light_box_color,text="")
        self.first_day_lbl.place(x=27, y=10)
        
        self.first_icon = CTkLabel(master = self.first_frm,bg_color = self.light_box_color,text="",image = "")
        self.first_icon.place(x=27, y=35)
        
        self.first_min_temp_lbl = CTkLabel(master = self.first_frm,text_color = "black",bg_color = self.light_box_color,fg_color = self.light_box_color,text="",font = ("Helvetica", 10),)
        self.first_min_temp_lbl.place(x=20, y=120)
        
        self.first_max_temp_lbl = CTkLabel(master = self.first_frm,text_color = "black",bg_color = self.light_box_color,fg_color = self.light_box_color,text="",font = ("Helvetica", 10),)
        self.first_max_temp_lbl.place(x=20, y=150)
    
    def create_secondday_frame(self):
        self.second_frm = CTkFrame(master = self,width = 165,height = 270,)
        self.second_frm.configure(bg_color = self.light_box_color,fg_color = self.light_box_color)
        self.second_frm.place(x=235, y=380)
        
        self.second_day_lbl = CTkLabel(master = self.second_frm,font = ("Helvetica", 14, "bold"),text_color = "black",bg_color = self.light_box_color,fg_color = self.light_box_color,text="")
        self.second_day_lbl.place(x=35, y=10)
        
        self.second_icon = CTkLabel(master = self.second_frm,bg_color = self.light_box_color,text="",image = "")
        self.second_icon.place(x=27, y=35)
        
        self.second_min_temp_lbl = CTkLabel(master = self.second_frm,text_color = "black",bg_color = self.light_box_color,fg_color = self.light_box_color,text="",font = ("Helvetica", 10),)
        self.second_min_temp_lbl.place(x=20, y=120)
        
        self.second_max_temp_lbl = CTkLabel(master = self.second_frm,text_color = "black",bg_color = self.light_box_color,fg_color = self.light_box_color,text="",font = ("Helvetica", 10),)
        self.second_max_temp_lbl.place(x=20, y=150)
    
    def create_thirdday_frame(self):
        self.third_frm = CTkFrame(master = self,width = 170,height = 270,)
        self.third_frm.configure(bg_color = self.light_box_color,fg_color = self.light_box_color)
        self.third_frm.place(x=420, y=380)

        self.third_day_lbl = CTkLabel(master = self.third_frm,font = ("Helvetica", 14, "bold"),text_color = "black",bg_color = self.light_box_color,fg_color = self.light_box_color,text="")
        self.third_day_lbl.place(x=45, y=10)
        
        self.third_icon = CTkLabel(master = self.third_frm,bg_color = self.light_box_color,text="",image = "")
        self.third_icon.place(x=27, y=35)
        
        self.third_min_temp_lbl = CTkLabel(master = self.third_frm,text_color = "black",bg_color = self.light_box_color,fg_color = self.light_box_color,text="",font = ("Helvetica", 10))
        self.third_min_temp_lbl.place(x=20, y=120)
        
        self.third_max_temp_lbl = CTkLabel(master = self.third_frm,text_color = "black",bg_color = self.light_box_color,fg_color = self.light_box_color,text="",font = ("Helvetica", 10))
        self.third_max_temp_lbl.place(x=20, y=150)
        
########################################################################

#Calls the main program
if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()