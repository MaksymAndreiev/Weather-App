from core import db
from models.base import Model


class HourlyForecast(Model, db.Model):
    __tablename__ = 'hourly_forecast'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id', ondelete='CASCADE'), nullable=False)
    weather_status_id = db.Column(db.Integer, db.ForeignKey('weather_status.id', ondelete='CASCADE'), nullable=False)
    temperature = db.Column(db.Integer, nullable=False)
    wind_speed = db.Column(db.Float(decimal_return_scale=2), nullable=False)
    pressure = db.Column(db.Float(decimal_return_scale=2), nullable=False)
    humidity = db.Column(db.Float(decimal_return_scale=2),  nullable=False)
    precipitation = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Integer, nullable=False)
    curr_time = db.Column(db.String(5), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    units = db.Column(db.String(10), nullable=False)
