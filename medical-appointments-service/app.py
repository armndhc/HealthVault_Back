from flask import Flask
from flask_cors import CORS
from models.medicalappointment_model import MedicalAppointmentsModel
from services.medicalappointment_service import MedicalAppointmentService
from schemas.medicalappointment_schema import MedicalAppointmentSchema
from routes.medicalappointment_routes import MedicalAppointmentRoute
from flasgger import Swagger

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
swagger = Swagger(app)
db_conn_medicalappointment = MedicalAppointmentsModel()
db_conn_medicalappointment.connect_to_database()
medicalappointment_service = MedicalAppointmentService(db_conn_medicalappointment)
medicalappointment_schema = MedicalAppointmentSchema()
medicalappointment_routes = MedicalAppointmentRoute(medicalappointment_service, medicalappointment_schema)
app.register_blueprint(medicalappointment_routes)

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        db_conn_medicalappointment.close_connection()