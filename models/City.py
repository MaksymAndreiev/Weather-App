from core import db
from models.base import Model


class City(Model, db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(200), unique=True, nullable=False)
    longitude = db.Column(db.Float(decimal_return_scale=2), unique=True, nullable=False)
    latitude = db.Column(db.Float(decimal_return_scale=2), unique=True, nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    hours = db.relationship('HourlyForecast', backref='city', lazy='dynamic', cascade='all, delete')
    days = db.relationship('DailyForecast', backref='city', lazy='dynamic', cascade='all, delete')
    #users = db.relationship('UsersCity', backref='city', lazy='dynamic', cascade='all, delete')

