from datetime import datetime
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Forbidden - Admin access required')
    @jwt_required()
    def post(self):
        """Create a new amenity (admin only)"""
        try:
            # Get the current user's identity
            current_user_id = get_jwt_identity()  # C'est une chaîne (ID utilisateur)
            claims = get_jwt()  # Obtenir les claims du token
            is_admin = claims.get('is_admin', False)
            
            # Check if the current user is an admin
            if not is_admin:
                return {'error': 'Admin privileges required'}, 403
                
            # Get the amenity data from the request
            amenity_data = api.payload
            new_amenity = facade.create_amenity(amenity_data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name,
                'created_at': new_amenity.created_at.isoformat() if isinstance(new_amenity.created_at, datetime) else str(new_amenity.created_at),
                'updated_at': new_amenity.updated_at.isoformat() if isinstance(new_amenity.updated_at, datetime) else str(new_amenity.updated_at)
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Get list of all amenities"""
        amenities = facade.get_all_amenities()
        return [{
            'id': amenity.id,
            'name': amenity.name,
            'created_at': amenity.created_at.isoformat() if isinstance(amenity.created_at, datetime) else str(amenity.created_at),
            'updated_at': amenity.updated_at.isoformat() if isinstance(amenity.updated_at, datetime) else str(amenity.updated_at)
        } for amenity in amenities], 200
        
@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The amenity identifier')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        try:
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                return {'error': 'Amenity not found'}, 404
            return {
                'id': amenity.id,
                'name': amenity.name,
                'created_at': amenity.created_at.isoformat() if isinstance(amenity.created_at, datetime) else str(amenity.created_at),
                'updated_at': amenity.updated_at.isoformat() if isinstance(amenity.updated_at, datetime) else str(amenity.updated_at)
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Forbidden - Admin access required')
    @jwt_required()
    def put(self, amenity_id):
        """Update amenity details (admin only)"""
        try:
            # Get the current user's identity
            current_user_id = get_jwt_identity()  # C'est une chaîne (ID utilisateur)
            
            # Get the claims that contain is_admin
            claims = get_jwt()  # Obtenir les claims du token
            is_admin = claims.get('is_admin', False)
            
            # Check if the current user is an admin
            if not is_admin:
                return {'error': 'Admin privileges required'}, 403
                
            # Get the amenity data from the request
            amenity_data = api.payload
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            if not updated_amenity:
                return {'error': 'Amenity not found'}, 404
            return {
                'id': updated_amenity.id,
                'name': updated_amenity.name,
                'created_at': updated_amenity.created_at.isoformat() if isinstance(updated_amenity.created_at, datetime) else str(updated_amenity.created_at),
                'updated_at': updated_amenity.updated_at.isoformat() if isinstance(updated_amenity.updated_at, datetime) else str(updated_amenity.updated_at)
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
