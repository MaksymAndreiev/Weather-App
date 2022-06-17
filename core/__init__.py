from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from settings.constants import DB_URL

db = SQLAlchemy()  # Database creation


def create_app():
    """Construct the core application."""
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning
    app.secret_key = 'secret_key'

    db.init_app(app)

    with app.app_context():
        from . import routes

        # Create tables for our models
        db.create_all()

        return app
