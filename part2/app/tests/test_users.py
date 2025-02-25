# app/tests/test_users.py
import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app().test_client()
        self.app.testing = True

    def test_update_user_success(self):
        new_data = {"first_name": "Updated Name", "last_name": "Updated Last", "email": "updated@example.com"}
        response = self.app.put('/api/v1/users/1', json=new_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Updated Name', response.json['first_name'])
        self.assertIn('Updated Last', response.json['last_name'])
        self.assertIn('updated@example.com', response.json['email'])

    def test_update_user_not_found(self):
        new_data = {"first_name": "Nonexistent", "last_name": "User", "email": "noexistent@example.com"}
        response = self.app.put('/api/v1/users/9999', json=new_data)
        self.assertEqual(response.status_code, 404)

    def test_update_user_invalid_data(self):
        new_data = {"first_name": "", "last_name": "", "email": ""}
        response = self.app.put('/api/v1/users/1', json=new_data)
        self.assertEqual(response.status_code, 400)

    def test_get_all_users(self):
        response = self.app.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json) > 0)
