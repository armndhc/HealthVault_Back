from marshmallow import fields, validates, ValidationError

class RecipeSchema:
    observations = fields.String(required=True)
    diagnostic = fields.String(required=True)
    weight = fields.Integer(required=True)
    temperature = fields.Integer(required=True)
    bloodPressure = fields.Integer(required=True)

    @validates('observations')
    def validate_observations(self, value):
        if len(value) < 3:
            raise ValidationError("Observations must be at least 5 character long.")

    @validates('diagnostic')
    def validate_diagnostic(self, value):
        if len(value) < 3:
            raise ValidationError("Diagnostic must be at least 5 character long.")
    
    @validates('weight')
    def validate_weight(self, value):
        try:
            if float(value) < 0:
                raise ValidationError("Weight must be a non-negative integer and cant be cero.")
        except:
            raise ValidationError("Weight must be a non-negative integer and cant be cero.")
    @validates('temperature')
    def validate_temperature(self, value):
        try:
            if float(value) < 0:
                raise ValidationError("Temperature must be a non-negative integer and cant be cero.")
        except:
            raise ValidationError("Temperature must be a non-negative integer and cant be cero.")
    @validates('bloodPressure')
    def validate_bloodPressure(self, value):
        if len(value) < 0:
            raise ValidationError("bloodPressure must be at least 5 character long.")
 
