from flask import jsonify
from logger.logger_base import Logger

# Service for managing medication
class MedicationService:
    def __init__(self, db_conn):
        self.logger = Logger()
        self.db_conn = db_conn

    # Getting all the medications
    def get_all_medications(self):
        try:
            # Reading
            medications = list(self.db_conn.db.medications.find())
            return medications
        except Exception as e:
            self.logger.error(f'Error fetching all medications from the database: {e}')
            return jsonify({ 'error': f'Error fetching all medications from the database: {e}' }), 500
    
    # Adding an medication
    def add_medication(self, new_medication):
        try:
            # Calculating next id
            last_medication = self.db_conn.db.medications.find_one(sort=[('_id', -1)])
            next_id = (last_medication['_id'] + 1 if last_medication else 1)
            new_medication["_id"] = next_id
            # Adding
            self.db_conn.db.medications.insert_one(new_medication)
            return new_medication
        except Exception as e:
            self.logger.error(f'Error creating the new medication: {e}')
            return jsonify({ 'error': f'Error creating the new medication: {e}' }), 500
        
    # Getting an medication by id
    def get_medication_by_id(self, medication_id):
        try:
            medication = self.db_conn.db.medications.find_one({'_id': medication_id})
            return medication
        except Exception as e:
            self.logger.error(f'Error fetching the medication id from the database: {e}')
            return jsonify({'error': f'Error fetching the medication id from the database: {e}'}), 500
        
    # Updating an medication
    def update_medication(self, medication_id, medication):
        try:
            update_medication = self.get_medication_by_id(medication_id)

            if update_medication:
                updated_medication = self.db_conn.db.medications.update_one({'_id': medication_id}, {'$set': medication})
                if updated_medication.modified_count > 0:
                    return medication
                else:
                    return 'The medication is already up-to-date'
            else:
                return None
        except Exception as e:
            self.logger.error(f'Error updating the medication: {e}')
            return jsonify({'error': f'Error updating the medication: {e}'}), 500
        
    def update_medication_existence(self, medication_id, existence):
        try:
            update_medication = self.get_medication_by_id(medication_id)

            # Just update the existence for medication
            if update_medication:
                updated_medication = self.db_conn.db.medications.update_one({'_id': medication_id}, {'$set': {'existence': existence}})
                if updated_medication.modified_count > 0:
                    update_medication["existence"] = existence
                    return update_medication
                else:
                    return 'The medication existence is already up-to-date'
            else:
                return None
        except Exception as e:
            self.logger.error(f'Error updating the medication existence: {e}')
            return jsonify({'error': f'Error updating the medication existence: {e}'}), 500
    
    # Deleting medication
    def delete_medication(self, medication_id):
        try:
            deleted_medication = self.get_medication_by_id(medication_id)

            if deleted_medication:
                self.db_conn.db.medications.delete_one({'_id': medication_id})            
                return deleted_medication
            else:
                return None            
        except Exception as e:
            self.logger.error(f'Error deleting the medication data: {e}')
            return jsonify({'error': f'Error deleting the medication: {e}'}), 500
