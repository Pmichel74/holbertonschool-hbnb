from flask import Flask
from flask_restx import Api
from .api.v1.users import api as users_ns
from .api.v1.amenities import api as amenities_ns


def create_app():
    app = Flask(__name__)
    api = Api(
        app, 
        version='1.0', 
        title='HBNB API', 
        description='HBNB Application API', 
        doc='/api/v1/'
    )

    # Register the users namespace
    api.add_namespace(users_ns)

    # Register the amenities namespace
    api.add_namespace(amenities_ns)

    return app