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

api = Namespace('users', description='User operations')

# Validation model for input
user_input_model = api.model('UserInput', {
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='Password')
})

# Response model (without password)
user_output_model = api.model('UserOutput', {
    'id': fields.String(description='Unique user ID'),
    'first_name': fields.String(description='User first name'),
    'last_name': fields.String(description='User last name'),
    'email': fields.String(description='User email')
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

            # Check email uniqueness
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                api.abort(400, 'Email already registered')

            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
            
        except Exception as e:
            api.abort(400, str(e))