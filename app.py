from flask import Flask
from flask_cors import CORS

from models.medicalappointment_model import MedicalAppointmentsModel
from services.medicalappointment_service import MedicalAppointmentService
from schemas.medicalappointment_schema import MedicalAppointmentSchema
from routes.medicalappointment_routes import MedicalAppointmentRoute

from models.patient_model import PatientModel
from services.patient_service import PatientService
from schemas.patient_schema import PatientSchema
from routes.patient_routes import PatientRoutes
from flasgger import Swagger
from services.nlp_service import NLPService 

from routes.doctor_routes import DoctorRoutes
from services.doctor_service import DoctorService
from schemas.doctor_schema import DoctorSchema
from models.doctor_model import DoctorModel

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
swagger = Swagger(app)

# Medical Appointment
db_conn_medicalappointment = MedicalAppointmentsModel()
db_conn_medicalappointment.connect_to_database()
medicalappointment_service = MedicalAppointmentService(db_conn_medicalappointment)
medicalappointment_schema = MedicalAppointmentSchema()
medicalappointment_routes = MedicalAppointmentRoute(medicalappointment_service, medicalappointment_schema)
app.register_blueprint(medicalappointment_routes)



db_conn_patient= PatientModel()
db_conn_patient.connect_to_database()
nlp_service = NLPService()
patient_service = PatientService(db_conn_patient,nlp_service)
patient_schema = PatientSchema()
patient_routes = PatientRoutes(patient_service, patient_schema)
app.register_blueprint(patient_routes)



db_conn_doctor = DoctorModel()
db_conn_doctor.connect_to_database()
doctor_service = DoctorService(db_conn_doctor)
doctor_schema = DoctorSchema()

doctor_routes = DoctorRoutes(doctor_service, doctor_schema)
app.register_blueprint(doctor_routes)





# Ejecutar la aplicación
if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        db_conn_medicalappointment.close_connection()
        
        db_conn_patient.close_connection()
        
        db_conn_doctor.close_connection()
