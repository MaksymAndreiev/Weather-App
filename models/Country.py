from core import db
from models.base import Model


class Country(Model, db.Model):
    __tablename__ = 'country'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    # добавить полное имя страны
    cities = db.relationship('City', backref='country', lazy='dynamic', cascade='all, delete')
