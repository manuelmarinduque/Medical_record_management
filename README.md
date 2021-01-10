# Para ejecución del servicio web
1. Se debe utilizar una aplicación tal como Postman o Insomnia para realizar las peticiones al servidor.

2. Instalar las depencias definidas en el archivo requeriments.txt.

3. Realizar migraciones de los modelos a la base de datos, especificando antes la base de datos a utilizar, con los siguientes comandos:

    from Medical_record_management.models import HospitalService, Hospital, Service, Patient, DoctorSpeciality, Doctor, MedicalSpeciality, MedicalRegister
    
    from Medical_record_management import create_app
    
    from Medical_record_management.database import db
    
    db.create_all(app=create_app())
    
4. Ejecutar aplicación con el comando:

    flask run
