# Para ejecución del servicio web
1. Se debe utilizar una aplicación tal como Postman o Insomnia para realizar las peticiones al servidor.
2. Instalar las depencias definidas en el archivo requeriments.txt.
3. Realizar migraciones de los modelos a la base de datos, especificando antes la base de datos a utilizar, con los siguientes comandos:
    3.1. from Medical_record_management.models import HospitalService, Hospital, Service, Patient, DoctorSpeciality, Doctor, MedicalSpeciality, MedicalRegister
    3.2. from Medical_record_management import create_app
    3.3. from Medical_record_management.database import db
    3.4. db.create_all(app=create_app())
4. Ejecutar aplicación con el comando: 
    4.1. flask run
