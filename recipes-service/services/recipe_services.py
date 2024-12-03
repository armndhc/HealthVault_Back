from flask import jsonify
from logger.logger_base import Logger

class RecipeService:
    def __init__(self, db_conn):
        self.logger = Logger()
        self.db_conn = db_conn

    def get_all_recipes(self):
        try:
            recipes = list(self.db_conn.db.recipe.find())
            return recipes
        except Exception as e:
            self.logger.error(f'Error fetching all recipes from the database: {e}')
            return jsonify({ 'error': f'Error fetching all recipes from the database: {e}' }), 500
        
    def add_recipe(self, new_recipe):
        try:
            last_recipe = self.db_conn.db.recipe.find_one(sort=[('_id', -1)])
            next_id = (last_recipe['_id'] + 1 if last_recipe else 1)
            new_recipe["_id"] = next_id
            self.db_conn.db.recipe.insert_one(new_recipe)
            return new_recipe
        except Exception as e:
            self.logger.error(f'Error creating the new recipe: {e}')
            return jsonify({ 'error': f'Error creating the new recipe: {e}' }), 500
    
    def get_appointment(self,appointment_id):
        try:
            appointment = self.db_conn.db.medicalappointments.find_one({"_id": appointment_id})
            self.logger.info(appointment)
            if appointment:
                result = {
                    "appointment_id" : appointment["_id"],
                    "patient_id" : appointment["patient_id"],
                    "patient": appointment["patient"],
                    "doctor_id" : appointment["doctor_id"],
                    "doctor": appointment["doctor"],
                }
                return result
            else:
                self.logger.error(f'Error fetching all appointment data from the database: {e}')
                return jsonify({ 'error': f'Error fetching appointment from the database: {e}' }), 500   
        except Exception as e:
            self.logger.error(f'Error fetching patients from the database: {e}')
            return jsonify({ 'error': f'Error fetching patients from the database: {e}' }), 500

    def get_medications_list(self):
        try:
            medications = list(self.db_conn.db.medications.find())
            medications_list = []
            for m in medications:
                medications_list.append({
                    "name": m["name"] + " " + m["unit"] + " " + m["distributor"],
                    "_id" : m["_id"]
                })  
            return medications_list
        except Exception as e:
            self.logger.error(f'Error fetching medications from the database: {e}')
            return jsonify({ 'error': f'Error fetching medications from the database: {e}' }), 500
