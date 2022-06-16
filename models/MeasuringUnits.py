from core import db
from models.base import Model


class MeasuringUnits(Model, db.Model):
    __tablename__ = 'measuring_units'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    unit_name = db.Column(db.String(20), unique=True, nullable=False)
    unit_description = db.Column(db.String(100), unique=True, nullable=False)
    # preferences = db.relationship('UserPreferences', backref='measuring_units', lazy='dynamic', cascade='all, delete')
    