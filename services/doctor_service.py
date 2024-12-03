from flask import jsonify
from logger.logger_base import Logger

class DoctorService:
    def __init__(self, db_conn):
        self.logger = Logger()
        self.db_conn = db_conn

    def get_all_doctors(self):
        try:
            doctors = list(self.db_conn.db.doctors.find())
            self.logger.info('Successfully fetched all doctors from the database.')
            return doctors
        except Exception as e:
            self.logger.error(f'Error fetching all doctors from the database: {e}')
            return jsonify({'error': f'Error fetching all doctors from the database: {e}'}), 500

    def add_doctor(self, new_doctor):
        try:
            # Find the last doctor record and calculate the next ID
            last_doctor = self.db_conn.db.doctors.find_one(sort=[('_id', -1)])
            next_id = (last_doctor['_id'] + 1 if last_doctor else 1)
            new_doctor["_id"] = next_id

            # Insert new doctor into the database
            self.db_conn.db.doctors.insert_one(new_doctor)
            self.logger.info(f'New doctor created with ID: {new_doctor["_id"]}')
            return new_doctor
        except Exception as e:
            self.logger.error(f'Error creating the new doctor: {e}')
            return jsonify({'error': f'Error creating the new doctor: {e}'}), 500

    def get_doctor_by_id(self, doctor_id):
        try:
            doctor = self.db_conn.db.doctors.find_one({'_id': doctor_id})
            if doctor:
                self.logger.info(f'Doctor with ID {doctor_id} fetched successfully.')
            else:
                self.logger.warning(f'Doctor with ID {doctor_id} not found.')
            return doctor
        except Exception as e:
            self.logger.error(f'Error fetching the doctor by ID {doctor_id}: {e}')
            return jsonify({'error': f'Error fetching the doctor by ID from the database: {e}'}), 500

    def update_doctor(self, doctor_id, doctor):
        try:
            update_doctor = self.get_doctor_by_id(doctor_id)

            if update_doctor:
                updated_doctor = self.db_conn.db.doctors.update_one({'_id': doctor_id}, {'$set': doctor})
                if updated_doctor.modified_count > 0:
                    self.logger.info(f'Doctor with ID {doctor_id} updated successfully.')
                    return updated_doctor
                else:
                    self.logger.info(f'Doctor with ID {doctor_id} is already up-to-date.')
                    return 'The doctor is already up-to-date'
            else:
                self.logger.warning(f'Doctor with ID {doctor_id} not found for update.')
                return None
        except Exception as e:
            self.logger.error(f'Error updating the doctor with ID {doctor_id}: {e}')
            return jsonify({'error': f'Error updating the doctor: {e}'}), 500

    def delete_doctor(self, doctor_id):
        try:
            deleted_doctor = self.get_doctor_by_id(doctor_id)

            if deleted_doctor:
                self.db_conn.db.doctors.delete_one({'_id': doctor_id})
                self.logger.info(f'Doctor with ID {doctor_id} deleted successfully.')
                return deleted_doctor
            else:
                self.logger.warning(f'Doctor with ID {doctor_id} not found for deletion.')
                return None
        except Exception as e:
            self.logger.error(f'Error deleting the doctor with ID {doctor_id}: {e}')
            return jsonify({'error': f'Error deleting the doctor: {e}'}), 500


if __name__ == '__main__':
    from models.doctor_model import DoctorModel  # Asegúrate de que la ruta sea correcta
    from doctor_service import DoctorService

    logger = Logger()
    db_conn = DoctorModel()  # Suponiendo que tienes un modelo similar a `DoctorModel`
    doctor_service = DoctorService(db_conn)

    try:
        # Conectamos a la base de datos
        db_conn.connect_to_database()

        # Obtener todos los doctores
        doctors = doctor_service.get_all_doctors()
        print(f'Doctors fetched: {doctors}')
        logger.info(f'Doctors fetched: {doctors}')

        # Crear un nuevo doctor con todos los campos
        new_doctor = doctor_service.add_doctor({
            'name': 'Albert Einstein',  # El nombre completo en un solo campo
            'license': '1234567890',
            'date_of_birth': '1879-03-14',  # Formato ISO para fecha
            'phone_number': '+1234567890',
            'email': 'cruzaz.einstein@example.com',
            'specialties': [
                {'specialty': 'Physics', 'consultation_fee': 100},
                {'specialty': 'Theoretical Physics', 'consultation_fee': 120}
            ],
        })
        logger.info(f'New doctor added: {new_doctor}')

        # Obtener un doctor por ID
        doctor = doctor_service.get_doctor_by_id(1)  # Usamos el ID del doctor para buscar
        logger.info(f'Doctor fetched by ID: {doctor}')

        # Actualizamos un doctor (suponiendo que el ID 1 existe)
        updated_doctor = doctor_service.update_doctor(1, {
            'name': 'Albert Einstein Jr.',  # Modificamos el nombre completo
            'specialties': [
                {'specialty': 'Physics', 'consultation_fee': 150},  # Modificamos la tarifa de consulta
                {'specialty': 'Theoretical Physics', 'consultation_fee': 130}
            ]
        })
        logger.info(f'Doctor updated: {updated_doctor}')

        # Eliminamos un doctor (suponiendo que el ID 1 existe)
        deleted_doctor = doctor_service.delete_doctor(1)
        logger.info(f'Doctor deleted: {deleted_doctor}')

    except Exception as e:
        logger.error(f'An error has occurred: {e}')
    
    finally:
        # Cerramos la conexión a la base de datos
        db_conn.close_connection()
        logger.info('Connection to the database was successfully closed.')