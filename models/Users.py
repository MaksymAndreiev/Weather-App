from core import db
from models.base import Model


class Users(Model, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    nickname = db.Column(db.String(50), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False) # список стран
    preferences = db.relationship('UserPreferences', backref='users', lazy='dynamic', cascade='all, delete')
    users_cities = db.relationship('UsersCity', backref='users', lazy='dynamic', cascade='all, delete')
