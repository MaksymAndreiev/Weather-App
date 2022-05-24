from core import db
from models.base import Model


class DailyForecast(Model, db.Model):
    __tablename__ = 'daily_forecast'
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, nullable=False)
    day_id = db.Column(db.Integer, nullable=False)
    day_name = db.Column(db.String(3), nullable=False)
    weather_status_id = db.Column(db.Integer, nullable=False)
    day_temperature = db.Column(db.Integer, nullable=False)
    night_temperature = db.Column(db.Integer, nullable=False)
    feels_like_day = db.Column(db.Integer, nullable=False)
    feels_like_night = db.Column(db.Integer,  nullable=False)
    precipitation = db.Column(db.Integer, nullable=False)
