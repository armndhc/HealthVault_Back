from flask import jsonify
from logger.logger_base import Logger

class PatientService:
    def __init__(self, db_conn,nlp_service):
        self.logger = Logger()
        self.db_conn = db_conn
        self.nlp_service = nlp_service

    def get_all_patients(self):
        try:
            patients = list(self.db_conn.db.patient.find())
            return patients
        except Exception as e:
            self.logger.error(f'Error fetching patients from the database: {e}')
            return jsonify({ 'error': f'Error fetching patients from the database: {e}' }), 500
        
    def add_patient(self, new_patient):
        try:
            last_patient = self.db_conn.db.patient.find_one(sort=[('_id', -1)])
            next_id = (last_patient['_id'] + 1 if last_patient else 1)
            new_patient["_id"] = next_id
            self.db_conn.db.patient.insert_one(new_patient)
            return new_patient
        except Exception as e:
            return jsonify({'error': f'Error creating the new patient: {e}'}), 500
        
    def get_patient_by_id(self, patient_id):
        try:
            patient = self.db_conn.db.patient.find_one({'_id': patient_id})
            return patient
        except Exception as e:
            self.logger.error(f'Error fetching the patient id from the database: {e}')
            return jsonify({'error': f'Error fetching the patient id from the database: {e}'}), 500
        
    def update_patient(self, patient_id, patient):
        try:
            update_patient = self.get_patient_by_id(patient_id)

            if update_patient:
                updated_patient = self.db_conn.db.patient.update_one({'_id': patient_id}, {'$set': patient})
                if updated_patient.modified_count > 0:
                    return patient
                else:
                    return 'The patient is already up-to-date'
            else:
                return None
        except Exception as e:
            self.logger.error(f'Error updating the patient: {e}')
            return jsonify({'error': f'Error updating the patient: {e}'}), 500
        
    
    def delete_patient(self, patient_id):
        try:
            deleted_patient = self.get_patient_by_id(patient_id)

            if deleted_patient:
                self.db_conn.db.patient.delete_one({'_id': patient_id})            
                return deleted_patient
            else:
                return None            
        except Exception as e:
            self.logger.error(f'Error deleting the patient data: {e}')
            return jsonify({'error': f'Error deleting the patient: {e}'}), 500

    def query_patients(self, user_query):
        try:
            parsed_query = self.nlp_service.parse_query(user_query)

            if not parsed_query:
                self.logger.info(f"No valid query filters generated from user query: {user_query}")
                return {'error': 'No valid filters found for the query. Please refine your input.'}, 400

            results = list(self.db_conn.db.patient.find(parsed_query))
            
            if not results:
                return {'message': 'No patients found matching the query.'}, 404

            return {'results': results}, 200

        except Exception as e:
            self.logger.error(f'Error querying patients: {e}')
            return {'error': f'Internal server error: {e}'}, 500






    def get_completed_appointments_by_patient(self, patient_id):
        try:
            # Convert patient_id to the appropriate type if necessary
            if isinstance(patient_id, str) and patient_id.isnumeric():
                patient_id = int(patient_id)

            # Find completed appointments
            appointments = list(self.db_conn.db.medicalappointments.find({
                "patient_id": patient_id,
                "status": "Completed"
            }))

            if not appointments:
                return []

            # Get all unique doctor IDs from the appointments
            doctor_ids = {appointment["doctor_id"] for appointment in appointments}

            # Fetch doctor details
            doctors = list(self.db_conn.db.doctors.find({"_id": {"$in": list(doctor_ids)}}))
            doctor_map = {doctor["_id"]: f"{doctor['first_name']} {doctor['last_name']}" for doctor in doctors}

            # Map doctor names to appointments
            for appointment in appointments:
                doctor_id = appointment["doctor_id"]
                appointment["doctor_name"] = doctor_map.get(doctor_id, "Unknown Doctor")

            return appointments

        except Exception as e:
            self.logger.error(f'Error fetching completed appointments: {e}')
            raise Exception(f'Error fetching completed appointments: {e}')