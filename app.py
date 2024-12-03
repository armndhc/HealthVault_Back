from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from routes.doctor_routes import DoctorRoutes
from services.doctor_service import DoctorService
from schemas.doctor_schema import DoctorSchema
from models.doctor_model import DoctorModel

# Crear la aplicación Flask
app = Flask(__name__)
CORS(app)
swagger = Swagger(app)

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
        db_conn_doctor.close_connection()