from flask_restx import Api
from flask import Blueprint
from app.api.v1.amenities import api as amenities_ns  # Correction ici

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

api = Api(blueprint, doc='/docs')

api.add_namespace(amenities_ns)
