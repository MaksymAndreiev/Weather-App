from core import db
from models.base import Model


class WeatherStatus(Model, db.Model):
    __tablename__ = 'weather_status'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(50), unique=True, nullable=False)
    hours = db.relationship('HourlyForecast', backref='weather_status', lazy='dynamic')
    days = db.relationship('DailyForecast', backref='weather_status', lazy='dynamic')
