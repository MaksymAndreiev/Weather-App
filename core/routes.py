import json

import requests
from flask import render_template, request
from flask import current_app as app
import datetime

from controllers.city import add_city as add, get_all_cities
from controllers.city import delete as del_
from controllers.parse_request import hourly_data, daily_data
from controllers.users import add_user
from models.MeasuringUnits import MeasuringUnits
from settings.constants import api_key
from settings.CountriesList import countries_codes


@app.template_filter('positive')
def positive(arr):
    return all(val >= 0 for val in arr)


@app.route('/add', methods=['GET', 'POST'])
def add_city():
    return add()


@app.route('/delete/<city_id>', methods=['GET', 'POST'])
def delete(city_id):
    return del_(city_id)


@app.route('/reg', methods=['GET', 'POST'])
def registration():
    return add_user()


@app.route('/')
def index():
    def get_date(timezone):
        tz = datetime.timezone(datetime.timedelta(seconds=int(timezone)))
        day = datetime.datetime.now(tz=tz).date().strftime("%a, %d %b")
        time = datetime.datetime.now(tz=tz).time().strftime("%H:%M")
        hour = datetime.datetime.now(tz=tz).time().hour
        return hour, time, day

    if len(MeasuringUnits.query.all()) == 0:
        MeasuringUnits.create(**{'unit_name': 'standard', 'unit_description': 'Kelvin'})
        MeasuringUnits.create(**{'unit_name': 'metric', 'unit_description': 'Celsius'})
        MeasuringUnits.create(**{'unit_name': 'imperial', 'unit_description': 'Fahrenheit'})
    weather = []
    cities = get_all_cities()
    for city in cities:

        # cur.execute(f"SELECT name FROM city WHERE id = {city[0]}")
        city_id = city[0]
        city_name = city[1]
        data = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric')

        lat = json.loads(data.content)["coord"].get("lat")
        lon = json.loads(data.content)["coord"].get("lon")

        data_forecast = requests.get(
            f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,'
            f'alerts&appid={api_key}&units=metric')

        # прогноз погоды по дням где ид города = сити.ид_города (поле дневная температура)
        days_weather = list(
            int(json.loads(data_forecast.content)["daily"][i].get("temp").get("day")) for i in range(1, 8))
        # прогноз погоды по дням где ид города = сити.ид_города (поле название дня недели)
        days_names = ['i' for i in range(7)]
        #
        for i in range(1, 8):
            days_names[i - 1] = get_date_name(json.loads(data_forecast.content)["daily"][i].get('dt'))

        # прогноз погоды по дням где ид города = сити.ид_города (поля)
        tooltip_info = [
            list(int(json.loads(data_forecast.content)["daily"][i].get("temp").get("day")) for i in range(1, 8)),
            list(int(json.loads(data_forecast.content)["daily"][i].get("temp").get("night")) for i in range(1, 8)),
            list(int(json.loads(data_forecast.content)["daily"][i].get("feels_like").get("day")) for i in range(1, 8)),
            list(int(json.loads(data_forecast.content)["daily"][i].get("feels_like").get("night")) for i in range(1, 8))
        ]

        #
        dict_with_weather_info = {
            "name": city.name,
            "state": {k: v for e in json.loads(data.content)["weather"] for (k, v) in e.items()}.get("main"),
            "desc": {k: v for e in json.loads(data.content)["weather"] for (k, v) in e.items()}.get("description"),
            "temp": int(json.loads(data.content)["main"].get("temp")),
            "wind": int(json.loads(data.content)["wind"].get("speed")),
            "pressure": json.loads(data.content)["main"].get("pressure"),
            "humidity": json.loads(data.content)["main"].get("humidity"),
            "precipitation": int(json.loads(data_forecast.content)["daily"][0].get("pop") * 100),
            "time": get_date(json.loads(data.content)['timezone'])[0],
            "curTime": get_date(json.loads(data.content)['timezone'])[1],
            "date": get_date(json.loads(data.content)['timezone'])[2],
            "days": days_weather,
            "names": days_names,
            "tooltip": tooltip_info,
            "id": f"{city_id}",
        }
        weather.append(dict_with_weather_info)

        if conn:
            cur.close()
            conn.close()

    return render_template('index.html', weather=weather, counties=countries_codes.items())
