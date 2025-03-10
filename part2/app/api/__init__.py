#!/usr/bin/python3
"""Initialisation de l'API Blueprint"""
from flask import Blueprint
from flask_restx import Api

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint,
          title='HBNB API',
          version='1.0',
          description='API pour le projet HBNB')

# Import and register namespaces
from app.api.v1 import get_namespaces
for ns in get_namespaces():
    # Définir explicitement le chemin pour chaque namespace
    path = None
    if ns.name == 'users':
        path = '/v1/users'
    elif ns.name == 'places':
        path = '/v1/places'
    elif ns.name == 'auth':
        path = '/v1/auth'
    elif ns.name == 'amenities':
        path = '/v1/amenities'
    elif ns.name == 'reviews':
        path = '/v1/reviews'
    
    if path:
        api.add_namespace(ns, path=path)
    else:
        api.add_namespace(ns)
