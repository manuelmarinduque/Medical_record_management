from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
import uuid

from Medical_record_management.models import (Hospital, Patient, Doctor, HospitalService,
DoctorSpeciality, MedicalRegister, MedicalSpeciality)
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

def create_medical_register(current_user, data, speciality):
    medical_speciality = MedicalSpeciality.query.filter_by(id=speciality).first()
    data.pop('medical_speciality')
    register = MedicalRegister(
        doctor_id = current_user.id,
        hospital_id = current_user.hospital_id,
        medical_speciality = medical_speciality.speciality_name,
        **data)
    save(register)

def save(element=None):
    if element:
        db.session.add(element)
    db.session.commit()

def get_doctor_specialities(id):
    specialities = DoctorSpeciality.query.filter_by(doctor_id=id)
    return [speciality.medical_speciality_id for speciality in specialities]

def get_medical_records(current_user):
    if isinstance(current_user, Patient):
        raw_records = MedicalRegister.query.filter_by(patient_id=current_user.id)
    elif isinstance(current_user, Hospital):
        raw_records = MedicalRegister.query.filter_by(hospital_id=current_user.id)
    else:
        raw_records = MedicalRegister.query.filter_by(doctor_id=current_user.id)
        print(raw_records)
    records = records_to_dict(raw_records)
    return records

def records_to_dict(raw_records):
    records = [{'id':obj.id,
                'patient_id':obj.patient_id,
                'doctor_id':obj.doctor_id,
                'hospital_id':obj.hospital_id,
                'date':obj.date,
                'medical_speciality':obj.medical_speciality,
                'description':obj.description,
                'health_state':obj.health_state
                } for obj in raw_records]
    return records
