from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from settings.constants import DB_URL

db = SQLAlchemy()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning

    db.init_app(app)

    with app.app_context():

        # Create tables for our models
        db.create_all()

        return app