from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
import uuid

from Medical_record_management.models import Hospital, Patient, Doctor, HospitalService
from Medical_record_management.database import db
  

def get_user(**kwargs):
    for class_type in (Patient, Hospital, Doctor):
        if 'auth' in kwargs:
            user = class_type.query.filter_by(identification=kwargs['auth'].username).first()
        elif 'public_id' in kwargs:
            user = class_type.query.filter_by(public_id=kwargs['public_id'].username).first()
        if user:
            return user

def create_patient_user(user_type):
    extra_data = get_extra_data()
    user = create_new_user(user_type, extra_data)
    save(user)

def create_hospital_user(user_type):
    extra_data = get_extra_data()
    services = extra_data['services']
    extra_data.pop('services')
    user = create_new_user(user_type, extra_data)
    save(user)
    create_hospital_services(services, user.id)

def create_hospital_services(services, id):
    for service in services:
        new_service = HospitalService(hospital_id=id, service_id=service)
        save(new_service)

def create_doctor_user():
    pass

def create_new_user(user_type, extra_data):
    for class_type in (Patient, Hospital, Doctor):
        print(class_type.__name__)
        if user_type.capitalize() == class_type.__name__:
            user = class_type(public_id=str(uuid.uuid4()), user_type=user_type, **extra_data)
            return user

def get_extra_data():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    data['password'] = hashed_password
    return data

def save(element):
    db.session.add(element)
    db.session.commit()
