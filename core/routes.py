import json

import requests
from flask import render_template, request
from flask import current_app as app

from controllers.city import add_city as add, get_all_cities
from controllers.city import delete as del_


@app.template_filter('positive')
def positive(arr):
    return all(val >= 0 for val in arr)


@app.route('/add', methods=['GET', 'POST'])
def add_city():
    return add()


@app.route('/delete/<city_id>', methods=['GET', 'POST'])
def delete(city_id):
    return del_(city_id)


@app.route('/')
def index():
    weather = []
    cities = get_all_cities()
    for city in cities:

        city_id = city[0]
        city_name = city[1]

        cur.execute(f"SELECT day_temperature FROM daily_forecast WHERE city_id = {city_id}")
        days_weather = [int(r[0]) for r in cur.fetchall()]

        cur.execute(f"SELECT day_name FROM daily_forecast WHERE city_id = {city_id}")
        days_names = [r[0] for r in cur.fetchall()]

        cur.execute(f"SELECT day_temperature FROM daily_forecast WHERE city_id = {city_id}")
        d_temp = [int(r[0]) for r in cur.fetchall()]

        cur.execute(f"SELECT night_temperature FROM daily_forecast WHERE city_id = {city_id}")
        n_temp = [int(r[0]) for r in cur.fetchall()]

        # прогноз погоды по дням где ид города = сити.ид_города (поля)
        tooltip_info = [
            list(int(json.loads(data_forecast.content)["daily"][i].get("temp").get("day")) for i in range(1, 8)),
            list(int(json.loads(data_forecast.content)["daily"][i].get("temp").get("night")) for i in range(1, 8)),
            list(int(json.loads(data_forecast.content)["daily"][i].get("feels_like").get("day")) for i in range(1, 8)),
            list(int(json.loads(data_forecast.content)["daily"][i].get("feels_like").get("night")) for i in range(1, 8))
        ]

        #
        dict_with_weather_info = {
            "name": city_name,
            "state": w_state,
            "desc": w_desc,
            "temp": w_temp,
            "wind": w_wind,
            "pressure": w_pressure,
            "humidity": w_humidity,
            "precipitation": w_prec,
            "time": w_time,
            "curTime": w_currtime,
            "date": w_date.strftime("%a, %d %b"),
            "days": days_weather,
            "names": days_names,
            "tooltip": tooltip_info,
            "id": f"{city_id}",
            "units": units
        }
        weather.append(dict_with_weather_info)

        if conn:
            cur.close()
            conn.close()

    return render_template('index.html', weather=weather)
