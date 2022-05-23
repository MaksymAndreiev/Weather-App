from core import db
from models.base import Model


class Daily_forecast(Model, db.Model):
    __tablename__ = 'daily_forecast'
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, unique=True, nullable=False)
    day_name = db.Column(db.String(3), unique=True, nullable=False)
    weather_status_id = db.Column(db.Integer, unique=True, nullable=False)
    day_temperature = db.Column(db.Integer, unique=True, nullable=False)
    night_temperature = db.Column(db.Integer, unique=True, nullable=False)
    feels_like_day = db.Column(db.Integer, unique=True, nullable=False)
    feels_like_night = db.Column(db.Integer, unique=True, nullable=False)
    wind_speed = db.Column(db.Float(decimal_return_scale=1), unique=True, nullable=False)
    pressure = db.Column(db.Float(decimal_return_scale=2), unique=True, nullable=False)
    humidity = db.Column(db.Float(decimal_return_scale=2), unique=True, nullable=False)
    precipitation = db.Column(db.Integer, unique=True, nullable=False)