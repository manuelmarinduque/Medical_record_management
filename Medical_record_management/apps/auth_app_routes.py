from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import check_password_hash
from functools import wraps
from jwt import encode
from os import environ

from Medical_record_management.database import db
from .aux_functions import get_user, create_patient_user, create_hospital_user

import datetime


auth_app = Blueprint('auth', __name__)

@auth_app.route("/create_user/<user_type>", methods=['POST'])
def create_user(user_type):
    if user_type == 'patient':
        create_patient_user()
    elif user_type == 'hospital':
        create_hospital_user()
    return jsonify({'message':'New user was created succesfully.'})

@auth_app.route("/<user_type>/login", methods=['POST'])
def login(user_type):
    auth = request.authorization
    print(auth)

    if auth and auth.username and auth.password:
        user = get_user(user_type, auth)
        if user:
            if check_password_hash(user.password, auth.password):
                token = encode(
                    {'public_id': user.public_id, 
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 
                    environ.get('SECRET_KEY')
                )
                return jsonify({'token': token.decode('utf-8')})
            else:
                return make_response('Incorrect password', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
        else:
            return make_response('User not found', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    else:
        return make_response('User not verified', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
