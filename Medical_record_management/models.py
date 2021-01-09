from datetime import datetime

from .database import db


class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    identification = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)
    is_activated = db.Column(db.Boolean, default=True)
    is_verificated = db.Column(db.Boolean, default=False)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(20), nullable=False)

class HospitalService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, nullable=False)
    service_id = db.Column(db.Integer, nullable=False)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    identification = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)
    is_activated = db.Column(db.Boolean, default=True)
    is_verificated = db.Column(db.Boolean, default=False)
    birth_day = db.Column(db.String(10), nullable=False)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    identification = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)
    is_activated = db.Column(db.Boolean, default=True)
    is_verificated = db.Column(db.Boolean, default=False)
    password_changed = db.Column(db.Boolean, default=False)
    hospital_id = db.Column(db.Integer, nullable=False)

class MedicalSpeciality(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    speciality_name = db.Column(db.String(20), nullable=False)

class DoctorSpeciality(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, nullable=False)
    medical_speciality_id = db.Column(db.Integer, nullable=False)

class MedicalRegister(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, nullable=False)
    doctor_id = db.Column(db.Integer, nullable=False)
    hospital_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now) 
    medical_speciality = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(10000), nullable=False)
    health_state = db.Column(db.String(10), nullable=False)
