# WeatherDisplayer
## Description
A weather station is a useful project for the constant updated information about weather wherever in the world.
Firstly, I like when something works well and have his autonomous system who doesn't need interaction or maintenance every time.
Secondly, it is just a beatiful project no ? Like all weather of the world in just in this program like I control everything.
I love this feeling of control everything in IT and more again in embedded system that's why this project run in my Raspberry Pi 4.
Now, this project use OpenWeather API for retrieve the data of my location and the other one but with time and money, 
I want to upgrade it with a temperature and rain sensors to make it more local and in my hand you know.

## Prerequisites
To make this project works, you need to create a file named `credentials.json` who stocks necessary informations to retrieve data.
You can find below the minimum informations you need to fill:
- The API key who is needed to call the API.
- The lattitude you want to know the weather.
- The longitude you want to know the weather.
```bash
{
    "API_KEY": "<YOUR_API_KEY>",
    "LAT": YOUR_LATTITUDE,
    "LON": YOUR_LONGITUDE
}
```
More settings are addable but there are optionals:
- The metric who is the unit of measurement for the temperature.
- The lang who is the language of return like US or whatever.
```bash
    "METRIC": "<YOUR_METRIC>",
    "LANG": "<YOUR_LANGUAGE>"
```

Now that is made, you need to create a venv (for 'Virtual Environment') to install dependacies in a dedicated Python environment to make sure
there are no version conflicts with your other project who use Python.
To do that's, you need to type the following command to create a venv:
```bash
python3 -m venv path/to/venv
```

When the venv is created, you now need to activate it with this command:
```bash
source .venv/bin/activate
```

## Installation
To install all the dependencies you need to run this project, I'm gonna make a dedicated file named `dependencies.txt` but now, 
this file is not created so you have to wait and do the manual installation below.

To make the interface of my weather station, I decided to use Flask to make it more customizable.
So, to install Flask, you need to do this command:
```bash
pip install flask
```
