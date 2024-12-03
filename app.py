from flask import Flask
from flask_cors import CORS
from models.patient_model import PatientModel
from services.patient_service import PatientService
from schemas.patient_schema import PatientSchema
from routes.patient_routes import PatientRoutes
from flasgger import Swagger
from services.nlp_service import NLPService 

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
swagger = Swagger(app)

db_conn_patient= PatientModel()
db_conn_patient.connect_to_database()
nlp_service = NLPService()
patient_service = PatientService(db_conn_patient,nlp_service)
patient_schema = PatientSchema()
patient_routes = PatientRoutes(patient_service, patient_schema)
app.register_blueprint(patient_routes)


if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        
        db_conn_patient.close_connection()
        