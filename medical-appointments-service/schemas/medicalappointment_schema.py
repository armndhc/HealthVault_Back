from datetime import datetime
from marshmallow import Schema, fields, validates, ValidationError
import re

# Define the schema for medicalappointment validations
class MedicalAppointmentSchema(Schema):
    date = fields.String(required=True)
    special = fields.String(required=True)

    # Custom validation for the 'date' field
    @validates('date')
    def validate_date(self, value):
        try:
            datetime.strptime(value, '%d %b %Y %H:%M') 
        except ValueError:
            raise ValidationError("Date must be in the format 'DD MMM YYYY HH:MM'")

    # Custom validation for the 'special' field
    @validates('reason')
    def validate_reason(self, value):
        if value and len(value) > 255:
            raise ValidationError("Special instructions must not exceed 255 characters.")
