import requests
from flask import request, redirect, flash

from core import db
from models.City import City



def add_city():
    city_name = request.form.get('city_name')
    response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}')
    if response.status_code == 404:
        flash("The city doesn't exist!")
        return redirect('/')
    cities = City.query.all()
    for city in cities:
        if city.name == city_name:
            flash("The city has already been added to the list!")
            return redirect('/')
    else:
        city = City(name=city_name)
        db.session.add(city)
        db.session.commit()

        return redirect('/')


def delete(city_id):
    city = City.query.filter_by(id=city_id).first()
    db.session.delete(city)
    db.session.commit()
    return redirect('/')
