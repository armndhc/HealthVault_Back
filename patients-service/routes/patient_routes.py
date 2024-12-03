from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from logger.logger_base import Logger
from flasgger import swag_from

class PatientRoutes(Blueprint):
    def __init__(self, patient_service, patient_schema):
        super().__init__('patient', __name__)
        self.patient_service = patient_service
        self.patient_schema = patient_schema
        self.register_routes()
        self.logger = Logger()

    def register_routes(self):
        self.route('/api/v1/patient', methods=['GET'])(self.get_patient)
        self.route('/api/v1/patient', methods=['POST'])(self.add_patient)
        self.route('/api/v1/patient/<int:patient_id>', methods=['PUT'])(self.update_patient)
        self.route('/api/v1/patient/<int:patient_id>', methods=['DELETE'])(self.delete_patient)
        self.route('/api/v1/patient/query', methods=['POST'])(self.query_patient_nlp)
        self.route('/api/v1/medicalappointments/<int:patient_id>', methods=['GET'])(self.get_completed_appointments)
        self.route('/api/v1/patient/<int:patient_id>', methods=['GET'])(self.get_patient_by_id)
        self.route('/healthcheck', methods=['GET', 'OPTIONS'])(self.healthcheck)


    @swag_from({
    'tags': ['Patient'],
    'parameters': [
        {
            'name': 'patient_id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': 'ID del paciente'
        }
    ],
    'responses': {
        200: {
            'description': 'Patient retrieved successfully',
            'schema': {
                'type': 'object',
                "properties": {
                    "avatar": {"type": "string"},
                    "name": {"type": "string"},
                    "lastName": {"type": "string"},
                    "weight": {"type": "number"},
                    "height": {"type": "number"},
                    "heartrate": {"type": "number"},
                    "bloodPressure": {"type": "string"},
                    "sugarBlood": {"type": "number"},
                    "birthDate": {"type": "string", "format": "date"},
                    "phone": {"type": "string"},
                    "email": {"type": "string", "format": "email"},
                    "bloodType": {"type": "string"},
                    "allergies": {"type": "string"},
                    "gender": {"type": "string"},
                    "familyHistory": {"type": "string"},
                    "medicalHistory": {"type": "string"},
                    "emergencyContact": {"type": "string"},
                    "emergencyPhone": {"type": "string"},
                    "socialSecurity": {"type": "string"}
                }
            }
        },
        404: {'description': 'Patient not found'},
        500: {'description': 'Internal server error'}
    }
    })
    def get_patient_by_id(self, patient_id):
        """
        Get a specific patient by their ID.
        """
        try:
            patient = self.patient_service.get_patient_by_id(patient_id)
            if not patient:
                return jsonify({'error': 'Patient not found'}), 404
            return jsonify(patient), 200
        except Exception as e:
            self.logger.error(f'Error fetching patient by ID: {e}')
            return jsonify({'error': 'Internal server error'}), 500



    @swag_from({
        'tags': ['Patient'],
        'responses': {
            200: {
                'description': 'Get all patients',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        "properties": {
                            "avatar": {"type": "string"},
                            "name": {"type": "string"},
                            "lastName": {"type": "string"},
                            "weight": {"type": "number"},
                            "height": {"type": "number"},
                            "heartrate": {"type": "number"},
                            "bloodPressure": {"type": "string"},
                            "sugarBlood": {"type": "number"},
                            "birthDate": {"type": "string", "format": "date"},
                            "phone": {"type": "string"},
                            "email": {"type": "string", "format": "email"},
                            "bloodType": {"type": "string"},
                            "allergies": {"type": "string"},
                            "gender": {"type": "string"},
                            "familyHistory": {"type": "string"},
                            "medicalHistory": {"type": "string"},
                            "emergencyContact": {"type": "string"},
                            "emergencyPhone": {"type": "string"},
                            "socialSecurity": {"type": "string"}
                        }
                    }
                }
            }
        }
    })

    def get_patient(self):
        try:
            patients = self.patient_service.get_all_patients()
            return jsonify(patients), 200
        except Exception as e:
            self.logger.error(f'Error fetching patients: {e}')
            return jsonify({'error': 'Internal server error'}), 500

    @swag_from({
        'tags': ['Patient'],
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    "properties": {
                        "avatar": {"type": "string"},
                        "name": {"type": "string"},
                        "lastName": {"type": "string"},
                        "weight": {"type": "number"},
                        "height": {"type": "number"},
                        "heartrate": {"type": "number"},
                        "bloodPressure": {"type": "string"},
                        "sugarBlood": {"type": "number"},
                        "birthDate": {"type": "string", "format": "date"},
                        "phone": {"type": "string"},
                        "email": {"type": "string", "format": "email"},
                        "bloodType": {"type": "string"},
                        "allergies": {"type": "string"},
                        "gender": {"type": "string"},
                        "familyHistory": {"type": "string"},
                        "medicalHistory": {"type": "string"},
                        "emergencyContact": {"type": "string"},
                        "emergencyPhone": {"type": "string"},
                        "socialSecurity": {"type": "string"}
                    },
                    'required': ['name', 'lastname', 'weight', 'height', 'heartrate', 'bloodPressure', 'sugarBlood','phone','email']
                }
            }
        ],
        'responses': {
            201: {'description': 'Patient successfully created'},
            400: {'description': 'Invalid data'},
            500: {'description': 'Internal server error'}
        }
    })
    def add_patient(self):
        try:
            request_data = request.json

            if not request_data:
                return jsonify({'error': 'Invalid data'}), 400

            name = request_data.get('name')
            lastName = request_data.get('lastName')
            weight = request_data.get('weight')
            height = request_data.get('height')
            heartrate = request_data.get('heartrate')
            bloodPressure = request_data.get('bloodPressure')
            sugarBlood = request_data.get('sugarBlood')
            birthDate = request_data.get('birthDate')
            phone = request_data.get('phone')
            email = request_data.get('email')
            bloodType = request_data.get('bloodType')
            allergies = request_data.get('allergies')
            gender = request_data.get('gender')
            familyHistory = request_data.get('familyHistory')
            medicalHistory = request_data.get('medicalHistory')
            emergencyContact = request_data.get('emergencyContact')
            emergencyPhone = request_data.get('emergencyPhone')
            socialSecurity = request_data.get('socialSecurity')
            avatar = request_data.get('avatar')


            try:
                self.patient_schema.validate_name(name)
                self.patient_schema.validate_lastName(lastName)
                self.patient_schema.validate_weight(weight)
                self.patient_schema.validate_height(height)
                self.patient_schema.validate_heartrate(heartrate)
                self.patient_schema.validate_bloodPressure(bloodPressure)
                self.patient_schema.validate_sugarBlood(sugarBlood)
                self.patient_schema.validate_birthDate(birthDate)
                self.patient_schema.validate_phone(phone)
                self.patient_schema.validate_email(email)
                self.patient_schema.validate_bloodType(bloodType)
                self.patient_schema.validate_gender(gender)
                self.patient_schema.validate_emergencyContact(emergencyContact)
                self.patient_schema.validate_emergencyPhone(emergencyPhone)
                self.patient_schema.validate_socialSecurity(socialSecurity)


                
            except ValidationError as e:
                return jsonify({'error': e.messages}), 400

            new_patient = {
                'name': name,
                'lastName': lastName,
                'weight': weight,
                'height': height,
                'heartrate': heartrate,
                'bloodPressure': bloodPressure,
                'sugarBlood': sugarBlood,
                'birthDate': birthDate,
                'phone': phone,
                'email': email,
                'bloodType': bloodType,
                'allergies': allergies,
                'gender': gender,
                'familyHistory': familyHistory,
                'medicalHistory': medicalHistory,
                'emergencyContact': emergencyContact,
                'emergencyPhone': emergencyPhone,
                'socialSecurity': socialSecurity,
                'avatar': avatar
            }


            created_patient = self.patient_service.add_patient(new_patient)
            return jsonify(created_patient), 201
        except Exception as e:
            self.logger.error(f'Error adding new patient: {e}')
            return jsonify({'error': 'Internal server error'}), 500

    @swag_from({
        'tags': ['Patient'],
        'parameters': [
            {
                'name': 'patient_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'ID of the patient to update'
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    "properties": {
                        "avatar": {"type": "string"},
                        "name": {"type": "string"},
                        "lastName": {"type": "string"},
                        "weight": {"type": "number"},
                        "height": {"type": "number"},
                        "heartrate": {"type": "number"},
                        "bloodPressure": {"type": "string"},
                        "sugarBlood": {"type": "number"},
                        "birthDate": {"type": "string", "format": "date"},
                        "phone": {"type": "string"},
                        "email": {"type": "string", "format": "email"},
                        "bloodType": {"type": "string"},
                        "allergies": {"type": "string"},
                        "gender": {"type": "string"},
                        "familyHistory": {"type": "string"},
                        "medicalHistory": {"type": "string"},
                        "emergencyContact": {"type": "string"},
                        "emergencyPhone": {"type": "string"},
                        "socialSecurity": {"type": "string"}
                    }
                }
            }
        ],
        'responses': {
            200: {'description': 'Patient successfully updated'},
            400: {'description': 'Invalid data'},
            404: {'description': 'Patient not found'},
            500: {'description': 'Internal server error'}
        }
    })
    def update_patient(self, patient_id):
        try:
            request_data = request.json

            if not request_data:
                return jsonify({'error': 'Invalid data'}), 400

            name = request_data.get('name')
            lastName = request_data.get('lastName')
            weight = request_data.get('weight')
            height = request_data.get('height')
            heartrate = request_data.get('heartrate')
            bloodPressure = request_data.get('bloodPressure')
            sugarBlood = request_data.get('sugarBlood')
            birthDate = request_data.get('birthDate')
            phone = request_data.get('phone')
            email = request_data.get('email')
            bloodType = request_data.get('bloodType')
            allergies = request_data.get('allergies')
            gender = request_data.get('gender')
            familyHistory = request_data.get('familyHistory')
            medicalHistory = request_data.get('medicalHistory')
            emergencyContact = request_data.get('emergencyContact')
            emergencyPhone = request_data.get('emergencyPhone')
            socialSecurity = request_data.get('socialSecurity')
            avatar = request_data.get('avatar')

            try:
                self.patient_schema.validate_name(name)
                self.patient_schema.validate_lastName(lastName)
                self.patient_schema.validate_weight(weight)
                self.patient_schema.validate_height(height)
                self.patient_schema.validate_heartrate(heartrate)
                self.patient_schema.validate_bloodPressure(bloodPressure)
                self.patient_schema.validate_sugarBlood(sugarBlood)
                self.patient_schema.validate_birthDate(birthDate)
                self.patient_schema.validate_phone(phone)
                self.patient_schema.validate_email(email)
                self.patient_schema.validate_bloodType(bloodType)
                self.patient_schema.validate_gender(gender)
                self.patient_schema.validate_emergencyContact(emergencyContact)
                self.patient_schema.validate_emergencyPhone(emergencyPhone)
                self.patient_schema.validate_socialSecurity(socialSecurity)


            except ValidationError as e:
                return jsonify({'error': e.messages}), 400

            update_patient = {
                '_id': patient_id,
                'name': name,
                'lastName': lastName,
                'weight': weight,
                'height': height,
                'heartrate': heartrate,
                'bloodPressure': bloodPressure,
                'sugarBlood': sugarBlood,
                'birthDate': birthDate,
                'phone': phone,
                'email': email,
                'bloodType': bloodType,
                'allergies': allergies,
                'gender': gender,
                'familyHistory': familyHistory,
                'medicalHistory': medicalHistory,
                'emergencyContact': emergencyContact,
                'emergencyPhone': emergencyPhone,
                'socialSecurity': socialSecurity,
                'avatar': avatar
            }

            updated_patient = self.patient_service.update_patient(patient_id,update_patient)

            if not updated_patient:
                return jsonify({'error': 'Patient not found'}), 404

            return jsonify(updated_patient), 200
        except Exception as e:
            self.logger.error(f'Error updating patient: {e}')
            return jsonify({'error': 'Internal server error'}), 500

    @swag_from({
        'tags': ['Patient'],
        'parameters': [
            {
                'name': 'patient_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'ID of the patient to delete'
            }
        ],
        'responses': {
            200: {'description': 'Patient successfully deleted'},
            404: {'description': 'Patient not found'},
            500: {'description': 'Internal server error'}
        }
    })
    def delete_patient(self, patient_id):
        try:
            deleted = self.patient_service.delete_patient(patient_id)
            if not deleted:
                return jsonify({'error': 'Patient not found'}), 404
            return jsonify({'message': 'Patient successfully deleted'}), 200
        except Exception as e:
            self.logger.error(f'Error deleting patient: {e}')
            return jsonify({'error': 'Internal server error'}), 500


    @swag_from({
        'tags': ['Patient'],
        'parameters': [
            {
                'name': 'query',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'query': {'type': 'string'}
                    }
                }
            }
        ],
        'responses': {
            200: {'description': 'Query executed successfully'},
            500: {'description': 'Internal server error'}
        }
    })
    def query_patient_nlp(self):
        try:
            request_data = request.json
            user_query = request_data.get('query', '')

            if not user_query:
                return jsonify({'error': 'Query cannot be empty'}), 400

            result = self.patient_service.query_patients(user_query)
            
            # Validar si hubo un error o no se encontraron resultados
            if 'error' in result:
                return jsonify(result), 400
            elif 'message' in result:
                return jsonify(result), 404

            return jsonify(result), 200

        except Exception as e:
            self.logger.error(f'Error querying patients with NLP: {e}')
            return jsonify({'error': 'Internal server error'}), 500




    @swag_from({
        'tags': ['Medical Appointments'],
        'parameters': [
            {
                'name': 'patient_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'ID del paciente'
            }
        ],
        'responses': {
            200: {
                'description': 'Completed medical appointments for the patient',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'appointment_id': {'type': 'integer'},
                            'date': {'type': 'string', 'format': 'date'},
                            'description': {'type': 'string'},
                            'doctor': {'type': 'string'},
                            'status': {'type': 'string'}
                        }
                    }
                }
            },
            404: {'description': 'No completed appointments found for the patient'},
            500: {'description': 'Internal server error'}
        }
    })
    def get_completed_appointments(self, patient_id):
        try:
            appointments = self.patient_service.get_completed_appointments_by_patient(patient_id)
            if not appointments:
                return jsonify({'error': 'No completed appointments found'}), 404
            return jsonify(appointments), 200
        except Exception as e:
            self.logger.error(f'Error fetching completed appointments: {e}')
            return jsonify({'error': 'Internal server error'}), 500
        
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
