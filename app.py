from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine
import sys
import requests
import json
import datetime

app = Flask(__name__)
# db = create_engine('sqlite:///weather.db?check_same_thread=False')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)
api_key = ['80d2dcec03133dc269c9a17fea6df313', 'be239b2e9342bb6379f7f5a1a1f81a71']
app.secret_key = 'secret_key'


class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)


db.create_all()


@app.template_filter('positive')
def positive(arr):
    return all(val >= 0 for val in arr)


@app.route('/')
def index():
    def get_date(timezone):
        tz = datetime.timezone(datetime.timedelta(seconds=int(timezone)))
        day = datetime.datetime.now(tz=tz).date().strftime("%a, %d %b")
        time = datetime.datetime.now(tz=tz).time().strftime("%H:%M")
        hour = datetime.datetime.now(tz=tz).time().hour
        return hour, time, day

    def get_date_name(dt):
        date = datetime.datetime.fromtimestamp(dt)
        day = date.date().strftime("%a")
        return day

    weather = []
    cities = City.query.all()
    for city in cities:
        city_name = city.name

        try:
            data = requests.get(
                f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key[0]}&units=metric')
            data.raise_for_status()
        except ConnectionError:
            data = requests.get(
                f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key[1]}&units=metric')

        lat = json.loads(data.content)["coord"].get("lat")
        lon = json.loads(data.content)["coord"].get("lon")

        try:
            data_forecast = requests.get(
                f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,'
                f'alerts&appid={api_key[0]}&units=metric')
        except ConnectionError:
            data_forecast = requests.get(
                f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,'
                f'alerts&appid={api_key[1]}&units=metric')

        days_weather = list(
            int(json.loads(data_forecast.content)["daily"][i].get("temp").get("day")) for i in range(1, 8))
        days_names = ['i' for i in range(7)]
        for i in range(1, 8):
            days_names[i - 1] = get_date_name(json.loads(data_forecast.content)["daily"][i].get('dt'))

        tooltip_info = [
            list(int(json.loads(data_forecast.content)["daily"][i].get("temp").get("day")) for i in range(1, 8)),
            list(int(json.loads(data_forecast.content)["daily"][i].get("temp").get("night")) for i in range(1, 8)),
            list(int(json.loads(data_forecast.content)["daily"][i].get("feels_like").get("day")) for i in range(1, 8)),
            list(int(json.loads(data_forecast.content)["daily"][i].get("feels_like").get("night")) for i in range(1, 8))
        ]

        dict_with_weather_info = {
            "name": json.loads(data.content)["name"],
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
            "id": f"{city.id}",
        }
        weather.append(dict_with_weather_info)
    return render_template('index.html', weather=weather)


@app.route('/add', methods=['GET', 'POST'])
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


@app.route('/delete/<city_id>', methods=['GET', 'POST'])
def delete(city_id):
    city = City.query.filter_by(id=city_id).first()
    db.session.delete(city)
    db.session.commit()
    return redirect('/')


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
