from flask import Flask
from flask_cors import CORS
from models.medication_model import MedicationModel
from services.medication_service import MedicationService
from schemas.medication_schema import MedicationSchema
from routes.medication_routes import MedicationRoutes
from flasgger import Swagger

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
swagger = Swagger(app)
db_conn_medication = MedicationModel()
db_conn_medication.connect_to_database()
medication_service = MedicationService(db_conn_medication)
medication_schema = MedicationSchema()
medication_routes = MedicationRoutes(medication_service, medication_schema)
app.register_blueprint(medication_routes)

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        db_conn_medication.close_connection()