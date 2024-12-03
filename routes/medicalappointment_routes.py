from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from logger.logger_base import Logger
from flasgger import swag_from

class MedicalAppointmentRoute(Blueprint):
    def __init__(self, medicalappointment_service, medicalappointment_schema):
        super().__init__('medicalappointment', __name__)
        self.medicalappointment_service = medicalappointment_service
        self.medicalappointment_schema = medicalappointment_schema
        self.register_routes()
        self.logger = Logger()

    # Register the API endpoints with corresponding methods
    def register_routes(self):
        self.route('/api/v1/medicalappointments', methods=['GET'])(self.get_medicalappointments)
        self.route('/api/v1/medicalappointments', methods=['POST'])(self.add_medicalappointment)
        self.route('/api/v1/medicalappointments/<int:medicalappointment_id>', methods = ['PUT'])(self.update_medicalappointment)
        self.route('/api/v1/medicalappointments/<int:medicalappointment_id>', methods = ['DELETE'])(self.delete_medicalappointment)
        self.route('/api/v1/medicalappointments/patients', methods=['GET'])(self.get_patients_list)
        self.route('/api/v1/medicalappointments/doctors', methods=['GET'])(self.get_doctors_list)

    @swag_from({
        'tags': ['MedicalAppointments'],
        'responses': {
            200: {
                'description': 'Get All MedicalAppointments',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'date': {'type': 'string'},
                            'patient': {'type': 'string'},
                            'doctor': {'type': 'string'},
                            'doctor_id': {'type': 'integer'},
                            'patient_id': {'type': 'integer'},
                            'reason': {'type': 'string'},
                            'status': {'type': 'string'},
                        }
                    }
                }
            }
        }
    })
    def get_medicalappointments(self):
    # Fetches all medicalappointments from the medicalappointment service
        medicalappointments = self.medicalappointment_service.get_all_medicalappointments()
        return jsonify(medicalappointments), 200
    
    @swag_from({
        'tags': ['MedicalAppointments'],
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                            'date': {'type': 'string'},
                            'patient': {'type': 'string'},
                            'doctor': {'type': 'string'},
                            'doctor_id': {'type': 'integer'},
                            'patient_id': {'type': 'integer'},
                            'reason': {'type': 'string'},
                            'status': {'type': 'string'},
                    },
                    'required': ['date', 'patient', 'doctor', 'reason', 'status']
                }
            }
        ],
        'responses': {
            201: {
                'description': 'Medical Appointment successfully created'
            },
            400: {
                'description': 'Invalid data'
            },
            500: {
                'description': 'Internal server error'
            }
        }
    })
    def add_medicalappointment(self):
    # Create a new medicalappointment
        try:
            request_data = request.json

            if not request_data:
                return jsonify({'error': 'invalid data'}), 400
            
            date = request_data.get('date')
            patient = request_data.get('patient')
            doctor = request_data.get('doctor')
            patient_id = request_data.get('patient_id')
            doctor_id = request_data.get('doctor_id')
            reason = request_data.get('reason', '')
            status = request_data.get('status')

            try:
                self.medicalappointment_schema.validate_date(date)
                self.medicalappointment_schema.validate_reason(reason)
            except ValidationError as e:
                return jsonify({ 'error': 'Invalid data' }), 400

            new_medicalappointment = {
                'date': date,
                'patient': patient,
                'doctor': doctor,
                'reason': reason,
                'status': status,
                'recipe_id': None,
                'doctor_id': doctor_id,
                'patient_id': patient_id
            }

            created_medicalappointment = self.medicalappointment_service.add_medicalappointment(new_medicalappointment)
            return jsonify(created_medicalappointment), 201
        except Exception as e:
            self.logger.error(f'Error adding new Medical Appointment to the database: {e}')
            return jsonify({ 'error': f'An exception has ocurred: {e}' }), 500
    
    @swag_from({
        'tags': ['MedicalAppointments'],
        'parameters': [
            {
                'name': 'medicalappointment_id',
                'in': 'path',
                'required': True,
                'type': 'string',
                'description': 'ID of the Medical Appointment to update'
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                            'date': {'type': 'string'},
                            'patient': {'type': 'string'},
                            'doctor': {'type': 'string'},
                            'doctor_id': {'type': 'integer'},
                            'patient_id': {'type': 'integer'},
                            'reason': {'type': 'string'},
                            'status': {'type': 'string'},
                    },
                    'required': ['date', 'patient', 'doctor', 'reason', 'status']
                }
            }
        ],
        'responses': {
            200: {
                'description': 'Medical Appointment successfully updated',
                'schema': {
                    'type': 'object',
                    'properties': {
                            'date': {'type': 'string'},
                            'patient': {'type': 'string'},
                            'doctor': {'type': 'string'},
                            'doctor_id': {'type': 'integer'},
                            'patient_id': {'type': 'integer'},
                            'reason': {'type': 'string'},
                            'status': {'type': 'string'},
                            'recipe_id': {'type': 'string'},
                    }
                }
            },
            400: {
                'description': 'Invalid data'
            },
            404: {
                'description': 'Medical Appointment not found'
            },
            500: {
                'description': 'Internal server error'
            }
        }
    })
    def update_medicalappointment(self, medicalappointment_id):
    # Update the medicalappointment data
        try:
            request_data = request.json    
            
            if not request_data:
                return jsonify({'error': 'Invalid data'}), 400
            
            date = request_data.get('date')
            patient = request_data.get('patient')
            doctor = request_data.get('doctor')
            reason = request_data.get('reason')
            doctor_id = request_data.get('doctor_id')
            patient_id = request_data.get('patient_id')
            status = request_data.get('status')    

            try:
                self.medicalappointment_schema.validate_date(date)
                self.medicalappointment_schema.validate_reason(reason)
            except ValidationError as e:
                return jsonify({'error': f'Invalid data {e}'}), 400
            
            update_medicalappointment = {
                '_id': medicalappointment_id,
                'date': date,
                'patient': patient,
                'doctor': doctor,
                'patient_id': patient_id,
                'doctor_id': doctor_id,
                'reason': reason,
                'status': status
            }
            updated_medicalappointment = self.medicalappointment_service.update_medicalappointment(medicalappointment_id, update_medicalappointment)
            if updated_medicalappointment:
                return jsonify(update_medicalappointment), 200
            else:            
                return jsonify({'error': 'Medical Appointment not found'}), 404
        except Exception as e:
            self.logger.error(f'Error updating the Medical Appointment in the database: {e}')
            return jsonify({'error': f'An exception has ocurred: {e}'})
    
    @swag_from({
        'tags': ['MedicalAppointments'],
        'parameters': [
            {
                'name': 'medicalappointment_id',
                'in': 'path',
                'required': True,
                'type': 'string',
                'description': 'ID of the Medical Appointment to delete'
            }
        ],
        'responses': {
            200: {
                'description': 'Medical Appointment successfully deleted'
            },
            404: {
                'description': 'Medical Appointment not found'
            },
            500: {
                'description': 'Internal server error'
            }
        }
    })
    def delete_medicalappointment(self, medicalappointment_id):
    # Delete a medicalappointment
        try:
            delete_medicalappointment = self.medicalappointment_service.delete_medicalappointment(medicalappointment_id)

            if delete_medicalappointment:
                return jsonify(delete_medicalappointment), 200
            else:
                jsonify({'error': 'Medical Appointment not found'}), 404
        except Exception as e:
            self.logger.error(f'Error deleting the Medical Appointment data: {e}')
            jsonify({'error': f'Error deleting the Medical Appointment data: {e}'}), 500
            
    def get_patients_list(self):
        patients = self.medicalappointment_service.get_patients_list()
        return jsonify(patients), 200

    def get_doctors_list(self):
        doctors = self.medicalappointment_service.get_doctors_list()
        return jsonify(doctors), 200


