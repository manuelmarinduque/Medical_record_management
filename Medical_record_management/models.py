from datetime import datetime
from abc import ABCMeta

from .database import db


hospital_service = ('HospitalService',
    db.Column('pk', db.Integer, primary_key=True),
    db.Column('hospital_pk', db.Integer, db.ForeignKey('hospital.pk')),
    db.Column('service_pk', db.Integer, db.ForeignKey('service.pk'))
)

class Hospital(db.Model):
    pk = db.Column(db.Integer, primary_key=True)
    identification = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)
    is_activated = db.Column(db.Boolean, default=True)
    is_verificated = db.Column(db.Boolean, default=False)
    services = db.relationship('Service', secondary=hospital_service, lazy='dynamic')
    doctors = db.relationship('Doctor', backref='doctor')
    medical_registers = db.relationship('MedicalRegister', backref='medical_register')

class Service(db.Model):
    pk = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(20), nullable=False)

class Patient(db.Model):
    pk = db.Column(db.Integer, primary_key=True)
    identification = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)
    is_activated = db.Column(db.Boolean, default=True)
    is_verificated = db.Column(db.Boolean, default=False)
    birth_day = db.Column(db.DateTime, nullable=False)
    medical_registers = db.relationship('MedicalRegister', backref='medical_register')

doctor_speciality = ('DoctorSpeciality',
    db.Column('pk', db.Integer, primary_key=True),
    db.Column('doctor_pk', db.Integer, db.ForeignKey('doctor.pk')),
    db.Column('medical_speciality_pk', db.Integer, db.ForeignKey('medicalspeciality.pk'))
)

class Doctor(db.Model):
    pk = db.Column(db.Integer, primary_key=True)
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
    hospital_pk = db.Column(db.Integer, db.ForeignKey('hospital.pk'))
    specialities = db.relationship('MedicalSpeciality', secondary=doctor_speciality)
    medical_registers = db.relationship('MedicalRegister', backref='medical_register')

class MedicalSpeciality(db.Model):
    pk = db.Column(db.String(10), primary_key=True)
    speciality_name = db.Column(db.String(20), nullable=False) 

class MedicalRegister(db.Model):
    pk = db.Column(db.Integer, primary_key=True)
    patient_pk = db.Column(db.Integer, db.ForeignKey('patient.pk'))
    doctor_pk = db.Column(db.Integer, db.ForeignKey('doctor.pk'))
    hospital_pk = db.Column(db.Integer, db.ForeignKey('hospital.pk'))
    date = db.Column(db.DateTime, default=datetime.now) 
    medical_speciality = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(10000), nullable=False)
    health_state = db.Column(db.String(10), nullable=False)
