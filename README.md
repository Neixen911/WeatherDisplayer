### Prérequis
Création d'un fichier credentials.json avec les informations minimum suivantes:
```bash
{
    "API_KEY": "<YOUR_API_KEY>",
    "LAT": YOUR_LATTITUDE,
    "LON": YOUR_LONGITUDE
}
```
Plus de paramètres sont ajoutables à cette liste.
Les paramètres optionnels sont les suivants:
```bash
    "METRIC": "<YOUR_METRIC>",
    "LANG": "<YOUR_LANGUAGE>"
```
Installation de Flask:
```bash
pip install flask
```

### Récupération de données
- Utilisation de requests pour le requetage vers l'API OpenWeather.

### Affichage des données
- Pour ce qui est de la partie affichage, j'ai tout simplement choisi Flask pour me permettre de designer comme je le souhaite 
le rendu des informations dans le navigateur. Flask m'oblige a tout faire moi même mais au moins, ça aura l'avantage d'être 
entièrement modifiable.