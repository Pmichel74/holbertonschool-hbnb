from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns

def create_app():
    """Create and configure the Flask application.
    
    Creates a new Flask instance, configures the REST API 
    and registers the user namespace.
    
    Returns:
        Flask: A configured Flask application instance.
    """
    app = Flask(__name__)
    
    # API Configuration
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='API for the HBnB project',
        prefix='/api/v1'
    )

    api.add_namespace(users_ns, path='/users')
    
    return app
