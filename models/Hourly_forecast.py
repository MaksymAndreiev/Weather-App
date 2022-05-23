from core import db
from models.base import Model


class Hourly_forecast(Model, db.Model):
    __tablename__ = 'hourly_forecast'
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, unique=True, nullable=False)
    weather_status_id = db.Column(db.Integer, unique=True, nullable=False)
    temperature = db.Column(db.Integer, unique=True, nullable=False)
    wind_speed = db.Column(db.Float(decimal_return_scale=2), unique=True, nullable=False)
    pressure = db.Column(db.Float(decimal_return_scale=2), unique=True, nullable=False)
    humidity = db.Column(db.Float(decimal_return_scale=2), unique=True, nullable=False)
    precipitation = db.Column(db.Integer, unique=True, nullable=False)
    time = db.Column(db.Time, unique=True, nullable=False)
    current_time = db.Column(db.Time, unique=True, nullable=False)
    date = db.Column(db.Date, unique=True, nullable=False)
