from flask_restx import Namespace, Resource, fields
from app.services.facade import get_facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

user_response_model = api.model('UserResponse', {
    'id': fields.String(description='User unique identifier'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user')
})

# Use the get_facade function to get an instance of HBnBFacade
facade_instance = get_facade()

@api.route('/')
class UserList(Resource):
    def get(self):
        """List all users"""
        return facade_instance.get_users()

    @api.expect(user_model)
    
    def post(self):
        """Create a new user"""
        return facade_instance.create_user(api.payload), 201

@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
class User(Resource):
    def get(self, user_id):
        """Get a user by ID."""
        user = facade_instance.get_user(user_id)
        if not user:
            api.abort(404, f"User {user_id} not found")
        return user

    @api.expect(user_model)
    def put(self, user_id):
        """Update a user."""
        user = facade_instance.update_user(user_id, api.payload)
        if not user:
            api.abort(404, f"User {user_id} not found")
        return user
