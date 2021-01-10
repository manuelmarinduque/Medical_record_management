from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
import uuid

from Medical_record_management.models import Hospital, Patient, Doctor, HospitalService, DoctorSpeciality
from Medical_record_management.database import db
  

def get_user(**kwargs):
    for class_type in (Patient, Hospital, Doctor):
        if 'auth' in kwargs:
            user = class_type.query.filter_by(identification=kwargs['auth'].username).first()
        elif 'public_id' in kwargs:
            user = class_type.query.filter_by(public_id=kwargs['public_id']).first()
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
    create_services(services, user.id, user_type)

def create_services(services, id, user_type):
    for service in services:
        if user_type == 'hospital':
            new_service = HospitalService(hospital_id=id, service_id=service)
        elif user_type == 'doctor':
            new_service = DoctorSpeciality(doctor_id=id, medical_speciality_id=service)
        save(new_service)

def create_doctor(user_type):
    extra_data = get_extra_data()
    specialities = extra_data['specialities']
    extra_data.pop('specialities')
    user = create_new_user(user_type, extra_data)
    save(user)
    create_services(specialities, user.id, user_type)

def create_new_user(user_type, extra_data):
    for class_type in (Patient, Hospital, Doctor):
        if user_type.capitalize() == class_type.__name__:
            user = class_type(public_id=str(uuid.uuid4()), user_type=user_type, **extra_data)
            return user

def get_extra_data():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    data['password'] = hashed_password
    return data

def save(element=None):
    if element:
        db.session.add(element)
    db.session.commit()
