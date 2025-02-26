from flask_restx import Api
from flask import Blueprint
from api.v1.amenities import api as amenities_ns

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

api = Api(blueprint, doc='/docs')

api.add_namespace(amenities_ns)
