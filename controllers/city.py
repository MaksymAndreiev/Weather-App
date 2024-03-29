import requests
import psycopg2
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
    conn = psycopg2.connect(user="root", password="root", host="127.0.0.1", port="5432",
                            dbname="weather_app")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM city")
    all_cities = [r for r in cur.fetchall()]
    return all_cities


def add_city():
    units = request.form.get('units')
    city_name = request.form.get('city_name')
    if city_name == "":
        flash("Error! Empty string")
        return redirect('/')
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
        data = city_data(city_name, units)
        if type(data) is not dict:
            flash("The city has already been added to the list!")
            return redirect('/')
        City.create(**data)
        h_data = hourly_data(city_name, units)
        HourlyForecast.create(**h_data)
        for i in range(0, 7):
            d_data = daily_data(city_name, i, units)
            DailyForecast.create(**d_data)
        return redirect('/')


def delete(city_id):
    City.delete(city_id)
    return redirect('/')
