from marshmallow import Schema, fields, validates, ValidationError
import re
from datetime import datetime

class DoctorSchema(Schema):
    # Fields with validation
    name = fields.String(required=True)
    license = fields.String(required=True)
    #date_of_birth = fields.Date(required=True)
    phone_number = fields.String(required=True)
    email = fields.Email(required=True)
    specialties = fields.List(fields.Dict(), required=True)

    @validates('name')
    def validate_name(self, value):
        # Check that the name contains at least two words (first and last name)
        if len(value.split()) < 2:
            raise ValidationError('The name must include both first and last name.')
        if not re.match(r"^[a-zA-Z ]+$", value):
            raise ValidationError('The name must only contain alphabetic characters and spaces.')

    @validates('license')
    def validate_license(self, value):
        # Validate that the license contains only numbers and is of a valid length
        
        if not re.match(r'^[k0-9]{10}$', value):
            raise ValidationError('The license number must be exactly 10 digits.')


 

    @validates('date_of_birth')
    def validate_date_of_birth(self, value):
        # Validate that the date of birth is not a future date
        print(" ")

        # Obtener la fecha actual en formato de cadena (YYYY-MM-DD)
        today = datetime.now().strftime('%Y-%m-%d')

        # Verificar si la fecha de nacimiento es mayor que la fecha de hoy
        if value > today:
            raise ValidationError('The date of birth cannot be in the future.')


    def validate_phone_number(self, value):
        # Validate that the phone number has exactly 10 digits (numeric only)
        if len(value) != 10 or not value.isdigit():
             raise ValidationError('The phone number must be exactly 10 digits.')

    @validates('email')
    def validate_email(self, value):
        # Email validation is handled by Marshmallow's Email field type, but additional checks can be added here if needed
        if '@' not in value:
            raise ValidationError('The email must be a valid email address.')

    @validates('specialties')
    def validate_specialties(self, value):
        # Check if the specialties list is not empty
        if not value:
            raise ValidationError('At least one specialty must be provided.')

        for specialty in value:
            # Check that each specialty has a name and consultation fee
            if 'specialty' not in specialty or not specialty['specialty']:
                raise ValidationError('Each specialty must have a valid name.')
            if 'consultation_fee' not in specialty or specialty['consultation_fee'] <= 0:
                raise ValidationError('The consultation fee for each specialty must be greater than 0.')

