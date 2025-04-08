from datetime import datetime
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='User password'),
    'is_admin': fields.Boolean(description='Administrative privileges', default=False)
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Forbidden - Admin access required')
    @jwt_required()
    def post(self):
        """Create a new user (admin only)"""
        try:
            # Get the current user's identity
            current_user_id = get_jwt_identity()
            
            # Get the claims that contain is_admin
            claims = get_jwt()  
            is_admin = claims.get('is_admin', False)
            
            # Check if the current user is an admin
            if not is_admin:
                return {'error': 'Admin privileges required'}, 403
            
            # Get the user data from the request
            user_data = api.payload
            email = user_data.get('email')
            
            # Set default value for is_admin if not provided
            if 'is_admin' not in user_data:
                user_data['is_admin'] = False
            
            # Check if email is already in use
            existing_user = facade.get_by_email(email)
            if existing_user:
                return {'error': 'Email already registered'}, 400
            
            # Create the new user
            new_user = facade.create_user(user_data)
            
            return {
                'id': new_user.id,
                'message': 'User successfully created'
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Get list of all users"""
        users = facade.get_all_users()
        return [{
            'id': user.id, 
            'first_name': user.first_name, 
            'last_name': user.last_name, 
            'email': user.email,
            'created_at': user.created_at.isoformat() if isinstance(user.created_at, datetime) else str(user.created_at),
            'updated_at': user.updated_at.isoformat() if isinstance(user.updated_at, datetime) else str(user.updated_at)
            # Password is intentionally excluded for security
        } for user in users], 200

@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id, 
            'first_name': user.first_name, 
            'last_name': user.last_name, 
            'email': user.email,
            'is_admin': user.is_admin,
            'created_at': user.created_at.isoformat() if isinstance(user.created_at, datetime) else str(user.created_at),
            'updated_at': user.updated_at.isoformat() if isinstance(user.updated_at, datetime) else str(user.updated_at)
            # Password is intentionally excluded for security
        }, 200

            
    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Forbidden - Cannot modify another user\'s data')
    @jwt_required()
    def put(self, user_id):
        """Update user details"""
        try:
            # Get the current user's identity
            current_user_id = get_jwt_identity()  # C'est une chaîne
            
            # Get the claims that contain is_admin
            claims = get_jwt()  
            is_admin = claims.get('is_admin', False)
            
            # Get the update data
            user_data = api.payload
            
            # Check if the current user is the requested user or an admin
            if current_user_id != user_id:
                # Si ce n'est pas le même utilisateur, vérifier si c'est un admin
                if not is_admin:
                    return {'error': 'Unauthorized action'}, 403
                    
                # Admin modifie un autre utilisateur
                # Vérifier si l'e-mail est modifié et s'il est déjà utilisé
                if 'email' in user_data:
                    email = user_data.get('email')
                    existing_user = facade.get_by_email(email)  # Noter le changement ici aussi
                    if existing_user and existing_user.id != user_id:
                        return {'error': 'Email already in use'}, 400
            else:
                # Les utilisateurs normaux ne peuvent pas modifier leur email ou mot de passe via ce endpoint
                if 'email' in user_data or 'password' in user_data:
                    return {'error': 'You cannot modify email or password'}, 400
            updated_user = facade.update_user(user_id, user_data)
            if not updated_user:
                return {'error': 'User not found'}, 404
            return {
                'id': updated_user.id, 
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name, 
                'email': updated_user.email,
                'is_admin': updated_user.is_admin,
                'created_at': updated_user.created_at.isoformat() if isinstance(updated_user.created_at, datetime) else str(updated_user.created_at),
                'updated_at': updated_user.updated_at.isoformat() if isinstance(updated_user.updated_at, datetime) else str(updated_user.updated_at)
                # Password is intentionally excluded for security
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
