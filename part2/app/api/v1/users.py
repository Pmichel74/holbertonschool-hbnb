from flask_restx import Namespace, Resource, fields
from app.services import facade
from werkzeug.exceptions import BadRequest

api = Namespace('users', description='User operations')

# Update input model to include password
user_model = api.model('User', {
    'first_name': fields.String(
        required=True, 
        description='First name of the user, max 50 characters',
        min_length=1,
        max_length=50,
        example='John'
    ),
    'last_name': fields.String(
        required=True, 
        description='Last name of the user, max 50 characters',
        min_length=1,
        max_length=50,
        example='Doe'
    ),
    'email': fields.String(
        required=True, 
        description='Email of the user, must be in valid format',
        pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        example='john.doe@example.com'
    ),
    'password': fields.String(
        required=True,
        description='User password',
        min_length=8,
        example='SecureP@ssw0rd'
    ),
    'is_admin': fields.Boolean(
        required=False, 
        default=False,
        description='Admin status, defaults to False',
        example=False
    )
})

# Complete response model including all fields
user_response_model = api.model('UserResponse', {
    'id': fields.String(description='User unique identifier'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'is_admin': fields.Boolean(description='Admin status'),
    'created_at': fields.DateTime(description='Timestamp of user creation'),
    'updated_at': fields.DateTime(description='Timestamp of last update')
})

# Create a model for registration response
registration_response = api.model('RegistrationResponse', {
    'id': fields.String(description='User unique identifier'),
    'message': fields.String(description='Success message'),
})

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_response_model, mask=False)  # Add mask=False here
    def get(self):
        """List all users"""
        return facade.get_users()

    @api.doc('create_user')
    @api.expect(user_model)
    @api.response(400, 'Validation Error')
    def post(self):
        """Create a new user"""
        try:
            user = facade.create_user(api.payload)
            
            # Retourner EXPLICITEMENT uniquement ces deux champs
            # Ne pas utiliser marshal_with pour être sûr
            response = {
                'id': str(user.id),
                'message': 'User successfully registered'
            }
            return response, 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
@api.response(404, 'User not found')
class User(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_response_model, mask=False)  # Add mask=False here
    def get(self, user_id):
        """Get a user by ID."""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, f"User {user_id} not found")
        return user

    @api.doc('update_user')
    @api.expect(user_model)
    @api.marshal_with(user_response_model, mask=False)  # Add mask=False here
    @api.response(400, 'Validation Error')
    def put(self, user_id):
        """Update a user."""
        try:
            user = facade.update_user(user_id, api.payload)
            if not user:
                api.abort(404, f"User {user_id} not found")
            return user
        except ValueError as e:
            api.abort(400, str(e))
