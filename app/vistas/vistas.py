from modelos.modelos import ( Ruta, RutaSchema, db)
from datetime import datetime, timedelta
import hashlib
from flask import request
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource
import os
import requests
import uuid


ruta_schema = RutaSchema()

def generate_uuid():
    uid = uuid.uuid4()
    parts = str(uid).split('-')
    return parts[0]


class VistaHealthCheck(Resource):
    def get(self):
        return {"message": "OK", "code": 200}, 200
    
class VistaRuta(Resource):
    def get(self):
        rutas = Ruta.query.all()
        rutas = ruta_schema.dump(rutas, many=True)
        return {"message": "OK", "content": rutas, "code":200}, 200
    
    def post(self):
        data = request.get_json()
        data['id'] = generate_uuid()
        data['createdAt'] = datetime.now()
        data['updatedAt'] = datetime.now()
        ruta = Ruta(**data)
        db.session.add(ruta)
        db.session.commit()
        return {"message": "Ruta creada", "code": 201, "content": ruta_schema.dump(ruta)}, 201

class VistaRutaID(Resource):
    def put(self, ruta_id):
        data = request.get_json()
        ruta = Ruta.query.filter_by(id=ruta_id).first()
        if ruta is None:
            return {"message": "Ruta no encontrada", "code": 404}, 404
        
        # Cambios de campos
        if ruta.route_name != data['route_name']:
            ruta.route_name = data['route_name']
        if ruta.route_description != data['route_description']:
            ruta.route_description = data['route_description']
        if ruta.route_location_A != data['route_location_A']:
            ruta.route_location_A = data['route_location_A']
        if ruta.route_location_B != data['route_location_B']:
            ruta.route_location_B = data['route_location_B']
        if ruta.route_latlon_A != data['route_latlon_A']:
            ruta.route_latlon_A = data['route_latlon_A']
        if ruta.route_latlon_B != data['route_latlon_B']:
            ruta.route_latlon_B = data['route_latlon_B']
        if ruta.route_type != data['route_type']:
            ruta.route_type = data['route_type']
        if ruta.link != data['link']:
            ruta.link = data['link']

        ruta.updatedAt = datetime.now()
        db.session.commit()
        return {"message": "Ruta actualizada", "code": 200, "content": ruta_schema.dump(ruta)}, 200
    
    def delete(self, ruta_id):
        ruta = Ruta.query.filter_by(id=ruta_id).first()
        if ruta is None:
            return {"message": "Ruta no encontrada", "code": 404}, 404
        db.session.delete(ruta)
        db.session.commit()
        return {"message": "Ruta eliminada", "code": 200, "content": ruta_schema.dump(ruta)}, 200