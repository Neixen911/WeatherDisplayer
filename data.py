from flask import Flask, render_template
import os
import requests
import json
import time

# Création de l'application Flask
app = Flask(__name__)

# Récupération des credentials
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
credentials_file = os.path.join(BASE_DIR, "credentials.json")
with open(credentials_file, "r") as file:
    credentials = json.load(file)

# URL de l'API
current_weather = f"https://api.open-meteo.com/v1/forecast?latitude={credentials['LAT']}&longitude={credentials['LON']}&daily=sunset,sunrise&current=temperature_2m,weather_code,rain,snowfall,precipitation,is_day&timezone=Europe%2FLondon&timeformat=unixtime"
hourly_forecast = f"https://api.open-meteo.com/v1/forecast?latitude={credentials['LAT']}&longitude={credentials['LON']}&hourly=temperature_2m,weather_code&timezone=Europe%2FLondon&timeformat=unixtime"
daily_forecast = f"https://api.open-meteo.com/v1/forecast?latitude={credentials['LAT']}&longitude={credentials['LON']}&daily=weather_code,temperature_2m_min,temperature_2m_max&timezone=Europe%2FLondon&timeformat=unixtime"

def get_weather():
    weather_informations = {
        'current-weather': {},
        'hourly-forecast': [],
        'daily-forecast': [],
    }
    while True:
        try:
            # Variable to use multiple times
            day_or_night = ""
            # Current weather
            response = requests.get(current_weather)
            if response.status_code == 200:
                data = response.json()
                # weather_informations['city'] = data['name']
                weather_informations['time'] = data['utc_offset_seconds']
                icon = get_desc_icon_from(data['current']['weather_code'])['icon']
                day_or_night = get_day_or_night(data['current']['is_day'])
                weather_informations['current-weather']['icon'] = "https://openweathermap.org/img/wn/" + icon + day_or_night + "@2x.png"
                weather_informations['current-weather']['temp'] = data['current']['temperature_2m']
                weather_informations['current-weather']['description'] = get_desc_icon_from(data['current']['weather_code'])['description'].capitalize()
                weather_informations['current-weather']['sunrise'] = time.strftime('%Hh%M', time.gmtime(data['daily']['sunrise'][0] + weather_informations['time']))
                weather_informations['current-weather']['sunset'] = time.strftime('%Hh%M', time.gmtime(data['daily']['sunset'][0] + weather_informations['time']))
                weather_informations['current-weather']['rain'] = data['current']['rain']
                weather_informations['current-weather']['snow'] = data['current']['snowfall']
            else:
                return f"Erreur {response.status_code} : {response.text}"
        
            # Hourly forecast for the next hours
            response = requests.get(hourly_forecast)
            if response.status_code == 200:
                data = response.json()
                # Itère sur les 7 prochaines heures
                for i in range(2, 9):
                    hour_forecast = {
                        'hour': time.strftime('%Hh', time.gmtime(data['hourly']['time'][i])),
                        'icon': "https://openweathermap.org/img/wn/" + get_desc_icon_from(data['hourly']['weather_code'][i])['icon'] + day_or_night + "@2x.png",
                        'temp': round(data['hourly']['temperature_2m'][i]),
                    }
                    weather_informations['hourly-forecast'].append(hour_forecast)
            else:
                return f"Erreur {response.status_code} : {response.text}"

            # Daily forecast on 7 days
            response = requests.get(daily_forecast)
            if response.status_code == 200:
                data = response.json()
                # Itère sur les 5 prochains jours
                for i in range(2, len(data['daily']['time'])):
                    day_forecast = {
                        'day': time.strftime('%A', time.gmtime(data['daily']['time'][i])),
                        'icon': "https://openweathermap.org/img/wn/" + get_desc_icon_from(data['daily']['weather_code'][i])['icon'] + "d" + "@2x.png",
                        'description': get_desc_icon_from(data['daily']['weather_code'][i])['description'].capitalize(),
                        'temp_min': round(data['daily']['temperature_2m_min'][i]),
                        'temp_max': round(data['daily']['temperature_2m_max'][i])
                    }
                    weather_informations['daily-forecast'].append(day_forecast)
            else:
                return f"Erreur {response.status_code} : {response.text}" 
        except requests.exceptions.RequestException as e:
            print(f"Erreur : {e}")

        return weather_informations

def get_desc_icon_from(value):
    # WMO weather codes, Description, Icon
    weather_values = {
        0: ("Clear sky", "01"),
        1: ("Mainly clear", "02"),
        2: ("Partly cloudy", "03"),
        3: ("Overcast", "04"),
        45: ("Fog", "50"),
        48: ("Depositing rime fog", "50"),
        51: ("Light drizzle", "09"),
        53: ("Moderate drizzle", "09"),
        55: ("Dense drizzle", "09"),
        56: ("Light freezing drizzle", "13"),
        57: ("Dense freezing drizzle", "13"),
        61: ("Slight rain", "10"),
        63: ("Moderate rain", "10"),
        65: ("Heavy rain", "10"),
        66: ("Light freezing rain", "13"),
        67: ("Heavy freezing rain", "13"),
        71: ("Slight snow fall", "13"),
        73: ("Moderate snow fall", "13"),
        75: ("Heavy snow fall", "13"),
        77: ("Snow grains", "13"),
        80: ("Slight rain showers", "09"),
        81: ("Moderate rain showers", "09"),
        82: ("Violent rain showers", "09"),
        85: ("Slight snow showers", "13"),
        86: ("Heavy snow showers", "13")
    }
    for wmo in weather_values:
        if wmo == value:
            return { 'description': weather_values[value][0], 'icon': weather_values[value][1] }
    return { 'description': "Unknown description", 'icon': "Unknown icon" }

def get_day_or_night(value):
    if value == 1:
        return "d"
    elif value == 0:
        return "n"
    return "Unknown day or night value"

@app.route('/')
def weather():
    return render_template('app.html', weather=get_weather())

@app.route('/update-data')
def update_data():
    return get_weather()

if __name__ == "__main__":
    app.run(debug=True)
