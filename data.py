import requests
import json

# Récupération des credentials
with open("credentials.json", "r") as file:
    credentials = json.load(file)

# URL de l'API
api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={credentials['LAT']}&lon={credentials['LON']}&appid={credentials['API_KEY']}&units={credentials['METRIC']}&lang={credentials['LANG']}"

try:
    # Envoi de la requête GET
    response = requests.get(api_url)

    # Vérification du statut de la réponse
    if response.status_code == 200:
        # Conversion de la réponse JSON en dictionnaire Python
        data = response.json()
        # Sauvegarde des données dans un fichier JSON
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print("Données sauvegardées dans le fichier data.json")
    else:
        print(f"Erreur {response.status_code} : {response.text}")

except requests.exceptions.RequestException as e:
    print("Une erreur est survenue :", e)
