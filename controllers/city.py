import requests
from flask import request, redirect, flash

from controllers.parse_request import city_data, hourly_data, daily_data, weather_data
from models.City import City
from models.DailyForecast import DailyForecast
from models.HourlyForecast import HourlyForecast
from settings.constants import api_key


def get_all_cities():
    """
    Get list of all records
    """
    all_cities = City.query.all()
    return all_cities


def add_city():
    # conn = psycopg2.connect(user="root", password="root", host="localhost", port="5432",
    #                         dbname="weather_app")
    # cur = conn.cursor()
    #
    # cur.execute(f"select unit_name from measuring_units where id = {pref_id}")
    # pref_units = cur.fetchone()[0]
    # cur.close()
    # conn.close()
    city_name = request.form.get('city_name')
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}')
    if response.status_code == 404:
        flash("The city doesn't exist!")
        return redirect('/')
    cities = get_all_cities()
    for city in cities:
        if city[1] == city_name:
            flash("The city has already been added to the list!")
            return redirect('/')
    else:
        data = city_data(city_name)
        City.create(**data)
        h_data = hourly_data(city_name)
        HourlyForecast.create(**h_data)
        for i in range(0, 7):
            d_data = daily_data(city_name, i)
            DailyForecast.create(**d_data)
        return redirect('/')


def delete(city_id):
    City.delete(city_id)
    return redirect('/')
