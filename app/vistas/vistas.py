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

ruta_no_encontrada = "Ruta no encontrada"
date_format = "%Y-%m-%d %H:%M:%S"

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
        if data['route_date'] is None:
            data['route_date'] = datetime.now()
        else:
            data['route_date'] = datetime.strptime(data['route_date'], date_format)
        data['id'] = generate_uuid()
        data['createdAt'] = datetime.now()
        data['updatedAt'] = datetime.now()
        ruta = Ruta(**data)
        db.session.add(ruta)
        db.session.commit()
        return {"message": "Ruta creada", "code": 201, "content": ruta_schema.dump(ruta)}, 201

class VistaRutaID(Resource):
    def get(self, ruta_id):
        ruta = Ruta.query.filter_by(id=ruta_id).first()
        if ruta is None:
            return {"message": ruta_no_encontrada, "code": 404}, 404
        return {"message": "OK", "content": ruta_schema.dump(ruta), "code": 200}, 200
    
    def put(self, ruta_id):
        data = request.get_json()
        ruta = Ruta.query.filter_by(id=ruta_id).first()
        if ruta is None:
            return {"message": ruta_no_encontrada, "code": 404}, 404
        
        # Cambios de campos
        changes = 0
        if ruta.route_name != data['route_name']:
            ruta.route_name = data['route_name']
            changes += 1
        if ruta.route_description != data['route_description']:
            ruta.route_description = data['route_description']
            changes += 1
        if ruta.route_location_A != data['route_location_A']:
            ruta.route_location_A = data['route_location_A']
            changes += 1
        if ruta.route_location_B != data['route_location_B']:
            ruta.route_location_B = data['route_location_B']
            changes += 1
        if ruta.route_latlon_A != data['route_latlon_A']:
            ruta.route_latlon_A = data['route_latlon_A']
            changes += 1
        if ruta.route_latlon_B != data['route_latlon_B']:
            ruta.route_latlon_B = data['route_latlon_B']
            changes += 1
        if ruta.route_type != data['route_type']:
            ruta.route_type = data['route_type']
            changes += 1
        if ruta.sport != data['sport']:
            ruta.sport = data['sport']
            changes += 1
        if ruta.link != data['link']:
            ruta.link = data['link']
            changes += 1
        if ruta.route_date != datetime.strptime(data['route_date'], date_format):
            ruta.route_date = datetime.strptime(data['route_date'], date_format)
            changes += 1

        print(f' * changes: {changes}')
        if changes == 0:
            return {"message": "No hay cambios", "code": 200}, 200

        ruta.updatedAt = datetime.now()
        db.session.commit()
        return {"message": "Ruta actualizada", "code": 200, "content": ruta_schema.dump(ruta)}, 200
    
    def delete(self, ruta_id):
        ruta = Ruta.query.filter_by(id=ruta_id).first()
        if ruta is None:
            return {"message": ruta_no_encontrada, "code": 404}, 404
        db.session.delete(ruta)
        db.session.commit()
        return {"message": "Ruta eliminada", "code": 200, "content": ruta_schema.dump(ruta)}, 200