from flask import Flask

from .apps.auth_app_routes import auth_app
from .database import db

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'a-18c3%!*qhz4_bs1-nt7yb2fq8xlv8d_7cyx^5i-o+qqmty@'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Manuel:1234@localhost/Medical_record_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(auth_app)
    
    return app
