from flask import jsonify
from logger.logger_base import Logger

class MedicalAppointmentService:
    def __init__(self, db_conn):
        self.logger = Logger()
        self.db_conn = db_conn

    # Get all servervations
    def get_all_medicalappointments(self):
        try:
            medicalappointments = list(self.db_conn.db.medicalappointments.find())
            return medicalappointments
        except Exception as e:
            self.logger.error(f'Error fetching all medicalappointments from the database: {e}')
            return jsonify({ 'error': f'Error fetching all medicalappointments from the database: {e}' }), 500
    
    # New medicalappointment
    def add_medicalappointment(self, new_medicalappointment):
        try:
            last_medicalappointment = self.db_conn.db.medicalappointments.find_one(sort=[('_id', -1)])
            next_id = (last_medicalappointment['_id'] + 1 if last_medicalappointment else 1)
            new_medicalappointment["_id"] = next_id
            self.db_conn.db.medicalappointments.insert_one(new_medicalappointment)
            return new_medicalappointment
        except Exception as e:
            self.logger.error(f'Error creating the new medicalappointment: {e}')
            return jsonify({ 'error': f'Error creating the new medicalappointment: {e}' }), 500
        
    # Get medicalappointment by id
    def get_medicalappointment_by_id(self, medicalappointment_id):
        try:
            medicalappointment = self.db_conn.db.medicalappointments.find_one({'_id': medicalappointment_id})
            return medicalappointment
        except Exception as e:
            self.logger.error(f'Error fetching the medicalappointment id from the database: {e}')
            return jsonify({'error': f'Error fetching the medicalappointment id from the database: {e}'}), 500
        
    # Update a medicalappointment by id
    def update_medicalappointment(self, medicalappointment_id, medicalappointment):
        try:
            update_medicalappointment = self.get_medicalappointment_by_id(medicalappointment_id)

            if update_medicalappointment:
                updated_medicalappointment = self.db_conn.db.medicalappointments.update_one({'_id': medicalappointment_id}, {'$set': medicalappointment})
                if updated_medicalappointment.modified_count > 0:
                    return medicalappointment
                else:
                    return 'The medicalappointment is already up-to-date'
            else:
                return None
        except Exception as e:
            self.logger.error(f'Error updating the medicalappointment: {e}')
            return jsonify({'error': f'Error updating the medicalappointment: {e}'}), 500
        
    # Delete a medicalappointment by id
    def delete_medicalappointment(self, medicalappointment_id):
        try:
            deleted_medicalappointment = self.get_medicalappointment_by_id(medicalappointment_id)

            if deleted_medicalappointment:
                self.db_conn.db.medicalappointments.delete_one({'_id': medicalappointment_id})            
                return deleted_medicalappointment
            else:
                return None            
        except Exception as e:
            self.logger.error(f'Error deleting the medicalappointment data: {e}')
            return jsonify({'error': f'Error deleting the medicalappointment: {e}'}), 500


    def get_patients_list(self):
        try:
            patients = list(self.db_conn.db.patient.find())
            patients_list=[]
            for p in patients:
                patients_list.append({
                    "name": p["name"] + " " + p["lastName"],
                    "_id": p["_id"]
                })
            return patients_list
        except Exception as e:
            self.logger.error(f'Error fetching all patients list from the database: {e}')
            return jsonify({ 'error': f'Error fetching all patients list from the database: {e}' }), 500
    
    def get_doctors_list(self):
        try:
            doctors = list(self.db_conn.db.doctors.find())
            doctors_list=[]
            for d in doctors:
                doctors_list.append({
                    "name": d["name"],
                    "_id": d["_id"]
                })
            return doctors_list
        except Exception as e:
            self.logger.error(f'Error fetching all doctors list from the database: {e}')
            return jsonify({ 'error': f'Error fetching all doctors list from the database: {e}' }), 500

