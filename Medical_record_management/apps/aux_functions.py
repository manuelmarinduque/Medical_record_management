from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
import uuid

from Medical_record_management.models import Hospital, Patient, Doctor, HospitalService
from Medical_record_management.database import db
  
    
def create_patient_user():
    extra_data = get_extra_data()
    user = Patient(
        public_id=str(uuid.uuid4()),
        user_type='patient',
        **extra_data
    )
    save(user)

def create_hospital_user():
    extra_data = get_extra_data()
    services = extra_data['services']
    extra_data.pop('services')
    user = Hospital(
        public_id=str(uuid.uuid4()),
        user_type='hospital',
        **extra_data
    )
    save(user)
    create_hospital_services(services, user.id)

def create_hospital_services(services, id):
    for service in services:
        new_service = HospitalService(hospital_id=id, service_id=service)
        save(new_service)

def get_extra_data():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    data['password'] = hashed_password
    return data

def save(element):
    db.session.add(element)
    db.session.commit()
