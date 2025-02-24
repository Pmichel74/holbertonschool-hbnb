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
