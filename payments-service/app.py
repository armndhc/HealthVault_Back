from flask import Flask
from flask_cors import CORS
from models.payment_model import PaymentModel
from services.payment_services import PaymentService
from schemas.payment_schemas import PaymentSchema
from routes.payment_route import PaymentRoutes
from flasgger import Swagger

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
swagger = Swagger(app)
db_conn = PaymentModel()
db_conn.connect_to_database()
payment_service = PaymentService(db_conn)
payment_schema = PaymentSchema()
payment_routes = PaymentRoutes(payment_service, payment_schema)
app.register_blueprint(payment_routes)

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        db_conn.close_connection()