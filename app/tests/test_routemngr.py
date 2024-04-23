import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch
from app import app
import json
import random
import string
from flask_restful import Api
from flask import Flask
from flask_restful import Resource
from modelos.modelos import db
from urllib.parse import urlparse

os.environ['DATABASE_URL'] = 'sqlite:///test_route.db'

class TestVistaHealthCheck(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app = app.test_client()

    def test_health_check(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {"message": "OK", "code": 200})

class TestVistaRuta(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app = app.test_client()
        print(db.engine.url)
        self.app.testing = True

    def test_get_rutas(self):
        response = self.app.get('/rutas')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {"message": "OK", "content": [], "code": 200})
    
    def test_post_rutas(self):
        response = self.app.post('/rutas', json={
            "route_name": "Ruta de prueba",
            "route_description": "Descripcion de la ruta de prueba",
            "route_location_A": "Ubicacion A de la ruta de prueba",
            "route_location_B": "Ubicacion B de la ruta de prueba",
            "route_latlon_A": "Latitud y longitud de la ubicacion A de la ruta de prueba",
            "route_latlon_B": "Latitud y longitud de la ubicacion B de la ruta de prueba",
            "route_type": "Tipo de ruta de prueba",
            "link": "https://rutadeprueba.com"
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data)['message'], "Ruta creada")
        self.assertEqual(json.loads(response.data)['code'], 201)
        self.assertEqual(json.loads(response.data)['content']['route_name'], "Ruta de prueba")
        self.assertEqual(json.loads(response.data)['content']['route_description'], "Descripcion de la ruta de prueba")
        self.assertEqual(json.loads(response.data)['content']['route_location_A'], "Ubicacion A de la ruta de prueba")
        self.assertEqual(json.loads(response.data)['content']['route_location_B'], "Ubicacion B de la ruta de prueba")
        self.assertEqual(json.loads(response.data)['content']['route_latlon_A'], "Latitud y longitud de la ubicacion A de la ruta de prueba")
        self.assertEqual(json.loads(response.data)['content']['route_latlon_B'], "Latitud y longitud de la ubicacion B de la ruta de prueba")
        self.assertEqual(json.loads(response.data)['content']['route_type'], "Tipo de ruta de prueba")
        self.assertEqual(json.loads(response.data)['content']['link'], "https://rutadeprueba.com")
        self.assertIsNotNone(json.loads(response.data)['content']['id'])
        self.assertIsNotNone(json.loads(response.data)['content']['createdAt'])
        self.assertIsNotNone(json.loads(response.data)['content']['updatedAt'])
    
    def test_put_rutas(self):
        response = self.app.post('/rutas', json={
            "route_name": "Ruta de prueba",
            "route_description": "Descripcion de la ruta de prueba",
            "route_location_A": "Ubicacion A de la ruta de prueba",
            "route_location_B": "Ubicacion B de la ruta de prueba",
            "route_latlon_A": "Latitud y longitud de la ubicacion A de la ruta de prueba",
            "route_latlon_B": "Latitud y longitud de la ubicacion B de la ruta de prueba",
            "route_type": "Tipo de ruta de prueba",
            "link": "https://rutadeprueba.com"
        })
        ruta_id = json.loads(response.data)['content']['id']
        response = self.app.put(f'/rutas/{ruta_id}', json={
            "route_name": "Ruta de prueba modificada",
            "route_description": "Descripcion de la ruta de prueba modificada",
            "route_location_A": "Ubicacion A de la ruta de prueba modificada",
            "route_location_B": "Ubicacion B de la ruta de prueba modificada",
            "route_latlon_A": "Latitud y longitud de la ubicacion A de la ruta de prueba modificada",
            "route_latlon_B": "Latitud y longitud de la ubicacion B de la ruta de prueba modificada",
            "route_type": "Tipo de ruta de prueba modificada",
            "link": "https://rutadeprueba.com/modificada"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['message'], "Ruta actualizada")
        self.assertEqual(json.loads(response.data)['code'], 200)
        self.assertEqual(json.loads(response.data)['content']['route_name'], "Ruta de prueba modificada")
        self.assertEqual(json.loads(response.data)['content']['route_description'], "Descripcion de la ruta de prueba modificada")
        self.assertEqual(json.loads(response.data)['content']['route_location_A'], "Ubicacion A de la ruta de prueba modificada")
        self.assertEqual(json.loads(response.data)['content']['route_location_B'], "Ubicacion B de la ruta de prueba modificada")
        self.assertEqual(json.loads(response.data)['content']['route_latlon_A'], "Latitud y longitud de la ubicacion A de la ruta de prueba modificada")
        self.assertEqual(json.loads(response.data)['content']['route_latlon_B'], "Latitud y longitud de la ubicacion B de la ruta de prueba modificada")
        self.assertEqual(json.loads(response.data)['content']['route_type'], "Tipo de ruta de prueba modificada")
        self.assertEqual(json.loads(response.data)['content']['link'], "https://rutadeprueba.com/modificada")
        self.assertIsNotNone(json.loads(response.data)['content']['id'])
        self.assertIsNotNone(json.loads(response.data)['content']['createdAt'])
        self.assertIsNotNone(json.loads(response.data)['content']['updatedAt'])
        response_2 = self.app.put('/rutas/noexiste', json={
            "route_name": "Ruta de prueba modificada",
            "route_description": "Descripcion de la ruta de prueba modificada",
            "route_location_A": "Ubicacion A de la ruta de prueba modificada",
            "route_location_B": "Ubicacion B de la ruta de prueba modificada",
            "route_latlon_A": "Latitud y longitud de la ubicacion A de la ruta de prueba modificada",
            "route_latlon_B": "Latitud y longitud de la ubicacion B de la ruta de prueba modificada",
            "route_type": "Tipo de ruta de prueba modificada",
            "link": "https://rutadeprueba.com/modificada"
        })
        self.assertEqual(response_2.status_code, 404)
        self.assertEqual(json.loads(response_2.data)['message'], "Ruta no encontrada")
        response_3 = self.app.put(f'/rutas/{ruta_id}', json={
            "route_name": "Ruta de prueba modificada",
            "route_description": "Descripcion de la ruta de prueba modificada",
            "route_location_A": "Ubicacion A de la ruta de prueba modificada",
            "route_location_B": "Ubicacion B de la ruta de prueba modificada",
            "route_latlon_A": "Latitud y longitud de la ubicacion A de la ruta de prueba modificada",
            "route_latlon_B": "Latitud y longitud de la ubicacion B de la ruta de prueba modificada",
            "route_type": "Tipo de ruta de prueba modificada",
            "link": "https://rutadeprueba.com/modificada"
        })
        self.assertEqual(response_3.status_code, 200)
        self.assertEqual(json.loads(response_3.data)['message'], "Ruta actualizada")

    
    def test_delete_rutas(self):
        response = self.app.post('/rutas', json={
            "route_name": "Ruta de prueba",
            "route_description": "Descripcion de la ruta de prueba",
            "route_location_A": "Ubicacion A de la ruta de prueba",
            "route_location_B": "Ubicacion B de la ruta de prueba",
            "route_latlon_A": "Latitud y longitud de la ubicacion A de la ruta de prueba",
            "route_latlon_B": "Latitud y longitud de la ubicacion B de la ruta de prueba",
            "route_type": "Tipo de ruta de prueba",
            "link": "https://rutadeprueba.com"
        })
        ruta_id = json.loads(response.data)['content']['id']
        response = self.app.delete(f'/rutas/{ruta_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['message'], "Ruta eliminada")
        self.assertEqual(json.loads(response.data)['code'], 200)
        self.assertEqual(json.loads(response.data)['content']['route_name'], "Ruta de prueba")
        self.assertEqual(json.loads(response.data)['content']['route_description'], "Descripcion de la ruta de prueba")
        self.assertEqual(json.loads(response.data)['content']['route_location_A'], "Ubicacion A de la ruta de prueba")
        self.assertEqual(json.loads(response.data)['content']['route_location_B'], "Ubicacion B de la ruta de prueba")
        self.assertEqual(json.loads(response.data)['content']['route_latlon_A'], "Latitud y longitud de la ubicacion A de la ruta de prueba")
        self.assertEqual(json.loads(response.data)['content']['route_latlon_B'], "Latitud y longitud de la ubicacion B de la ruta de prueba")
        self.assertEqual(json.loads(response.data)['content']['route_type'], "Tipo de ruta de prueba")
        self.assertEqual(json.loads(response.data)['content']['link'], "https://rutadeprueba.com")
        self.assertIsNotNone(json.loads(response.data)['content']['id'])
        self.assertIsNotNone(json.loads(response.data)['content']['createdAt'])
        self.assertIsNotNone(json.loads(response.data)['content']['updatedAt'])
        response_2 = self.app.delete(f'/rutas/{ruta_id}')
        self.assertEqual(response_2.status_code, 404)
        self.assertEqual(json.loads(response_2.data)['message'], "Ruta no encontrada")

    def test_get_ruta(self):
        response = self.app.get('/rutas/noexiste')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data), {"message": "Ruta no encontrada", "code": 404})
        response = self.app.post('/rutas', json={
            "route_name": "Ruta de prueba",
            "route_description": "Descripcion de la ruta de prueba",
            "route_location_A": "Ubicacion A de la ruta de prueba",
            "route_location_B": "Ubicacion B de la ruta de prueba",
            "route_latlon_A": "Latitud y longitud de la ubicacion A de la ruta de prueba",
            "route_latlon_B": "Latitud y longitud de la ubicacion B de la ruta de prueba",
            "route_type": "Tipo de ruta de prueba",
            "link": "https://rutadeprueba.com"
        })
        ruta_id = json.loads(response.data)['content']['id']
        response = self.app.get(f'/rutas/{ruta_id}')
        self.assertEqual(response.status_code, 200)
        self.app.delete(f'/rutas/{ruta_id}')

