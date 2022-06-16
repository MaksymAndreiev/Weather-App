from core import db
from models.base import Model


class Users(Model, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False) # список стран
    preferences = db.relationship('UserPreferences', backref='users', lazy='dynamic', cascade='all, delete')
    # users_cities = db.relationship('UsersCity', backref='users', lazy='dynamic', cascade='all, delete')
