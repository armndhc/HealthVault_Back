from flask import jsonify
from logger.logger_base import Logger

class PaymentService:
    def __init__(self, db_conn):
        self.logger = Logger()
        self.db_conn = db_conn
    """
    def get_all_prescription(self):
        try:
            # Obtener todas las prescripciones
            prescriptions = list(self.db_conn.db.prescription.find())

            # Procesar las prescripciones para obtener solo la información requerida
            result = []
            for prescription in prescriptions:
                # Obtener el id, si existe
                prescription_id = str(prescription.get('_id'))  # Convertir a string para facilidad en el front

                # Obtener el nombre y RFC
                name = prescription.get('name', '')
                rfc = prescription.get('rfc', '')

                # Verificar si tiene medicamentos
                has_medicines = 'si' if prescription.get('medicines') == 'si' else 'no'

                # Crear un diccionario con la información deseada
                result.append({
                    'id': prescription_id,  # Añadir el ID de la prescripción
                    'name': name,
                    'rfc': rfc,
                    'medicines': has_medicines
                })
            
            # Retornar la lista de prescripciones con la nueva estructura
            return result

        except Exception as e:
            self.logger.error(f'Error fetching all prescriptions from the database: {e}')
            return jsonify({'error': f'Error fetching all prescriptions from the database: {e}'}), 500

    

    def get_all_medicines(self):
        try:
            # Obtener todos los medicamentos de la base de datos 'medicinesdb'
            medicines = list(self.db_conn.db.medicines.find())
            
            # Verificar si hay medicamentos disponibles
            if medicines:
                medicines_details = []
                for medicine in medicines:
                    name = medicine.get('name', '')
                    quantity = medicine.get('quantity', 0)
                    price = medicine.get('price', 0.0)
                    
                    # Crear un diccionario con la información de cada medicamento
                    medicines_details.append({
                        'name': name,
                        'quantity': quantity,
                        'price': price
                    })
                
                return medicines_details
            else:
                return jsonify({'error': 'No medicines found in the database'}), 404

        except Exception as e:
            self.logger.error(f'Error fetching all medicines from the database: {e}')
            return jsonify({'error': f'Error fetching all medicines: {e}'}), 500
    """

    def get_all_orders_to_pay(self):
        try:
            orders = list(self.db_conn.db.orders.find({"status": "done"}))
            for order in orders:
                total = 0
                for item in order["items"]:
                    total += item["price"] * item["quantity"]
                order["total"] = total
            return orders
        except Exception as e:
            self.logger.error(f'Error fetching all orders to pay from the database: {e}')
            return jsonify({'error': f'Error fetching all orders to pay from the database: {e}'}), 500

    def get_all_payments(self):
        try:
            payments = list(self.db_conn.db.payments.find({"active": True}))
            return payments
        except Exception as e:
            self.logger.error(f'Error fetching all payments from the database: {e}')
            return jsonify({'error': f'Error fetching all payments from the database: {e}'}), 500

    def get_all_medicalappointments(self):
        try:
            medicalappointments = list(self.db_conn.db.recipe.find())
            return medicalappointments
        except Exception as e:
            self.logger.error(f'Error fetching all medical appointments from the database: {e}')
            return jsonify({'error': f'Error fetching all medical appointments from the database: {e}'}), 500

    def get_all_medications(self):
        try:
            medications = list(self.db_conn.db.medications.find())
            return medications
        except Exception as e:
            self.logger.error(f'Error fetching all medical medications from the database: {e}')
            return jsonify({'error': f'Error fetching all medical medications from the database: {e}'}), 500

    def add_payment(self, new_payment):
        try:
            self.logger.info("INICIO")
            self.logger.info(new_payment["order_id"])
            self.logger.info("INICIO 2")
            last_book = self.db_conn.db.payments.find_one(sort=[('_id', -1)])
            next_id = (last_book['_id'] + 1 if last_book else 1)
            new_payment['_id'] = next_id
            new_payment['active'] = True
            self.db_conn.db.payments.insert_one(new_payment)
            self.db_conn.db.orders.delete_one({'_id': new_payment['order_id']})    
            return new_payment
        except Exception as e:
            self.logger.error(f'Error creating the new payment: {e}')
            return jsonify({'error': f'Error creating the new payment: {e}'}), 500

    def get_payment_by_id(self, payment_id):
        try:
            payment_id =int(payment_id)
            self.logger.info(type(payment_id))
            payment = self.db_conn.db.payments.find_one({'_id': payment_id})
            self.logger.info(payment)
            return payment
        except Exception as e:
            self.logger.error(f'Error fetching the payment by id from the database: {e}')
            return jsonify({'error': f'Error fetching the payment by id from the database: {e}'}), 500

    def delete_payment(self, payment_id):
        try:
            payment_id = int(payment_id)
            existing_payment = self.get_payment_by_id(payment_id)

            if existing_payment:
                if existing_payment["active"]:
                    result = self.db_conn.db.payments.update_one({'_id': payment_id}, {'$set': {"active": False}})    #Libro actualizado
                    if result.modified_count > 0: #Verifica si hay documentos actualizados
                            existing_payment["active"] = False
                            return existing_payment
                    else:
                        return None
                else:
                    return None
            else:
                return None
        except Exception as e:
            self.logger.error(f'Error deleting the payment: {e}')
            return jsonify({'error': f'Error deleting the payment: {e}'}), 500


if __name__ == '_main_':
    from models.payment_model import PaymentModel

    logger = Logger()
    db_conn = PaymentModel()
    payment_service = PaymentService(db_conn)

    try:
        db_conn.connect_to_database()
        
        # Obtener todos los pagos
        prescription = payment_service.get_all_prescription()
        payments = payment_service.get_all_payments()
        logger.info(f'Payments fetched: {payments}')

        # Añadir un nuevo pago
        new_payment = payment_service.add_payment({
            'name': 'Payment1',
            'user_id': 1,
            'items': [
                {'dish': 'Burger', 'price': 10.99, 'quantity': 2},
                {'dish': 'Fries', 'price': 3.50, 'quantity': 1}
            ]
        })
        logger.info(f'New payment added: {new_payment}')

        # Obtener un pago por ID
        payment = payment_service.get_payment_by_id(new_payment['_id'])
        logger.info(f'Payment fetched by ID: {payment}')

    except Exception as e:
        logger.error(f'An error has occurred: {e}')
    finally:
        db_conn.close_connection()
        logger.info('Connection to database was successfully closed.')