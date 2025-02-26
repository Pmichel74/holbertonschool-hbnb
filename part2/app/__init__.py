from flask import Flask, redirect
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns  # Ajout ici

def create_app():
    app = Flask(__name__)
    
    # API Configuration
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='API for the HBnB project',
        doc='/api/v1'  # Documentation Swagger ici
    )

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')  # Ajout ici
    
    # Ajouter une redirection de la racine vers la documentation
    @app.route('/')
    def index():
        return redirect('/api/v1')
    
    return app
