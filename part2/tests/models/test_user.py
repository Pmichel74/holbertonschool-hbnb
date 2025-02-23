import unittest
from app.models.user import User

class TestUser(unittest.TestCase):
    """Test cases for User class"""

    def setUp(self):
        """Set up test cases"""
        self.user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com'
        }
        self.user = User(**self.user_data)

    def test_user_creation(self):
        """Test user creation with valid data"""
        self.assertEqual(self.user.first_name, self.user_data['first_name'])
        self.assertEqual(self.user.last_name, self.user_data['last_name'])
        self.assertEqual(self.user.email, self.user_data['email'])
        self.assertFalse(self.user.is_admin)

    def test_invalid_email(self):
        """Test user creation with invalid email"""
        with self.assertRaises(ValueError):
            User(first_name='John', last_name='Doe', email='invalid-email')

if __name__ == '__main__':
    unittest.main()
