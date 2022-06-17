import json
import datetime

import psycopg2
import requests
from flask import flash, redirect

from controllers.country import add_country
from models.City import City
from models.Country import Country
from models.WeatherStatus import WeatherStatus
from settings.constants import api_key

global DATA, FORECAST


def weather_id_det(state, i):
    """
    Detect weather id by weather state

    :param state: weather state
    :param i: day index
    :return: weather id
    """
    weather = WeatherStatus.query.filter_by(status=state).first()
    if weather is None:
        w_data = weather_data(i)
        WeatherStatus.create(**w_data)
        weather = WeatherStatus.query.filter_by(status=state).first()
        w_id = weather.id
    else:
        w_id = weather.id
    return w_id


def country_id_det(country_name):
    """
    Detect country id by name

    :param country_name: country name
    :return: country id
    """
    country = Country.query.filter_by(name=country_name).first()
    if country is None:
        add_country(country_name)
        country = Country.query.filter_by(name=country_name).first()
        c_id = country.id
    else:
        c_id = country.id
    return c_id


def get_data(city_name, units):
    """
    Get hourly forecast data from API

    :param city_name: city name
    :param units: measuring units
    """
    data = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units={units}')
    global DATA
    DATA = data


def get_forecast_data(city_name, units):
    """
    Get daily forecast data from API

    :param city_name: city name
    :param units: measuring units
    """
    global FORECAST
    city = City.query.filter_by(name=city_name).first()
    lat = city.latitude
    lon = city.longitude
    data_forecast = requests.get(
        f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,'
        f'alerts&appid={api_key}&units={units}')
    FORECAST = data_forecast


def city_data(city_name, units):
    """
    Get data about the city

    :param city_name: city name
    :param units: measuring units
    :return: city data dictionary
    """
    get_data(city_name, units)
    lat = json.loads(DATA.content)["coord"].get("lat")
    lon = json.loads(DATA.content)["coord"].get("lon")
    conn = psycopg2.connect(user="root", password="root", host="127.0.0.1", port="5432",
                            dbname="weather_app")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM city")
    all_cities = [r for r in cur.fetchall()]
    for city in all_cities:
        if city[2] == lon and city[3] == lat:
            return redirect('/')
    country_name = json.loads(DATA.content)["sys"].get("country")
    c_id = country_id_det(country_name)
    return {'name': city_name, 'longitude': lon, 'latitude': lat, 'country_id': c_id}


def hourly_data(city_name, units):
    """
    Get hourly forecast date

    :param city_name: city name
    :param units: measuring units
    :return: hourly forecast date dictionary
    """
    def get_date(timezone):
        """
        Extract current time from timezone

        :param timezone: offset from UTC
        :return: current time
        """
        tz = datetime.timezone(datetime.timedelta(seconds=int(timezone)))
        day = datetime.datetime.now(tz=tz).date()
        time = datetime.datetime.now(tz=tz).time().strftime("%H:%M")
        hour = datetime.datetime.now(tz=tz).time().hour
        return hour, time, day

    get_forecast_data(city_name, units)
    city = City.query.filter_by(name=city_name).first()
    city_id = city.id
    state = {k: v for e in json.loads(DATA.content)["weather"] for (k, v) in e.items()}.get("main")
    w_id = weather_id_det(state, 0)
    temp = int(json.loads(DATA.content)["main"].get("temp"))
    wind = int(json.loads(DATA.content)["wind"].get("speed"))
    pressure = json.loads(DATA.content)["main"].get("pressure")
    humidity = json.loads(DATA.content)["main"].get("humidity")
    precipitation = int(json.loads(FORECAST.content)["daily"][0].get("pop") * 100)
    time = get_date(json.loads(DATA.content)['timezone'])[0]
    current_time = get_date(json.loads(DATA.content)['timezone'])[1]
    date = get_date(json.loads(DATA.content)['timezone'])[2]
    return {'city_id': city_id, 'weather_status_id': w_id, 'temperature': temp, 'wind_speed': wind,
            'pressure': pressure, 'humidity': humidity, 'precipitation': precipitation, 'time': time,
            'curr_time': current_time, 'date': date, 'units': units}


def daily_data(city_name, day_number, units):
    """
    Get daily data

    :param city_name: city name
    :param day_number: day number
    :param units: measuring units
    :return: daily date dictionary
    """

    def get_date_name(dt):
        """
        Get day of the week by date point

        :param dt: date point
        :return: current day of the week
        """
        date = datetime.datetime.fromtimestamp(dt)
        day = date.date().strftime("%a")
        return day

    city = City.query.filter_by(name=city_name).first()
    city_id = city.id
    i = day_number + 1
    day_id = i
    day_name = get_date_name(json.loads(FORECAST.content)["daily"][i].get('dt'))
    state = {k: v for e in json.loads(FORECAST.content)["daily"][i]["weather"] for (k, v) in e.items()}.get("main")
    w_id = weather_id_det(state, i)
    day_temperature = int(json.loads(FORECAST.content)["daily"][i].get("temp").get("day"))
    night_temperature = int(json.loads(FORECAST.content)["daily"][i].get("temp").get("night"))
    feels_like_day = int(json.loads(FORECAST.content)["daily"][i].get("feels_like").get("day"))
    feels_like_night = int(json.loads(FORECAST.content)["daily"][i].get("feels_like").get("night"))
    precipitation = int(json.loads(FORECAST.content)["daily"][i].get("pop") * 100)
    return {'city_id': city_id, 'day_id': day_id, 'day_name': day_name, 'weather_status_id': w_id,
            'day_temperature': day_temperature, 'night_temperature': night_temperature,
            'feels_like_day': feels_like_day, 'feels_like_night': feels_like_night, 'precipitation': precipitation,
            'units': units}


def weather_data(i):
    """
    Get weather forecast data by day index

    :param i: day index
    :return: weather state dictionary
    """
    if i == 0:
        state = {k: v for e in json.loads(DATA.content)["weather"] for (k, v) in e.items()}.get("main")
        desc = {k: v for e in json.loads(DATA.content)["weather"] for (k, v) in e.items()}.get("description")
    else:
        state = {k: v for e in json.loads(FORECAST.content)["daily"][i]["weather"] for (k, v) in e.items()}.get("main")
        desc = {k: v for e in json.loads(FORECAST.content)["daily"][i]["weather"] for (k, v) in e.items()}.get(
            "description")
    return {'status': state, 'description': desc}
