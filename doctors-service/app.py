from flask import Flask
from flask_cors import CORS
from routes.doctor_routes import DoctorRoutes
from services.doctor_service import DoctorService
from schemas.doctor_schema import DoctorSchema
from models.doctor_model import DoctorModel
from flasgger import Swagger

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
swagger = Swagger(app)
db_conn_doctor = DoctorModel()
db_conn_doctor.connect_to_database()
doctor_service = DoctorService(db_conn_doctor)
doctor_schema = DoctorSchema()

doctor_routes = DoctorRoutes(doctor_service, doctor_schema)
app.register_blueprint(doctor_routes)

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        db_conn_doctor.close_connection()
