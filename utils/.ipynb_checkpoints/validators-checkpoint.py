from marshmallow import Schema, fields

class ExoplanetSchema(Schema):
    name = fields.Str(required=True)
    mass = fields.Float(required=True)
    radius = fields.Float(required=True)
    temperature = fields.Float(required=True)
