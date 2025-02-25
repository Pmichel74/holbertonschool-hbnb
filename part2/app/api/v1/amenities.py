from flask import jsonify
from flask_restx import Namespace, Resource
from models import storage
from models.amenity import Amenity

# Define the namespace for Swagger
api = Namespace("amenities", description="Operations related to amenities")

# Define the model for Swagger documentation
amenity_model = api.model("Amenity", {
    "id": fields.String(required=True, description="Amenity ID"),
    "name": fields.String(required=True, description="Amenity name"),
})
