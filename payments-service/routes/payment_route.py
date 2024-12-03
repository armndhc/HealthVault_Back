from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from logger.logger_base import Logger
from flasgger import swag_from

class PaymentRoutes(Blueprint):
    def __init__(self, payment_service, payment_schema):
        super().__init__('payment', __name__)
        self.payment_service = payment_service
        self.payment_schema = payment_schema
        self.register_routes()
        self.logger = Logger()

    def register_routes(self):
        #self.route('/api/v1/payments/prescript', methods=['GET'])(self.get_all_prescription)
        #self.route('/api/v1/payments/medicines', methods=['GET'])(self.get_all_medicines)
        self.route('/api/v1/medications', methods=['GET'])(self.get_all_medications)
        self.route('/api/v1/payments/pending', methods=['GET'])(self.get_all_orders_to_pay)
        self.route('/api/v1/recipe', methods=['GET'])(self.get_all_medicalappointments)
        self.route('/api/v1/payments', methods=['GET'])(self.get_all_payments)
        self.route('/api/v1/payments/add', methods=['POST'])(self.add_payment)
        self.route('/api/v1/payments/<payment_id>', methods=['DELETE'])(self.delete_payment)
        self.route('/healthcheck', methods=['GET', 'OPTIONS'])(self.healthcheck)
   
    """
    @swag_from({
        'tags': ['Medicines'],
        'summary': 'Get all medicines in the database with their quantity and price',
        'responses': {
            200: {
                'description': 'List of all medicines with their details',
                'content': {
                    'application/json': {
                        'example': [
                            {'name': 'Aspirin', 'quantity': 100, 'price': 5.0},
                            {'name': 'Ibuprofen', 'quantity': 50, 'price': 7.2}
                        ]
                    }
                }
            },
            500: {
                'description': 'Server error',
                'content': {
                    'application/json': {
                        'example': {'error': 'Error fetching all medicines from the database'}
                    }
                }
            }
        }
    })
    def get_all_medicines(self):
        try:
            medicines = self.payment_service.get_all_medicines()
            return jsonify(medicines), 200

        except Exception as e:
            return jsonify({'error': f'Error fetching medicines: {e}'}), 500


    @swag_from({
    'tags': ['Payments'],
    'summary': 'Get all prescriptions from the database',
    'responses': {
        200: {
            'description': 'List of all prescriptions',
            'content': {
                'application/json': {
                    'example': [
                        {'_id': 1, 'full name': 'Andreafi iuashid', 'medicines': 'si'}
                    ]
                }
            }
        },
        500: {
            'description': 'Error fetching prescriptions from database',
            'content': {
                'application/json': {
                    'example': {'error': 'Error fetching all prescriptions from the database'}
                }
            }
        }
    }
})
    def get_all_prescription(self):
        prescription = self.payment_service.get_all_prescription()
        return jsonify(prescription), 200



    @swag_from({
    'tags': ['Payments'],
    'summary': 'Get medications for a specific prescription',
    'parameters': [
        {
            'name': 'prescription_id',
            'in': 'path',
            'required': True,
            'schema': {'type': 'integer'},
            'description': 'The ID of the prescription to get medications for'
        }
    ],
    'responses': {
        200: {
            'description': 'Medications for the prescription',
            'content': {
                'application/json': {
                    'example': [
                        {'name': 'Med1', 'quantity': 2, 'price': 10.5},
                        {'name': 'Med2', 'quantity': 1, 'price': 5.0}
                    ]
                }
            }
        },
        404: {
            'description': 'Prescription not found',
            'content': {
                'application/json': {
                    'example': {'error': 'Prescription not found'}
                }
            }
        },
        500: {
            'description': 'Error fetching medications',
            'content': {
                'application/json': {
                    'example': {'error': 'Error fetching medications'}
                }
            }
        }
    }
})
    def get_medications_for_prescription(self, prescription_id):
        medications = self.payment_service.get_medications_for_prescription(prescription_id)
        return jsonify(medications), 200
    """



    

    @swag_from({
        'tags': ['Payments'],
        'summary': 'Get all pending orders to pay',
        'responses': {
            200: {
                'description': 'List of all pending orders',
                'content': {
                    'application/json': {
                        'example': [{'order_id': 1, 'total': 1500}]
                    }
                }
            }
        }
    })
    def get_all_orders_to_pay(self):
        orders = self.payment_service.get_all_orders_to_pay()
        return jsonify(orders), 200

    

    @swag_from({
        'tags': ['Payments'],
        'summary': 'Get all payments',
        'responses': {
            200: {
                'description': 'List of all payments',
                'content': {
                    'application/json': {
                        'example': [{'payment_id': 1, 'amount': 500}]
                    }
                }
            }
        }
    })
    def get_all_payments(self):
        orders = self.payment_service.get_all_payments()
        return jsonify(orders), 200

    @swag_from({
    'responses': {
        200: {
            'description': 'Record successfully created',
            'schema': {
                'type': 'object',
                'properties': {
                    '_id': {'type': 'integer', 'example': 1},
                    'observations': {'type': 'string', 'example': 'string'},
                    'diagnostic': {'type': 'string', 'example': 'string'},
                    'weight': {'type': 'number', 'example': 12},
                    'temperature': {'type': 'number', 'example': 12},
                    'bloodPressure': {'type': 'number', 'example': 12},
                    'patient': {'type': 'string', 'example': 'Carrillo Alejandra'},
                    'doctor': {'type': 'string', 'example': 'Dra Alejandra Carrillo'},
                    'doctor_id': {'type': 'integer', 'example': 2},
                    'patient_id': {'type': 'integer', 'example': 2},
                    'medication': {'type': 'string', 'example': 'paracetamol'},
                    'medication_id': {'type': 'integer', 'example': 2}
                }
            }
        }
    }     
    })
    def get_all_medicalappointments(self):
        medicalappointments = self.payment_service.get_all_medicalappointments()
        return jsonify(medicalappointments), 200

    @swag_from({
    'responses': {
        200: {
            'description': 'Medicine successfully created',
            'schema': {
                'type': 'object',
                'properties': {
                    '_id': {'type': 'integer', 'example': 1},
                    'name': {'type': 'string', 'example': 'Paracetamol'},
                    'unit': {'type': 'string', 'example': 'caja'},
                    'existence': {'type': 'integer', 'example': 4},
                    'price': {'type': 'number', 'format': 'float', 'example': 22.2},
                    'administration': {'type': 'string', 'example': 'Oral'},
                    'distributor': {'type': 'string', 'example': 'MM'}
                }
            }
        }
    }
    })
    def get_all_medications(self):
            medications = self.payment_service.get_all_medications()
            return jsonify(medications), 200


    @swag_from({
        'tags': ['Payments'],
        'summary': 'Add a new payment',
        'parameters': [
    {
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'name': {'type': 'string'},
                'rfc': {'type': 'string'},
                'payment_type': {'type': 'string'},
                'total':{'type': 'integer'},
                #'table': {'type': 'integer'},
                'order_id': {'type': 'integer'},
                'items': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'name': {'type': 'string'},
                            'quantity': {'type': 'integer'},
                            'price': {'type': 'number'}
                        },
                        'required': ['name', 'quantity', 'price']
                    }
                }
            },
            'required': ['name', 'rfc', 'payment_type', 'items']
        }
    }
],

        'responses': {
            201: {
                'description': 'Payment created successfully',
                'content': {
                    'application/json': {
                        'example': {'payment_id': 1, 'total': 650}
                    }
                }
            },
            400: {
                'description': 'Invalid data',
                'content': {
                    'application/json': {
                        'example': {'error': 'Invalid data: name is required'}
                    }
                }
            },
            500: {
                'description': 'Server error',
                'content': {
                    'application/json': {
                        'example': {'error': 'An error occurred: Database unreachable'}
                    }
                }
            }
        }
    })
    def add_payment(self):
        try:
            request_data = request.json
            if not request_data:
                return jsonify({'error': 'Invalid data'}), 400

            name = request_data.get('name')
            rfc = request_data.get('rfc')
            payment_type = request_data.get('payment_type')
            items = request_data.get('items')
            order_id = request_data.get('order_id')
            total = request_data.get('total')

            try:
                self.payment_schema.validate_name(name)
                self.payment_schema.validate_rfc(rfc)
                self.payment_schema.validate_payment_type(payment_type)
                self.payment_schema.validate_items(items)
                self.payment_schema.validate_order_id(order_id)
                self.payment_schema.validate_total(total)
            except ValidationError as e:
                return jsonify({'error': f'Invalid data: {e}'}), 400

            new_payment = {
                'name': name,
                'items': items,
                'rfc': rfc,
                'payment_type': payment_type,
                'order_id': order_id,
                'total': total
            }

            created_payment = self.payment_service.add_payment(new_payment)
            self.logger.info(f'New Payment Created: {created_payment}')
            return jsonify(created_payment), 201

        except Exception as e:
            self.logger.error(f'Error adding a new payment: {e}')
            return jsonify({'error': f'An error occurred: {e}'}), 500

    @swag_from({
        'tags': ['Payments'],
        'summary': 'Delete a payment',
        'parameters': [
            {
                'name': 'payment_id',
                'in': 'path',
                'required': True,
                'schema': {'type': 'integer'},
                'description': 'The ID of the payment to delete'
            }
        ],
        'responses': {
            200: {
                'description': 'Payment deleted successfully',
                'content': {
                    'application/json': {
                        'example': {'message': 'Payment deleted successfully'}
                    }
                }
            },
            404: {
                'description': 'Payment not found',
                'content': {
                    'application/json': {
                        'example': {'error': 'Payment not found'}
                    }
                }
            },
            500: {
                'description': 'Server error',
                'content': {
                    'application/json': {
                        'example': {'error': 'Error deleting the payment'}
                    }
                }
            }
        }
    })
    def delete_payment(self, payment_id):
        try:
            delete_payment = self.payment_service.delete_payment(payment_id)
            if delete_payment:
                return jsonify(delete_payment), 200
            else:
                return jsonify({'error': 'Payment not found'}), 404
        except Exception as e:
            self.logger.error(f'Error deleting the payment data: {e}')
            return jsonify({'error': f'Error deleting the payment data: {e}'}), 500
        
    @swag_from({
        'tags': ['Health'],
        'responses': {
            200: {
                'description': 'Service is up and running',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'status': {'type': 'string'}
                    }
                }
            },
            500: {
                'description': 'Internal server error'
            }
        }
    })
    # Veriifying a healthcheck
    def healthcheck(self):
        return jsonify({ 'status': 'up' }), 200