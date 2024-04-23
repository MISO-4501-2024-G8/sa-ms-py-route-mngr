from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from datetime import timedelta
import os
from modelos.modelos import db
from vistas import VistaHealthCheck, VistaRuta, VistaRutaID
import uuid

def generate_uuid():
    uid = uuid.uuid4()
    parts = str(uid).split('-')
    return parts[0]


DATABASE_URI = os.getenv('DATABASE_URL', None)
if DATABASE_URI is None or DATABASE_URI == '':
    new_uuid = generate_uuid()
    DATABASE_URI = f"sqlite:///test_route_{new_uuid}.db"

print(' * DATABASE_URI: ')
print(DATABASE_URI)

app=Flask(__name__) # NOSONAR
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'MISO-4501-2024-G8' # NOSONAR
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=120)
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()
db.init_app(app)
db.create_all()

cors = CORS(app) # NOSONAR

api = Api(app)
api.add_resource(VistaHealthCheck, '/')
api.add_resource(VistaRuta, '/rutas')
api.add_resource(VistaRutaID, '/rutas/<string:ruta_id>')


jwt = JWTManager(app)

print(' * ROUTE MANAGEMENT corriendo ----------------')

if __name__=='__main__':
    app.run(port=5001)
