from core import db
from models.base import Model


class UserPreferences(Model, db.Model):
    __tablename__ = 'user_preferences'
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    measuring_units_id = db.Column(db.Integer, db.ForeignKey('measuring_units.id'), nullable=False)
