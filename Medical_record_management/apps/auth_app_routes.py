from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from jwt import encode
from os import environ
from sqlalchemy.exc import IntegrityError

from Medical_record_management.database import db
from .decorators import token_required
from .aux_functions import (save, get_user, create_patient_user, create_hospital_user, 
    create_doctor, create_medical_register, get_doctor_specialities)

import datetime


auth_app = Blueprint('auth', __name__)

@auth_app.route("/create_user/<user_type>", methods=['POST'])
def create_user(user_type):
    try:
        if user_type == 'patient':
            create_patient_user(user_type)
        elif user_type == 'hospital':
            create_hospital_user(user_type)
        else:
            return jsonify({'message': 'Incorrect url.'})
        return jsonify({'message': f'New {user_type} user was created succesfully.'}), 200
    except IntegrityError as e:
        return make_response(f"May be this {user_type} user exists in the database or you din't enter all the requerided values", 401)

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
                return jsonify({'token': token.decode('utf-8'),
                                'user_name': user.name})
            else:
                return make_response('Incorrect password', 401)
        else:
            return make_response('User not found', 401)
    else:
        return make_response('Must enter an username or password', 401)

@auth_app.route("/user/hospital/create_doctor", methods=['POST'])
@token_required
def create_doctor_user(current_user):
    if not current_user.user_type == 'hospital':
        return make_response("You don't have permissions to perform this task.", 401)
    elif not current_user.is_verificated:
        return jsonify({'message': 'You must verify your account. Please check your imbox.'})
    else:
        try:
            create_doctor('doctor')
            return jsonify({'message':'New doctor user was created successfully.'}), 200
        except IntegrityError:
            return make_response(f'This doctor user exists in the database', 401)

@auth_app.route('/user/account_confirmation/<public_id>', methods=['PUT'])
def account_confirmation(public_id):
    user = get_user(public_id=public_id)
    user.is_verificated = True
    save()
    return jsonify({'message' : f'The user {user.name} has the account verificated.'})

@auth_app.route('/user/change_password', methods=['PUT'])
@token_required
def change_password(current_user):
    data = request.get_json()
    new_password = data.get('password')
    if check_password_hash(current_user.password, new_password):
        return make_response('The new password matches with the old one', 401)
    else:
        current_user.password = generate_password_hash(new_password, method='sha256')
        if current_user.user_type == 'doctor' and not current_user.password_changed:
            current_user.password_changed = True
        save()
        return jsonify({'message' : 'The password has changed successfully.'})

@auth_app.route('/doctor/medical_register', methods=['POST'])
@token_required
def medical_register(current_user):
    if not current_user.user_type == 'doctor':
        return make_response("You don't have permissions to perform this task.", 401)
    else:        
        if not current_user.is_verificated:
            return jsonify({'message': 'You must verify your account. Please check your imbox.'})
        elif not current_user.password_changed:
            return jsonify({'message': 'You must change your password. Please visit '})
        else:
            doctor_specialities = get_doctor_specialities(current_user.id)
            print(doctor_specialities)
            data = request.get_json() 
            speciality = data.get('medical_speciality')
            if speciality in doctor_specialities:
                create_medical_register(current_user, data, speciality)
                return jsonify({'message': "The medical register was created successfully."})
            else:
                return jsonify({'message': f"The doctor {current_user.name} doesn't have the selected speciality"})
    