from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import check_password_hash
from functools import wraps
from jwt import encode, decode
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

@auth_app.route("/login", methods=['POST'])
def login():
    auth = request.authorization

    if auth.username and auth.password:
        user = get_user(auth=auth)
        if user:
            if check_password_hash(user.password, auth.password):
                token = encode(
                    {'public_id': user.public_id, 
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 
                    environ.get('SECRET_KEY')
                )
                return jsonify({'token': token.decode('utf-8')})
            else:
                return make_response('Incorrect password', 401)
        else:
            return make_response('User not found', 401)
    else:
        return make_response('Must enter an username or password', 401)
