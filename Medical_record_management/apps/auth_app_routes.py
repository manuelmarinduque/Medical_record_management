from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import check_password_hash
from functools import wraps
from jwt import encode, decode
from os import environ

from Medical_record_management.database import db
from .aux_functions import get_user, create_patient_user, create_hospital_user, create_doctor

import datetime


auth_app = Blueprint('auth', __name__)

def token_required(route):
    @wraps(route)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try: 
            data = decode(token, environ.get('SECRET_KEY'))
            print(data)
            current_user = get_user(public_id=data['public_id'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return route(current_user, *args, **kwargs)

    return decorated

@auth_app.route("/create_user/<user_type>", methods=['POST'])
def create_user(user_type):
    data = request.get_json()

    if get_user(identification=data['identification']) is not None:
        return make_response('This user exists in the database', 401)
    elif user_type == 'patient':
        create_patient_user(user_type)
    elif user_type == 'hospital':
        create_hospital_user(user_type)

    return jsonify({'message': f'New {user_type} user was created succesfully.'}), 200

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

@auth_app.route("/hospital/create_doctor", methods=['POST'])
@token_required
def create_doctor_user(current_user):
    if current_user.user_type == 'hospital':
        create_doctor('doctor')
        return jsonify({'message':'New doctor user was created succesfully.'}), 200
    else:
        return make_response("You don't have permissions to perform this task.", 401)
