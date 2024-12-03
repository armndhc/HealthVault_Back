from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from logger.logger_base import Logger
from flasgger import swag_from


class DoctorRoutes(Blueprint):
    def __init__(self, doctor_service, doctor_schema):
        super().__init__('doctor', __name__)
        self.doctor_service = doctor_service
        self.doctor_schema = doctor_schema
        self.register_routes()
        self.logger = Logger()

    def register_routes(self):
        self.route('/api/v1/doctors', methods=['GET'])(self.get_doctors)
        self.route('/api/v1/doctors', methods=['POST'])(self.add_doctor)
        self.route('/api/v1/doctors/<int:doctor_id>', methods=['PUT'])(self.update_doctor)
        self.route('/api/v1/doctors/<int:doctor_id>', methods=['DELETE'])(self.delete_doctor)

    @swag_from({
        'tags': ['Doctors'],
        'summary': 'Retrieve all doctors',
        'description': 'Fetch a list of all doctors in the system.',
        'responses': {
            200: {
                'description': 'A list of doctors',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            '_id': {'type': 'integer', 'example': 1},
                            'name': {'type': 'string', 'example': 'Dr. John Doe'},
                            'specialty': {'type': 'string', 'example': 'Cardiology'},
                            'location': {'type': 'string', 'example': 'New York'},
                        }
                    }
                }
            }
        }
    })
    def get_doctors(self):
        doctors = self.doctor_service.get_all_doctors()
        return jsonify(doctors), 200

    @swag_from({
        'tags': ['Doctors'],
        'summary': 'Create a new doctor',
        'description': 'Add a new doctor with a name, specialty, and location.',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string', 'example': 'Dr. John Doe'},
                        'license': {'type': 'string', 'example': '1234567890'},
                        'date_of_birth': {'type': 'string', 'example': '1980-05-15'},
                        'phone_number': {'type': 'string', 'example': '1234567890'},
                        'email': {'type': 'string', 'example': 'johndoe@example.com'},
                        'specialties': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'specialty': {'type': 'string', 'example': 'Cardiology'},
                                    'consultation_fee': {'type': 'number', 'example': 150},
                                    'services': {'type': 'array', 'items': {'type': 'string'}}
                                }
                            },
                            'example': [
                                {"specialty": "Cardiology", "consultation_fee": 150, "services": ["Electrocardiogram (ECG)", "Stress Test"]},
                                {"specialty": "Pediatrics", "consultation_fee": 120, "services": ["Vaccinations", "Growth Monitoring"]}
                            ]
                        }
                    },
                    'required': ['name', 'license', 'date_of_birth', 'phone_number', 'email', 'specialties']
                }
            }
        ],
        'responses': {
            201: {'description': 'Doctor successfully created'},
            400: {'description': 'Invalid data'},
            500: {'description': 'Internal server error'}
        }
    })
    def add_doctor(self):
        try:
            request_data = request.json
            if not request_data:
                return jsonify({'error': 'Invalid data'}), 400

            # Obtener todos los atributos del doctor
            name = request_data.get('name')
            license = request_data.get('license')
            date_of_birth = request_data.get('date_of_birth')
            phone_number = request_data.get('phone_number')
            email = request_data.get('email')
            specialties = request_data.get('specialties')  # Lista de especialidades

            # Validar campos individuales usando métodos del esquema
            try:
                self.doctor_schema.validate_name(name)
                self.doctor_schema.validate_license(license)
                self.doctor_schema.validate_date_of_birth(date_of_birth)
                self.doctor_schema.validate_phone_number(phone_number)
                self.doctor_schema.validate_email(email)
                self.doctor_schema.validate_specialties(specialties)
    
            except ValidationError as e:
                return jsonify({'error': f'Invalid data: {e}'}), 400

            # Crear un nuevo doctor con la lista completa de especialidades
            new_doctor = {
                'name': name,
                'license': license,
                'date_of_birth': date_of_birth,
                'phone_number': phone_number,
                'email': email,
                'specialties': specialties,  # Asignando la lista completa de especialidades
            }

            created_doctor = self.doctor_service.add_doctor(new_doctor)
            self.logger.info(f'New Doctor Created: {created_doctor}')
            return jsonify(created_doctor), 201
        except Exception as e:
            self.logger.error(f'Error adding new doctor to the database: {e}')
            return jsonify({'error': f'An exception has occurred: {e}'}), 500

    @swag_from({
        'tags': ['Doctors'],
        'summary': 'Update an existing doctor',
        'description': 'Modify the name, phone number, email, and license of a doctor by their ID.',
        'parameters': [
            {
                'name': 'doctor_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'example': 1,
                'description': 'The ID of the doctor to update'
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string', 'example': 'Dr. John Doe'},
                        'phone_number': {'type': 'string', 'example': '1234567890'},
                        'email': {'type': 'string', 'example': 'johndoe@example.com'},
                        'license': {'type': 'string', 'example': '1234567890'}
                    },
                    'required': ['name', 'phone_number', 'email', 'license']
                }
            }
        ],
        'responses': {
            200: {'description': 'Doctor successfully updated'},
            400: {'description': 'Invalid data'},
            404: {'description': 'Doctor not found'},
            500: {'description': 'Internal server error'}
        }
    })
    def update_doctor(self, doctor_id):
        try:
            # Get the data to update
            request_data = request.json
            if not request_data:
                return jsonify({'error': 'Invalid data'}), 400

            # Extract the updated fields
            name = request_data.get('name')
            phone_number = request_data.get('phone_number')
            email = request_data.get('email')
            license = request_data.get('license')

            # Validate fields using the schema
            try:
                self.doctor_schema.validate_name(name)
                self.doctor_schema.validate_phone_number(phone_number)
                self.doctor_schema.validate_email(email)
                self.doctor_schema.validate_license(license)
            except ValidationError as e:
                return jsonify({'error': f'Invalid data: {e}'}), 400

            # Prepare the updated doctor data
            updated_doctor = {
                '_id': doctor_id,
                'name': name,
                'phone_number': phone_number,
                'email': email,
                'license': license
            }

            # Call the service to update the doctor in the database
            # Assuming the update service returns the updated document or None if not found
            update_result = self.doctor_service.update_doctor(doctor_id, updated_doctor)

            if update_result:
                # If the update was successful, return the updated doctor
                return jsonify(update_result), 200
            else:
                return jsonify({'error': 'Doctor not found'}), 404
        except Exception as e:
            self.logger.error(f'Error updating the doctor in the database: {e}')
            return jsonify({'error': f'An exception has occurred: {e}'}), 500
    @swag_from({
        'tags': ['Doctors'],
        'summary': 'Delete a doctor',
        'description': 'Remove a doctor by their ID.',
        'parameters': [
            {
                'name': 'doctor_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'example': 1,
                'description': 'The ID of the doctor to delete'
            }
        ],
        'responses': {
            200: {'description': 'Doctor successfully deleted'},
            404: {'description': 'Doctor not found'},
            500: {'description': 'Internal server error'}
        }
    })
    def delete_doctor(self, doctor_id):
        try:
            deleted_doctor = self.doctor_service.delete_doctor(doctor_id)
            if deleted_doctor:
                return jsonify(deleted_doctor), 200
            else:
                return jsonify({'error': 'Doctor not found'}), 404
        except Exception as e:
            self.logger.error(f'Error deleting the doctor data: {e}')
            return jsonify({'error': f'Error deleting the doctor data: {e}'}), 500
