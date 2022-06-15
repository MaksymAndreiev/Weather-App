from core import db
from models.base import Model


class UsersCity(Model, db.Model):
    __tablename__ = 'users_city'
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    city_id = db.Column(db.Integr, db.ForeignKey('city.id'), primary_key=True, nullable=False)
    added_on = db.Column(db.Date, unique=True, nullable=False)
    