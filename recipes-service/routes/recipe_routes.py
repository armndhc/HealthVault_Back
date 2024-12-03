from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from logger.logger_base import Logger
from flasgger import swag_from

class RecipeRoutes(Blueprint):
    def __init__(self, recipe_service, recipe_schema):
        super().__init__('recipe', __name__)
        self.recipe_service = recipe_service
        self.recipe_schema = recipe_schema
        self.register_routes()
        self.logger = Logger()

    def register_routes(self):
        self.route('/recipe-api/v1/recipe', methods=['GET'])(self.get_recipes)
        self.route('/recipe-api/v1/recipe', methods=['POST'])(self.add_recipes)
        self.route('/recipe-api/v1/recipe/<int:appointment_id>',methods=['GET'])(self.get_appointment)
        self.route('/recipe-api/v1/recipe/medications', methods=['GET'])(self.get_medications_list)
        self.route('/healthcheck', methods=['GET', 'OPTIONS'])(self.healthcheck)

    @swag_from({
        'tags': ['recipes'],
        'responses': {
            200: {
                'description': 'Get all the recipes from database',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'observations': { 'type': 'string' },
                            'diagnostic': { 'type': 'string' },
                            'weight': { 'type': 'integer' },
                            'temperature': { 'type': 'integer' },
                            'bloodPressure': { 'type': 'string' },
                        }
                    }
                }
            }
        }
    })

    def get_recipes(self):
        recipes = self.recipe_service.get_all_recipes()
        return jsonify(recipes), 200
    
    @swag_from({
        'tags': ['Recipes'],
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                            'observations': { 'type': 'string' },
                            'diagnostic': { 'type': 'string' },
                            'weight': { 'type': 'integer' },
                            'temperature': { 'type': 'integer' },
                            'bloodPressure': { 'type': 'string' },
                            'bloodPressure': { 'type': 'integer' },
                    },
                    'required': ['observations', 'diagnostic','weight','temperature','bloodPressure' ]
                }
            }
        ],
        'responses': {
            201: {
                'description': 'Recipe succesfully added'
            },
            400: {
                'description': 'Invalid data'
            },
            500: {
                'description': 'Internal server error'
            }
        }
    })

    def add_recipes(self):
        try:
            request_data = request.json

            if not request_data:
                return jsonify({'error': 'invalid data'}), 400
            patient = request_data.get('patient')
            doctor = request_data.get('doctor')
            observations = request_data.get('observations')
            diagnostic = request_data.get('diagnostic')
            weight = request_data.get('weight')
            temperature = request_data.get('temperature')
            bloodPressure = request_data.get('bloodPressure')
            medication = request_data.get('medication')
            quantity = request_data.get('quantity')

            try:
                self.recipe_schema.validate_observations(observations)
                self.recipe_schema.validate_diagnostic(diagnostic)
                self.recipe_schema.validate_weight(weight)
                self.recipe_schema.validate_temperature(temperature)
                self.recipe_schema.validate_bloodPressure(bloodPressure)
            except ValidationError as e:
                return jsonify({ 'error': 'Invalid data' }), 400

            new_recipe = {
                'patient': patient,
                'doctor': doctor,
                'observations': observations,
                'diagnostic': diagnostic,
                'weight':weight,
                'temperature': temperature,
                'bloodPressure': bloodPressure,
                'medication': medication,
                'quantity': quantity

            }

            created_recipe = self.recipe_service.add_recipe(new_recipe)
            return jsonify(created_recipe), 201
        except Exception as e:
            self.logger.error(f'Error adding new recipe to the database: {e}')
            return jsonify({ 'error': f'An exception has ocurred: {e}' }), 500
        
    def get_appointment(self,appointment_id):
        self.logger.info(appointment_id)
        appointment = self.recipe_service.get_appointment(appointment_id)
        return jsonify(appointment), 200
    
    def get_medications_list(self):
        medications = self.recipe_service.get_medications_list()
        return jsonify(medications), 200
    
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
