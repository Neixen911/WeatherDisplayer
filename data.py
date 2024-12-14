from flask import Flask, Response, stream_with_context
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
three_hour_forecast= f"https://api.openweathermap.org/data/2.5/forecast?lat={credentials['LAT']}&lon={credentials['LON']}&appid={credentials['API_KEY']}&units={credentials['METRIC']}&lang={credentials['LANG']}"

def get_weather():
    while True:
        try:
            # Current weather
            response = requests.get(current_weather)
            if response.status_code == 200:
                data = response.json()
                yield f"Icone: {data['weather'][0]['icon']}\n"
                yield f"Temps: {data['weather'][0]['main']}\n"
                yield f"Description: {data['weather'][0]['description']}\n"
                yield f"Température: {data['main']['temp']}°C\n"
                yield f"Ressenti: {data['main']['feels_like']}°C\n"
                yield f"Min: {data['main']['temp_min']}°C\n"
                yield f"Max: {data['main']['temp_max']}°C\n"
                yield f"Vent: {data['wind']['speed']} m/s\n"
                yield f"Levé du soleil: {time.strftime('%H:%M', time.gmtime(data['sys']['sunrise']))}\n"
                yield f"Couché du soleil: {time.strftime('%H:%M', time.gmtime(data['sys']['sunset']))}\n"
                # yield f"{data}\n"
                yield f"\n"
            else:
                yield f"Erreur {response.status_code} : {response.text}"

            # 3-hour forecast for 5 days
            response = requests.get(three_hour_forecast)
            if response.status_code == 200:
                data = response.json()
                # Itère sur chaque élément de la liste data['list']
                for i in range(0, len(data['list'])):
                    yield f"Horaires de prévision: {data['list'][i]['dt_txt']}\n"
                    yield f"Icone: {data['list'][i]['weather'][0]['icon']}\n"
                    yield f"Temps: {data['list'][i]['weather'][0]['main']}\n"
                    yield f"Description: {data['list'][i]['weather'][0]['description']}\n"
                    yield f"Température: {data['list'][i]['main']['temp']}°C\n"
                # yield f"{data['list'][0]}\n"
                # yield f"{data}\n"
                yield f"\n"
            else:
                yield f"Erreur {response.status_code} : {response.text}"
        except requests.exceptions.RequestException as e:
            print(f"Erreur : {e}")

        time.sleep(90)  # Attente de 90 secondes

@app.route('/')
def weather():
    return Response(stream_with_context(get_weather()), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(debug=True)