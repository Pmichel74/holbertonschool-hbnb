from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns  # Ajout du namespace des amenities

def create_app():
    app = Flask(__name__)
    
    # Configuration de l'API
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='API pour le projet HBnB',
        doc='/api/v1'
    )

    # Enregistrement des namespaces
    api.add_namespace(users_ns)
    api.add_namespace(amenities_ns, path='/amenities')  # Ajout du namespace des amenities

    return app
