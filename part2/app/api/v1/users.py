#Debut partie Rayane
#!/usr/bin/python3
"""User API routes"""

from flask import Flask, jsonify, abort
from models import storage
from models.user import User

app = Flask(__name__)

@app.route('/api/v1/users/', methods=['GET'])
def get_users():
    """Retrieve all users"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users]), 200

@app.route('/api/v1/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieve a user by ID"""
    user = storage.get(User, user_id)
    if not user:
        abort(404, description="User not found")
    return jsonify(user.to_dict()), 200

if __name__ == '__main__':
    app.run(debug=True)
    
#Fin partie Rayane

from flask_restx import Namespace, Resource, fields
from app.services.facade import facade
import re

api = Namespace('users', description='User operations')


# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_input_model, validate=True)
    @api.marshal_with(user_output_model, code=201)
    @api.doc(responses={
        201: 'User created successfully',
        400: 'Email already registered or invalid data'
    })
    def post(self):
        """Create a new user"""
        try:
            user_data = api.payload
            if facade.get_user_by_email(user_data['email']):
                api.abort(400, 'Email already registered')
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except Exception as e:
<<<<<<< HEAD
            api.abort(400, str(e))

@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.expect(update_user_model)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Validation error')
    def put(self, user_id):
        """
        Update an existing user's information
        
        Args:
            user_id (str): The unique identifier of the user to update
            
        Returns:
            tuple: JSON response with updated user data and HTTP status code
            
        Raises:
            400: If email format is invalid or already taken
            404: If user is not found
            
        Example:
            PUT /api/v1/users/123e4567-e89b-12d3-a456-426614174000
            {
                "first_name": "John",
                "last_name": "Smith",
                "email": "john.smith@example.com"
            }
        """
        data = api.payload
        
        # Email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, data['email']):
            api.abort(400, "Invalid email format")

        try:
            # Check if email is already used by another user
            if facade.is_email_taken(data['email'], exclude_id=user_id):
                api.abort(400, "This email is already used by another user")

            updated_user = facade.update_user(
                user_id,
                data['first_name'],
                data['last_name'],
                data['email']
            )

            if not updated_user:
                api.abort(404, "User not found")

            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email
            }, 200

        except ValueError as e:
            api.abort(400, str(e))
=======
            api.abort(400, str(e))
>>>>>>> refs/remotes/origin/Test
