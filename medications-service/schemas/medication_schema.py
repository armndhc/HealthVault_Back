from marshmallow import fields, validates, ValidationError

# Schema for medication
class MedicationSchema:
    name = fields.String(required=True)
    unit = fields.String(required=True)
    existence = fields.Integer(required=True)
    image = fields.String(required=True)

    # Validating name
    @validates('name')
    def validate_name(self, value):
        if not value:
            raise ValidationError("Name must be a non-empty string.")

    # Validating unit
    @validates('unit')
    def validate_unit(self, value):
        if not value:
            raise ValidationError("Unit must be a non-empty string.")

    # Validating existence
    @validates('existence')
    def validate_existence(self, value):
        try:
            if int(value) < 0:
                raise ValidationError("Existence must be a non-negative integer.")
        except:
            raise ValidationError("Existence must be a non-negative integer.")

    # Validating price
    @validates('price')
    def validate_price(self, value):
        try:
            if float(value) < 0:
                raise ValidationError("Price must be a non-negative number.")
        except:
            raise ValidationError("Price must be a non-negative number.")

    # Validating administration
    @validates('administration')
    def validate_administration(self, value):
        if not value:
            raise ValidationError("Administration must be a non-empty string.")

    # Validating distributor
    @validates('distributor')
    def validate_distributor(self, value):
        if not value:
            raise ValidationError("Distributor must be a non-empty string.")

    # Validating image
    @validates('image')
    def validate_image(self, value):
        if not value:
            raise ValidationError("Image must be a base-64-image string.")

