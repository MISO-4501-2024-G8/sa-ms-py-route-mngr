from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Ruta(db.Model):
    __tablename__ = 'route'

    id = db.Column(db.String(255), primary_key=True)
    route_name = db.Column(db.String(255))
    route_description = db.Column(db.String(500))
    route_location_A = db.Column(db.String(255))
    route_location_B = db.Column(db.String(255))
    route_latlon_A = db.Column(db.String(255))
    route_latlon_B = db.Column(db.String(255))
    route_type = db.Column(db.String(255))
    link = db.Column(db.String(500))
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)

class RutaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Ruta
        include_relationships = True
        load_instance = True