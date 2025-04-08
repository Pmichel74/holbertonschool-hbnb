#!/usr/bin/env python3
"""
Test script for admin endpoints in the HBnB API.

This script demonstrates different strategies to test admin endpoints:
1. Creating an admin user directly in the database
2. Getting a JWT token for the admin user
3. Testing admin endpoints with the admin token
"""

import os
import json
import requests
import subprocess
from uuid import uuid4
from datetime import datetime
import sys
import time

# API base URL
BASE_URL = "http://127.0.0.1:5000/api/v1"

# Strategy 1: Create an admin user directly in the database
def create_admin_user_in_db():
    """
    Create an admin user directly in the database.
    
    This approach bypasses the API's normal user creation flow to create
    an admin user for testing purposes.
    
    Returns:
        dict: The admin user data including email and password
    """
    print("\n=== Strategy 1: Create an admin user directly in the database ===")
    
    # Generate a unique email to avoid conflicts
    admin_email = f"admin_{uuid4().hex[:8]}@example.com"
    admin_password = "AdminPassword123!"
    
    # Admin user data
    admin_user = {
        "email": admin_email,
        "password": admin_password,
        "first_name": "Admin",
        "last_name": "User",
        "is_admin": True
    }
    
    print(f"Admin user data: {admin_user}")
    print("To implement this strategy:")
    print("1. Connect to your database")
    print("2. Insert the admin user with is_admin=True")
    print("3. Use the admin credentials to obtain a JWT token")
    
    return admin_user

# Strategy 2: Modify the authentication logic temporarily for testing
def modify_auth_for_testing():
    """
    Temporarily modify the authentication logic for testing.
    
    This approach involves temporarily modifying the authentication code
    to grant admin privileges to a specific test user.
    
    Returns:
        str: Instructions for implementing this strategy
    """
    print("\n=== Strategy 2: Modify the authentication logic temporarily for testing ===")
    
    instructions = """
    To implement this strategy:
    
    1. Temporarily modify the login endpoint in auth.py to grant admin privileges:
    
    ```python
    @api.route('/login')
    class Login(Resource):
        @api.expect(login_model)
        def post(self):
            credentials = api.payload
            
            # For testing: Grant admin privileges to a specific test user
            if credentials['email'] == 'test_admin@example.com':
                # Create a test admin user if it doesn't exist
                user = facade.get_user_by_email(credentials['email'])
                if not user:
                    user_data = {
                        'email': 'test_admin@example.com',
                        'password': 'TestAdminPass123!',
                        'first_name': 'Test',
                        'last_name': 'Admin',
                        'is_admin': True
                    }
                    user = facade.create_user(user_data)
                
                # Create token with admin privileges
                access_token = create_access_token(
                    identity={'id': str(user.id), 'is_admin': True}
                )
                return {'access_token': access_token}, 200
            
            # Normal authentication flow
            user = facade.get_user_by_email(credentials['email'])
            if not user or not user.verify_password(credentials['password']):
                return {'error': 'Invalid credentials'}, 401
                
            access_token = create_access_token(
                identity={'id': str(user.id), 'is_admin': user.is_admin}
            )
            return {'access_token': access_token}, 200
    ```
    
    2. After testing, revert these changes to maintain security
    """
    
    print(instructions)
    return instructions

# Strategy 3: Create a special test endpoint
def create_test_endpoint():
    """
    Create a special test endpoint for obtaining admin tokens.
    
    This approach involves creating a special endpoint that is only
    available in development/test environments for obtaining admin tokens.
    
    Returns:
        str: Instructions for implementing this strategy
    """
    print("\n=== Strategy 3: Create a special test endpoint ===")
    
    instructions = """
    To implement this strategy:
    
    1. Create a special test endpoint in auth.py that is only available in test/development environments:
    
    ```python
    # Only include this endpoint in development/test environments
    if os.environ.get('FLASK_ENV') == 'development' or os.environ.get('TESTING') == 'true':
        @api.route('/test/admin-token')
        class TestAdminToken(Resource):
            def get(self):
                # Create a token with admin privileges for testing
                admin_identity = {'id': 'test_admin_id', 'is_admin': True}
                access_token = create_access_token(identity=admin_identity)
                return {'access_token': access_token}, 200
    ```
    
    2. Set the appropriate environment variable when testing:
       export FLASK_ENV=development
    
    3. Call this endpoint to get an admin token for testing
    """
    
    print(instructions)
    return instructions

# Function to get a JWT token
def get_jwt_token(email, password):
    """
    Get a JWT token for the given credentials.
    
    Args:
        email (str): User email
        password (str): User password
        
    Returns:
        str: JWT token if successful, None otherwise
    """
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": email, "password": password},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            print(f"Failed to get token: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error getting token: {e}")
        return None

# Test admin endpoints using curl commands
def test_admin_endpoints_with_curl(admin_token):
    """
    Test admin endpoints using curl commands.
    
    Args:
        admin_token (str): JWT token for admin user
    """
    print("\n=== Testing Admin Endpoints with curl ===")
    
    # Test commands
    curl_commands = [
        # Create a new user as an admin
        f'curl -X POST "{BASE_URL}/users/" -d \'{{"email": "newuser@example.com", "first_name": "New", "last_name": "User", "password": "Password123!"}}\' -H "Authorization: Bearer {admin_token}" -H "Content-Type: application/json"',
        
        # Get all users to find a user_id to modify
        f'curl -X GET "{BASE_URL}/users/" -H "Authorization: Bearer {admin_token}"',
        
        # Modify another user's data as an admin (replace <user_id> with an actual ID)
        f'curl -X PUT "{BASE_URL}/users/<user_id>" -d \'{{"email": "updatedemail@example.com"}}\' -H "Authorization: Bearer {admin_token}" -H "Content-Type: application/json"',
        
        # Add a new amenity as an admin
        f'curl -X POST "{BASE_URL}/amenities/" -d \'{{"name": "Swimming Pool"}}\' -H "Authorization: Bearer {admin_token}" -H "Content-Type: application/json"',
        
        # Get all amenities to find an amenity_id to modify
        f'curl -X GET "{BASE_URL}/amenities/" -H "Authorization: Bearer {admin_token}"',
        
        # Modify an amenity as an admin (replace <amenity_id> with an actual ID)
        f'curl -X PUT "{BASE_URL}/amenities/<amenity_id>" -d \'{{"name": "Updated Amenity"}}\' -H "Authorization: Bearer {admin_token}" -H "Content-Type: application/json"',
        
        # Test modifying a place that doesn't belong to the admin
        f'curl -X PUT "{BASE_URL}/places/<place_id>" -d \'{{"title": "Admin Modified Place"}}\' -H "Authorization: Bearer {admin_token}" -H "Content-Type: application/json"',
        
        # Test modifying a review that doesn't belong to the admin
        f'curl -X PUT "{BASE_URL}/reviews/<review_id>" -d \'{{"text": "Admin modified review", "rating": 5}}\' -H "Authorization: Bearer {admin_token}" -H "Content-Type: application/json"',
        
        # Test deleting a review that doesn't belong to the admin
        f'curl -X DELETE "{BASE_URL}/reviews/<review_id>" -H "Authorization: Bearer {admin_token}"'
    ]
    
    print("To test the admin endpoints, run the following curl commands:")
    for i, cmd in enumerate(curl_commands, 1):
        print(f"\n{i}. {cmd}")
        
    print("\nNote: Replace <user_id>, <amenity_id>, <place_id>, and <review_id> with actual IDs from your database.")

def main():
    """Main function to run the test script."""
    print("=== HBnB API Admin Endpoints Test ===")
    
    # Present different strategies for testing admin endpoints
    admin_user = create_admin_user_in_db()
    modify_auth_for_testing()
    create_test_endpoint()
    
    # Placeholder for admin token
    admin_token = "YOUR_ADMIN_TOKEN_HERE"
    
    # Test admin endpoints with curl commands
    test_admin_endpoints_with_curl(admin_token)
    
    print("\n=== Test Script Complete ===")
    print("Choose one of the strategies above to obtain an admin token,")
    print("then use the curl commands to test the admin endpoints.")

if __name__ == "__main__":
    main()
