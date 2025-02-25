from flask_restx import Namespace, Resource, fields
from app.services import facade

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

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_response_model)
    def get(self):
        """List all users"""
        return facade.get_users()

    @api.doc('create_user')
    @api.expect(user_model)
    @api.marshal_with(user_response_model, code=201)
    def post(self):
        """Create a new user"""
        return facade.create_user(api.payload), 201

@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
class User(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_response_model)
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get a user by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, f"User {user_id} not found")
        return user

    @api.doc('update_user')
    @api.expect(user_model)
    @api.marshal_with(user_response_model)
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update a user"""
        user = facade.update_user(user_id, api.payload)
        if not user:
            api.abort(404, f"User {user_id} not found")
        return user
