import os
import sys
import unittest
import json

# Add project path to system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.user import User
from app import app
from models import storage

def test_user_creation():
    """
    Test User creation with valid data

    This test verifies that:
    - A User instance is created successfully
    - All attributes are set correctly
    - Default values are properly initialized
    """
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False
    print("User creation test passed!")

class TestUserAPI(unittest.TestCase):
    """Test cases for User API"""

    @classmethod
    def setUpClass(cls):
        """Set up the test client and test data"""
        cls.client = app.test_client()
        cls.user = User(id="1234", email="test@example.com", password="password123")
        storage.new(cls.user)
        storage.save()

    @classmethod
    def tearDownClass(cls):
        """Clean up test data"""
        storage.delete(cls.user)
        storage.save()

    def test_get_users(self):
        """Test retrieving all users"""
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_get_user_valid(self):
        """Test retrieving a valid user"""
        response = self.client.get(f'/api/v1/users/{self.user.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], self.user.id)
        self.assertEqual(data['email'], self.user.email)

    def test_get_user_invalid(self):
        """Test retrieving a non-existent user"""
        response = self.client.get('/api/v1/users/invalid_id')
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    test_user_creation()  # Run existing test
    unittest.main()
