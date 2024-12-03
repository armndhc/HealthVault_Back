from marshmallow import Schema, fields, validates, ValidationError
from logger.logger_base import Logger

class ItemSchema(Schema):
    name = fields.Str(required=True)
    quantity = fields.Int(required=True)
    price = fields.Float(required=True)

# Definimos el esquema PaymentSchema con las validaciones
class PaymentSchema(Schema):
    name = fields.String(required=True)
    order_id = fields.Integer(required=True)
    total = fields.Float(required=True)
    rfc = fields.String(required=True)
    payment_type = fields.String(required=True)
    items = fields.List(fields.Nested(ItemSchema), required=True)

    @validates('name')
    def validate_name(self, value):
        if len(value) < 1 or not value.isalnum():
            raise ValidationError('El name .')
        
    @validates('rfc')
    def validate_rfc(self, value):
        if len(value) != 13 or not value.isalnum():
            raise ValidationError('El RFC debe tener 13 caracteres alfanuméricos.')

    @validates('order_id')
    def validate_order_id(self, value):
        if not isinstance(value, int) or value < 1:
            raise ValidationError('El id  debe ser un número entero mayor que 0.')

    @validates('total')
    def validate_total(self, value):
        if not isinstance(value, int) or value < 1:
            raise ValidationError('LTOTAAAL 0.')

    @validates('payment_type')
    def validate_payment_type(self, value):
        if not value:
            raise ValidationError('PAGPPPP ro mayor que 0.')
    
    @validates('items')
    def validate_items(self, value):
        if not value or len(value) == 0:
            raise ValidationError('EITEMMMS mero entero mayor que 0.')


# Prueba de validación
if __name__ == '_main_':
    logger = Logger()  # Instanciamos el logger
    schema = PaymentSchema()  # Creamos la instancia del esquema

    # Datos de prueba con campos inválidos
    new_payment = {
        'name': "HOOOLLL",
        #'mesa': 3,  # Mesa inválida (debe ser mayor a 0)
        'numero_de_orden': 12345,  # Número de orden válido
        'rfc': 'INVALIDRFCGHA'  # RFC inválido (debe tener 13 caracteres alfanuméricos)
    }

    try:
        # Intentamos cargar los datos y validar
        schema.load(new_payment)  # Esto valida el nuevo pago con el esquema
        print("El pago es válido.")  # Si no se lanza ninguna excepción, se imprime que es válido

    except ValidationError as e:
        # Si hay un error de validación, lo capturamos y lo mostramos
        logger.error(f'An error has occurred: {e.messages}')  # Mostramos el error con los mensajes de validación