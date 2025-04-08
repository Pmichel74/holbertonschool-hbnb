from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import facade
from datetime import datetime

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, description="List of amenities ID's")
})

# Model for detailed place response including relationships
place_detail_model = api.model('PlaceDetail', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'owner': fields.Nested(user_model, description='Owner details'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place"""
        try:
            # Get the current user's identity from the JWT token
            current_user_id = get_jwt_identity()
            
            place_data = api.payload
            
            # Set the owner_id to the current user's ID
            place_data['owner_id'] = current_user_id
            new_place = facade.create_place(place_data)
            
            # Convertir les amenities en liste d'ID ou de dictionnaires si nécessaire
            amenities_list = []
            if hasattr(new_place, 'amenities') and new_place.amenities:
                amenities_list = [{'id': amenity.id, 'name': amenity.name} for amenity in new_place.amenities]
                
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner_id,
                'amenities': amenities_list  # Liste de dictionnaires ou d'IDs
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [{
            'id': place.id,
            'title': place.title,
            'latitude': place.latitude,
            'longitude': place.longitude
        } for place in places], 200

@api.route('/<string:place_id>')
@api.param('place_id', 'The place identifier')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place_details = facade.get_place_with_details(place_id)
        if not place_details:
            return {'error': 'Place not found'}, 404
        return place_details, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Forbidden - Only the owner can modify this place')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        try:
            # Get the current user's identity and JWT claims
            current_user_id = get_jwt_identity()  # C'est une chaîne (ID utilisateur)
            
            # Get the claims that contain is_admin
            claims = get_jwt()  
            is_admin = claims.get('is_admin', False)
            
            # Get the place to check ownership
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404
                
            # Check if the current user is the owner of the place or an admin
            if not is_admin and place.owner_id != current_user_id:
                return {'error': 'Unauthorized action'}, 403
            
            place_data = api.payload
            updated_place = facade.update_place(place_id, place_data)
            
            if not updated_place:
                return {'error': 'Place not found'}, 404
                
            # Convertir les amenities en liste d'ID ou de dictionnaires si nécessaire
            amenities_list = []
            if hasattr(updated_place, 'amenities') and updated_place.amenities:
                amenities_list = [{'id': amenity.id, 'name': amenity.name} for amenity in updated_place.amenities]
                
            return {
                'id': updated_place.id,
                'title': updated_place.title,
                'description': updated_place.description,
                'price': updated_place.price,
                'latitude': updated_place.latitude,
                'longitude': updated_place.longitude,
                'owner_id': updated_place.owner_id,
                'amenities': amenities_list  # Liste de dictionnaires ou d'IDs
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        
    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    @api.response(403, 'Forbidden - Only the owner or an admin can delete this place')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place"""
        try:
            # Get the current user's identity and JWT claims
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            
            # Get the place to check ownership
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404
                
            # Check if the current user is the owner of the place or an admin
            if not is_admin and str(place.owner_id) != str(current_user_id):
                return {'error': 'Unauthorized action'}, 403
            
            # Delete the place
            success = facade.delete_place(place_id)
            if not success:
                return {'error': 'Place not found or could not be deleted'}, 404
                
            return {'message': 'Place deleted successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 500

# Adding the review model
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

# Update the place_detail_model to include reviews
place_detail_model = api.model('PlaceDetail', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'owner': fields.Nested(user_model, description='Owner details'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

@api.route('/<string:place_id>/reviews')
@api.param('place_id', 'The place identifier')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {'error': 'Place not found'}, 404

        # Convertir les objets datetime en chaînes pour la sérialisation     
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'created_at': review.created_at.isoformat() if isinstance(review.created_at, datetime) else str(review.created_at),
            'updated_at': review.updated_at.isoformat() if isinstance(review.updated_at, datetime) else str(review.updated_at)
        } for review in reviews], 200
