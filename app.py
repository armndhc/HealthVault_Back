from flask import Flask
from flask_cors import CORS
from models.recipe_model import RecipeModel
from services.recipe_services import RecipeService
from schemas.recipe_schemas import RecipeSchema
from routes.recipe_routes import RecipeRoutes

from models.payment_model import PaymentModel
from services.payment_services import PaymentService
from schemas.payment_schemas import PaymentSchema
from routes.payment_route import PaymentRoutes

from models.medication_model import MedicationModel
from services.medication_service import MedicationService
from schemas.medication_schema import MedicationSchema
from routes.medication_routes import MedicationRoutes

from models.medicalappointment_model import MedicalAppointmentsModel
from services.medicalappointment_service import MedicalAppointmentService
from schemas.medicalappointment_schema import MedicalAppointmentSchema
from routes.medicalappointment_routes import MedicalAppointmentRoute

from models.patient_model import PatientModel
from services.patient_service import PatientService
from schemas.patient_schema import PatientSchema
from routes.patient_routes import PatientRoutes
from services.nlp_service import NLPService 

from routes.doctor_routes import DoctorRoutes
from services.doctor_service import DoctorService
from schemas.doctor_schema import DoctorSchema
from models.doctor_model import DoctorModel
from flasgger import Swagger

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
swagger = Swagger(app)

# Recipe
app = Flask(__name__)
CORS(app)
swagger = Swagger(app)
db_conn_recipe = RecipeModel()
db_conn_recipe.connect_to_database()
recipe_service = RecipeService(db_conn)
recipe_schema = RecipeSchema()
recipe_routes = RecipeRoutes(recipe_service, recipe_schema)
app.register_blueprint(recipe_routes)

# Payment
db_conn = PaymentModel()
db_conn.connect_to_database()
payment_service = PaymentService(db_conn)
payment_schema = PaymentSchema()
payment_routes = PaymentRoutes(payment_service, payment_schema)
app.register_blueprint(payment_routes)

# Medication
db_conn_medication = MedicationModel()
db_conn_medication.connect_to_database()
medication_service = MedicationService(db_conn_medication)
medication_schema = MedicationSchema()
medication_routes = MedicationRoutes(medication_service, medication_schema)
app.register_blueprint(medication_routes)


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
        db_conn_recipe.close_connection()
        db_conn.close_connection()
        db_conn_medication.close_connection()
        db_conn_medicalappointment.close_connection()
        db_conn_patient.close_connection()
        db_conn_doctor.close_connection()
