from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns


def create_app():
    app = Flask(__name__)
    
    # Créer l'API Flask-RESTX
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBNB Application API',
        doc='/api/v1/'
    )  

    # Enregistrer le namespace users
    api.add_namespace(users_ns, path='/api/v1/users')
    
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
        
    return app
