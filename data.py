from flask import Flask, render_template
import requests
import json
import time

# Création de l'application Flask
app = Flask(__name__)

# Récupération des credentials
with open("credentials.json", "r") as file:
    credentials = json.load(file)

# URL de l'API
current_weather = f"https://api.openweathermap.org/data/2.5/weather?lat={credentials['LAT']}&lon={credentials['LON']}&appid={credentials['API_KEY']}&units={credentials['METRIC']}&lang={credentials['LANG']}"
three_hour_forecast= f"https://api.openweathermap.org/data/2.5/forecast/daily?lat={credentials['LAT']}&lon={credentials['LON']}&cnt={7}&appid={credentials['API_KEY']}&units={credentials['METRIC']}&lang={credentials['LANG']}"

def get_weather():
    weather_informations = {
        'current-weather': {}, 
        'daily-forecast': []
    }
    while True:
        try:
            # Current weather
            response = requests.get(current_weather)
            if response.status_code == 200:
                data = response.json()
                weather_informations['current-weather']['icon'] = data['weather'][0]['icon']
                weather_informations['current-weather']['main'] = data['weather'][0]['main']
                weather_informations['current-weather']['description'] = data['weather'][0]['description']
                weather_informations['current-weather']['temp'] = data['main']['temp']
                weather_informations['current-weather']['feels_like'] = data['main']['feels_like']
                weather_informations['current-weather']['temp_min'] = data['main']['temp_min']
                weather_informations['current-weather']['temp_max'] = data['main']['temp_max']
                weather_informations['current-weather']['wind'] = data['wind']['speed']
                weather_informations['current-weather']['sunrise'] = time.strftime('%H:%M', time.gmtime(data['sys']['sunrise']))
                weather_informations['current-weather']['sunset'] = time.strftime('%H:%M', time.gmtime(data['sys']['sunset']))
            else:
                return f"Erreur {response.status_code} : {response.text}"

            # Daily forecast on 7 days
            response = requests.get(three_hour_forecast)
            if response.status_code == 200:
                data = response.json()
                # Itère sur chaque élément de la liste data['list']
                for i in range(0, len(data['list'])):
                    day_forecast = {
                        'icon': data['list'][i]['weather'][0]['icon'],
                        'main': data['list'][i]['weather'][0]['main'],
                        'description': data['list'][i]['weather'][0]['description'],
                        'temp_min': data['list'][i]['temp']['min'],
                        'temp_max': data['list'][i]['temp']['max']
                    }
                    weather_informations['daily-forecast'].append(day_forecast)
            else:
                return f"Erreur {response.status_code} : {response.text}"
        except requests.exceptions.RequestException as e:
            print(f"Erreur : {e}")

        return weather_informations

@app.route('/')
def weather():
    return render_template('app.html', weather=get_weather())

@app.route('/update_data')
def update_data():
    return get_weather()

if __name__ == "__main__":
    app.run(debug=True)