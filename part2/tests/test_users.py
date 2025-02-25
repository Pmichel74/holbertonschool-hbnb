import unittest
import json
from app import create_app
from app.services.facade import facade


class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        """Initialize test environment"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        # Clear any existing users
        facade.users = {}
        # Define headers
        self.headers = {'Content-Type': 'application/json'}

    def tearDown(self):
        """Clean up after tests"""
        facade.users = {}
        self.app_context.pop()

    def test_create_user_success(self):
        """Test successful user creation"""
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123'
        }

        response = self.client.post(
            '/api/v1/users/',
            json=data,
            headers={'Content-Type': 'application/json'}
        )

        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data.decode()}")
        
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertIn('id', response_data)
        self.assertEqual(response_data['email'], data['email'])
        self.assertEqual(response_data['first_name'], data['first_name'])
        self.assertEqual(response_data['last_name'], data['last_name'])
        self.assertNotIn('password', response_data)

    def test_create_user_duplicate_email(self):
        """Test la création d'un utilisateur avec un email déjà existant"""
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123'
        }
        
        # Première création
        response1 = self.client.post(
            '/api/v1/users/',
            json=data,
            headers=self.headers
        )
        self.assertEqual(response1.status_code, 201)
        
        # Tentative de création avec le même email
        response2 = self.client.post(
            '/api/v1/users/',
            json=data,
            headers=self.headers
        )
        self.assertEqual(response2.status_code, 400)

    def test_create_user_missing_field(self):
        """Test création utilisateur avec champ manquant"""
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            # email manquant
            'password': 'password123'
        }
        
        response = self.client.post(
            '/api/v1/users/',
            json=data,
            headers=self.headers
        )
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
