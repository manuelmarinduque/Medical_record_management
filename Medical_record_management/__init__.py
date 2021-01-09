from flask import Flask
from os import environ

from .apps.auth_app_routes import auth_app
from .database import db


def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Manuel:1234@localhost/Medical_record_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(auth_app)
    
    return app
