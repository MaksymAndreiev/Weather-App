import requests
from flask import request, redirect, flash

from models.City import City
from settings.constants import api_key


def get_all_cities():
    """
    Get list of all records
    """
    all_cities = City.query.all()
    return all_cities


def add_city():
    city_name = request.form.get('city_name')
    response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}')
    if response.status_code == 404:
        flash("The city doesn't exist!")
        return redirect('/')
    cities = get_all_cities()
    for city in cities:
        if city.name == city_name:
            flash("The city has already been added to the list!")
            return redirect('/')
    else:
        City().create(name=city_name)
        return redirect('/')


def delete(city_id):
    City.delete(city_id)
    return redirect('/')
