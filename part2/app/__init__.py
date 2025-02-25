from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns

def create_app():
    app = Flask(__name__)
    
    # Configuration de l'API
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='API pour le projet HBnB',
        prefix='/api/v1'
    )

    # Enregistrement des namespaces
    api.add_namespace(users_ns)

    return app
