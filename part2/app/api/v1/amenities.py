from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from models import storage
from models.amenity import Amenity

# Define the namespace for Swagger
api = Namespace("amenities", description="Operations related to amenities")

# Define the model for Swagger documentation
amenity_model = api.model("Amenity", {
    "id": fields.String(required=True, description="Amenity ID"),
    "name": fields.String(required=True, description="Amenity name"),
})


@api.route("/")
class AmenityList(Resource):
    """Handles operations for the list of amenities"""

    @api.doc("get_amenities")
    @api.marshal_list_with(amenity_model)
    def get(self):
        """Retrieve all amenities"""
        amenities = storage.all(Amenity).values()
        return [amenity.to_dict() for amenity in amenities], 200
