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

    @api.doc("create_amenity")
    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        """Create a new amenity"""
        data = request.get_json()

        # Validate input
        if not data or "name" not in data:
            return {"error": "Missing 'name' field"}, 400

        # Create new amenity
        new_amenity = Amenity(name=data["name"])
        storage.new(new_amenity)
        storage.save()

        return new_amenity.to_dict(), 201
