# app/controllers/user_controller.py
from flask import Blueprint, request, jsonify
from app.business_logic.user_logic import update_user, get_all_users
from app.models.user import User

user_api = Blueprint('user_api', __name__)

@user_api.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user_endpoint(user_id):
    data = request.get_json()

    if not data.get('first_name') or not data.get('last_name') or not data.get('email'):
        return jsonify({"error": "First name, last name and email are required"}), 400

    try:
        updated_user = update_user(user_id, data)
        if updated_user is None:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify(updated_user.to_dict()), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@user_api.route('/api/v1/users/', methods=['GET'])
def get_all_users_endpoint():
    users = [user.to_dict() for user in get_all_users().values()]
    return jsonify(users), 200
