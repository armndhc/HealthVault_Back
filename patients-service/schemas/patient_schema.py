from marshmallow import Schema, fields, validates, ValidationError
from datetime import datetime

class PatientSchema(Schema):
    name = fields.String(required=True)
    lastName = fields.String(required=True)
    weight = fields.Float(required=True)
    height = fields.Float(required=True)
    heartrate = fields.Integer(required=True)
    bloodPressure = fields.String(required=True)
    sugarBlood = fields.Float(required=True)
    birthDate = fields.String(required=True)
    phone = fields.String(required=True)
    email = fields.Email(required=True)
    bloodType = fields.String(required=True)
    allergies = fields.String(required=False)
    gender = fields.String(required=True)
    familyHistory = fields.String(required=False)
    medicalHistory = fields.String(required=False)
    emergencyContact = fields.String(required=True)
    emergencyPhone = fields.String(required=True)
    socialSecurity = fields.String(required=True)
    avatar = fields.String(required=False)

    @validates('name')
    def validate_name(self, value):
        if not value or not value.strip():
            raise ValidationError("Name must be a non-empty string.")
        if len(value) > 50:
            raise ValidationError("Name must not exceed 50 characters.")

    @validates('lastName')
    def validate_lastName(self, value):
        if not value or not value.strip():
            raise ValidationError("Last name must be a non-empty string.")
        if len(value) > 50:
            raise ValidationError("Last name must not exceed 50 characters.")

    @validates('weight')
    def validate_weight(self, value):
        if float(value) <= 0:
            raise ValidationError("Weight must be a positive number.")
        if float(value)  > 500:
            raise ValidationError("Weight seems unrealistic (over 500 kg).")

    @validates('height')
    def validate_height(self, value):
        if float(value) <= 0:
            raise ValidationError("Height must be a positive number.")
        if float(value)  > 300:
            raise ValidationError("Height seems unrealistic (over 300 cm).")

    @validates('heartrate')
    def validate_heartrate(self, value):
        if float(value) < 30 or float(value) > 200:
            raise ValidationError("Heart rate must be between 30 and 200 bpm.")

    @validates('bloodPressure')
    def validate_bloodPressure(self, value):
        if not value or not value.strip():
            raise ValidationError("Blood pressure must be a non-empty string.")
        if not all(part.isdigit() for part in value.split('/')):
            raise ValidationError("Blood pressure must be in the format '120/80'.")

    @validates('sugarBlood')
    def validate_sugarBlood(self, value):
        if float(value) < 0:
            raise ValidationError("Blood sugar level must be a non-negative number.")

    @validates('birthDate')
    def validate_birthDate(self, value):
        try:
            date = datetime.strptime(value, '%Y-%m-%d')
            if date > datetime.now():
                raise ValidationError("Birth date cannot be in the future.")
        except ValueError:
            raise ValidationError("Birth date must be in the format 'YYYY-MM-DD'.")

    @validates('phone')
    def validate_phone(self, value):
        if len(value) < 5:
            raise ValidationError("Phone number must be at least 10 digits.")

    @validates('email')
    def validate_email(self, value):
        if not value:
            raise ValidationError("Email must be provided.")
        if len(value) > 100:
            raise ValidationError("Email must not exceed 100 characters.")

    @validates('bloodType')
    def validate_bloodType(self, value):
        valid_blood_types = {'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'}
        if value not in valid_blood_types:
            raise ValidationError("Blood type must be one of: A+, A-, B+, B-, AB+, AB-, O+, O-.")

    @validates('emergencyContact')
    def validate_emergencyContact(self, value):
        if not value.strip():
            raise ValidationError("Emergency contact name must be provided.")

    @validates('emergencyPhone')
    def validate_emergencyPhone(self, value):
        if len(value) < 5:
            raise ValidationError("Emergency phone number must be at least 10 digits.")

    @validates('socialSecurity')
    def validate_socialSecurity(self, value):
        if not value or not value.strip():
            raise ValidationError("Social security number must be provided.")
        if len(value) > 20:
            raise ValidationError("Social security number must not exceed 20 characters.")

    @validates('gender')
    def validate_gender(self, value):
        valid_genders = {'Male', 'Female', 'Other'}
        if value not in valid_genders:
            raise ValidationError("Gender must be 'Male', 'Female', or 'Other'.")
