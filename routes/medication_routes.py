from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from logger.logger_base import Logger
from flasgger import swag_from

# Routes for Medication
class MedicationRoutes(Blueprint):
    def __init__(self, medication_service, medication_schema):
        super().__init__('medication', __name__)
        self.medication_service = medication_service
        self.medication_schema = medication_schema
        self.register_routes()
        self.logger = Logger()

    # Routes
    def register_routes(self):
        self.route('/api/v1/medications', methods=['GET', 'OPTIONS'])(self.get_medications)
        self.route('/api/v1/medications', methods=['POST', 'OPTIONS'])(self.add_medications)
        self.route('/api/v1/medications/<int:medication_id>', methods = ['PUT', 'OPTIONS'])(self.update_medication)
        self.route('/api/v1/medications/existence/<int:medication_id>', methods = ['PUT', 'OPTIONS'])(self.update_medication_existence)
        self.route('/api/v1/medications/<int:medication_id>', methods = ['DELETE', 'OPTIONS'])(self.delete_medication)
    
    @swag_from({
        'tags': ['Medications'],
        'responses': {
            200: {
                'description': 'Get All medications',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'name': { 'type': 'string' },
                            'unit': { 'type': 'string' },
                            'existence': { 'type': 'integer' },
                            'price': { 'type': 'number' },
                            'administration': { 'type': 'string' },
                            'distributor': { 'type': 'string' },
                            'image': { 'type': 'string' },
                        }
                    }
                }
            }
        }
    })
    # Getting all the medications.
    def get_medications(self):
        medications = self.medication_service.get_all_medications()
        return jsonify(medications), 200
    
    @swag_from({
        'tags': ['Medications'],
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'name': { 'type': 'string' },
                        'unit': { 'type': 'string' },
                        'existence': { 'type': 'integer' },
                        'price': { 'type': 'number' },
                        'administration': { 'type': 'string' },
                        'distributor': { 'type': 'string' },
                        'image': { 'type': 'string' },
                    },
                    'required': ['name', 'unit', 'existence', 'price', 'administration', 'distributor', 'image']
                }
            }
        ],
        'responses': {
            201: {
                'description': 'Medication successfully created'
            },
            400: {
                'description': 'Invalid data'
            },
            500: {
                'description': 'Internal server error'
            }
        }
    })
    # Adding new medication
    def add_medications(self):
        try:
            request_data = request.json

            if not request_data:
                return jsonify({'error': 'invalid data'}), 400
            
            name = request_data.get('name')
            unit = request_data.get('unit')
            existence = request_data.get('existence')
            price = request_data.get('price')
            administration = request_data.get('administration')
            distributor = request_data.get('distributor')
            image = request_data.get('image')


            try:
                self.medication_schema.validate_name(name)
                self.medication_schema.validate_unit(unit)
                self.medication_schema.validate_existence(existence)
                self.medication_schema.validate_price(price)
                self.medication_schema.validate_administration(administration)
                self.medication_schema.validate_distributor(distributor)
                self.medication_schema.validate_image(image)
            except ValidationError as e:
                return jsonify({ 'error': 'Invalid data' }), 400

            new_medication = {
                'name': name,
                'unit': unit,
                'existence': existence,
                'price': price,
                'administration': administration,
                'distributor': distributor,
                'image': image
            }

            created_medication = self.medication_service.add_medication(new_medication)
            return jsonify(created_medication), 201
        except Exception as e:
            self.logger.error(f'Error adding new medication to the database: {e}')
            return jsonify({ 'error': f'An exception has ocurred: {e}' }), 500
    
    @swag_from({
        'tags': ['Medications'],
        'parameters': [
            {
                'name': 'medication_id',
                'in': 'path',
                'required': True,
                'type': 'string',
                'description': 'ID of the medication to update'
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'name': { 'type': 'string' },
                        'unit': { 'type': 'string' },
                        'existence': { 'type': 'integer' },
                        'price': { 'type': 'number' },
                        'administration': { 'type': 'string' },
                        'distributor': { 'type': 'string' },
                        'image': { 'type': 'string' },
                    },
                    'required': ['name', 'unit', 'existence', 'price', 'administration', 'distributor', 'image']
                }
            }
        ],
        'responses': {
            200: {
                'description': 'Medication successfully updated',
                'schema': {
                    'type': 'object',
                    'properties': {
                        '_id': {'type': 'string'},
                        'name': {'type': 'string'},
                        'unit': {'type': 'string'},
                        'existence': {'type': 'integer'},
                        'price': { 'type': 'number' },
                        'administration': { 'type': 'string' },
                        'distributor': { 'type': 'string' },
                        'image': {'type': 'string'},
                    }
                }
            },
            400: {
                'description': 'Invalid data'
            },
            404: {
                'description': 'Medication not found'
            },
            500: {
                'description': 'Internal server error'
            }
        }
    })
    # Updating an medication
    def update_medication(self, medication_id):
        try:
            request_data = request.json    
            
            if not request_data:
                return jsonify({'error': 'Invalid data'}), 400
            
            name = request_data.get('name')
            unit = request_data.get('unit')
            existence = request_data.get('existence')
            price = request_data.get('price')
            administration = request_data.get('administration')
            distributor = request_data.get('distributor')
            image = request_data.get('image')


            try:
                self.medication_schema.validate_name(name)
                self.medication_schema.validate_unit(unit)
                self.medication_schema.validate_existence(existence)
                self.medication_schema.validate_price(price)
                self.medication_schema.validate_administration(administration)
                self.medication_schema.validate_distributor(distributor)
                self.medication_schema.validate_image(image)
            except ValidationError as e:
                return jsonify({ 'error': 'Invalid data' }), 400
            
            update_medication = {
                'name': name,
                'unit': unit,
                'existence': existence,
                'price': price,
                'administration': administration,
                'distributor': distributor,
                'image': image
            }
            
            updated_medication = self.medication_service.update_medication(medication_id, update_medication)
            if updated_medication:
                return jsonify(update_medication), 200
            else:            
                return jsonify({'error': 'Medication not found'}), 404
        except Exception as e:
            self.logger.error(f'Error updating the medication in the database: {e}')
            return jsonify({'error': f'An exception has ocurred: {e}'})
    
    @swag_from({
        'tags': ['Medications'],
        'parameters': [
            {
                'name': 'medication_id',
                'in': 'path',
                'required': True,
                'type': 'string',
                'description': 'ID of the medication to update its existence'
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'existence': {'type': 'integer'},
                    },
                    'required': ['existence']
                }
            }
        ],
        'responses': {
            200: {
                'description': 'Existence medication successfully updated',
                'schema': {
                    'type': 'object',
                    'properties': {
                        '_id': {'type': 'string'},
                        'name': {'type': 'string'},
                        'unit': {'type': 'string'},
                        'existence': {'type': 'integer'},
                        'price': { 'type': 'number' },
                        'administration': { 'type': 'string' },
                        'distributor': { 'type': 'string' },
                        'image': {'type': 'string'},
                    }
                }
            },
            400: {
                'description': 'Invalid data'
            },
            404: {
                'description': 'Medication not found'
            },
            500: {
                'description': 'Internal server error'
            }
        }
    })
    # Updating the existence for an medication
    def update_medication_existence(self, medication_id):
        try:
            request_data = request.json    
            
            if not request_data:
                return jsonify({'error': 'Invalid data'}), 400
            
            existence = request_data.get('existence')

            try:
                self.medication_schema.validate_existence(existence)
            except ValidationError as e:
                return jsonify({'error': f'Invalid data {e}'}), 400
            
            updated_medication = self.medication_service.update_medication_existence(medication_id, existence)
            if updated_medication:
                return jsonify(updated_medication), 200
            else:            
                return jsonify({'error': 'Medication not found'}), 404
        except Exception as e:
            self.logger.error(f'Error updating the medication in the database: {e}')
            return jsonify({'error': f'An exception has ocurred: {e}'})
    
    @swag_from({
        'tags': ['Medications'],
        'parameters': [
            {
                'name': 'medication_id',
                'in': 'path',
                'required': True,
                'type': 'string',
                'description': 'ID of the medication to delete'
            }
        ],
        'responses': {
            200: {
                'description': 'Medication successfully deleted'
            },
            404: {
                'description': 'Medication not found'
            },
            500: {
                'description': 'Internal server error'
            }
        }
    })
    # Deleting an medication
    def delete_medication(self, medication_id):
        try:
            delete_medication = self.medication_service.delete_medication(medication_id)

            if delete_medication:
                return jsonify(delete_medication), 200
            else:
                jsonify({'error': 'Medication not found'}), 404
        except Exception as e:
            self.logger.error(f'Error deleting the medication data: {e}')
            jsonify({'error': f'Error deleting the medication data: {e}'}), 500
