from flask import Blueprint, request, jsonify

from Medical_record_management.models import HospitalService, Hospital, Service, Patient, DoctorSpeciality, Doctor, MedicalSpeciality, MedicalRegister
from Medical_record_management.database import db
from .aux_functions import create_patient_user, create_hospital_user


auth_app = Blueprint('auth', __name__)

@auth_app.route("/create_user/<user_type>", methods=['POST'])
def create_user(user_type):
    if user_type == 'patient':
        create_patient_user()
    elif user_type == 'hospital':
        create_hospital_user()
    return jsonify({'message':'New user was created succesfully.'})
