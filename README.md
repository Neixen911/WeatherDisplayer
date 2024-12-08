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
Installation de dash et de pandas nécessaire à l'affichage des informations et graphiques:
```bash
pip install dash
pip install pandas
```

### Récupération de données
- Excellente prise en charge de la récupération de données depuis des bases de données (via pandas, SQLAlchemy, psycopg2, etc.).
- Intégré avec des outils pour des API (REST/GraphQL) et le scraping web (requests, BeautifulSoup, Selenium).

### Affichage des données
- Bibliothèques de visualisation puissantes : Matplotlib, Seaborn, Plotly, et Dash (pour des tableaux de bord interactifs).