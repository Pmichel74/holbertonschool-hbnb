from flask import Flask          # Base Flask framework
from flask_restx import Api      # RESTful API extension
from app.api.v1.users import api as users_ns  # Users API namespace

def create_app():
    # Create Flask application instance
    app = Flask(__name__)

    # Create API instance with Swagger documentation
    api = Api(app, 
             version='1.0',
             title='HBnB API',
             description='HBnB Application API')

    # Register the users namespace with path prefix
    api.add_namespace(users_ns, path='/api/v1/users')
    
    return app
