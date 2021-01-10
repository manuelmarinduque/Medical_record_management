from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from jwt import encode
from os import environ
from sqlalchemy.exc import IntegrityError

from Medical_record_management.database import db
from .decorators import token_required
from .aux_functions import (save, get_user, create_patient_user, create_hospital_user,
create_doctor, create_medical_register, get_doctor_specialities, get_medical_records)

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
        return jsonify({'message': f"May be this {user_type} user exists in the database or you din't enter all the requerided values."})

@auth_app.route("/login", methods=['POST'])
def login():
    auth = request.authorization
    user = get_user(auth=auth)
    if not user:
        return jsonify({'message': "User not found."})
    else:
        if not check_password_hash(user.password, auth.password):
            return jsonify({'message': "Incorrect password."})
        else:
            token = encode({'public_id': user.public_id, 
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 
                            environ.get('SECRET_KEY'))
            return jsonify({'token': token.decode('utf-8'), 'user_name': user.name})

@auth_app.route("/hospital/create_doctor", methods=['POST'])
@token_required
def create_doctor_user(current_user):
    if not current_user.user_type == 'hospital':
        return jsonify({'message': "You don't have permissions to perform this task."})
    elif not current_user.is_verificated:
        return jsonify({'message': 'You must verify your account. Please check your email imbox.'})
    else:
        try:
            create_doctor('doctor')
            return jsonify({'message': 'New doctor user was created successfully.'}), 200
        except IntegrityError:
            return jsonify({'message': 'This doctor user exists in the database.'})

@auth_app.route('/user/account_confirmation/<public_id>', methods=['PUT'])
def account_confirmation(public_id):
    user = get_user(public_id=public_id)
    if not user:
        return jsonify({'message' : "This user doen's exist."})
    else:
        user.is_verificated = True
        save()
        return jsonify({'message' : f'The user {user.name} has the account verificated.'})

@auth_app.route('/user/change_password', methods=['PUT'])
@token_required
def change_password(current_user):
    data = request.get_json()
    new_password = data.get('password')
    if check_password_hash(current_user.password, new_password):
        return jsonify({'message' : 'The new password matches with the old one.'})
    else:
        current_user.password = generate_password_hash(new_password, method='sha256')
        if current_user.user_type == 'doctor' and not current_user.password_changed:
            current_user.password_changed = True
        save()
        return jsonify({'message': 'The password has been changed successfully.'})

@auth_app.route('/doctor/medical_register', methods=['POST'])
@token_required
def medical_register(current_user):
    if not current_user.user_type == 'doctor':
        return jsonify({'message': "You don't have permissions to perform this task."})
    else:        
        if not current_user.is_verificated:
            return jsonify({'message': 'You must verify your account. Please check your email imbox.'})
        elif not current_user.password_changed:
            return jsonify({'message': 'You must change your password.'})
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

@auth_app.route('/user/consult_medical_record')
@token_required
def consult_medical_record(current_user):
    if not current_user.is_verificated:
        return jsonify({'message': 'You must verify your account. Please check your email imbox.'})
    if current_user.user_type == 'doctor' and not current_user.password_changed:
        return jsonify({'message': 'You must change your password.'})
    medical_records = get_medical_records(current_user)
    if medical_records:
        return jsonify({'data': medical_records})
    else:
        return jsonify({'message': f"{current_user.__class__.__name__} user doesn't have registers yet."})
