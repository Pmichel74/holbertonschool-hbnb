import unittest
import json
from app import create_app

class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        
        # Créer d'abord un utilisateur pour les tests
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "test.user@example.com"
        })
        user_data = json.loads(user_response.data)
        self.user_id = user_data['id']
        
        # Créer ensuite un place pour les tests
        place_response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A place for testing",
            "price": 100.0,
            "latitude": 48.858844,
            "longitude": 2.294351,
            "owner_id": self.user_id,
            "amenities": []
        })
        place_data = json.loads(place_response.data)
        self.place_id = place_data['id']
        
        # Review de test par défaut
        self.test_review_data = {
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        }

    def test_create_review_valid(self):
        """Test creating a valid review"""
        response = self.client.post('/api/v1/reviews/', json=self.test_review_data)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['text'], self.test_review_data['text'])
        self.assertEqual(data['rating'], self.test_review_data['rating'])
        self.assertEqual(data['user_id'], self.test_review_data['user_id'])
        self.assertEqual(data['place_id'], self.test_review_data['place_id'])

    def test_create_review_empty_text(self):
        """Test creating a review with empty text"""
        invalid_data = dict(self.test_review_data)
        invalid_data['text'] = ""
        response = self.client.post('/api/v1/reviews/', json=invalid_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('message', data)

    def test_create_review_invalid_rating(self):
        """Test creating a review with invalid rating"""
        # Test with rating too high
        invalid_data = dict(self.test_review_data)
        invalid_data['rating'] = 6
        response = self.client.post('/api/v1/reviews/', json=invalid_data)
        self.assertEqual(response.status_code, 400)
        
        # Test with rating too low
        invalid_data['rating'] = 0
        response = self.client.post('/api/v1/reviews/', json=invalid_data)
        self.assertEqual(response.status_code, 400)
        
        # Test with non-integer rating
        invalid_data['rating'] = "not-a-number"
        response = self.client.post('/api/v1/reviews/', json=invalid_data)
        self.assertEqual(response.status_code, 400)

    def test_create_review_nonexistent_user(self):
        """Test creating a review with non-existent user"""
        invalid_data = dict(self.test_review_data)
        invalid_data['user_id'] = "non-existent-user-id"
        response = self.client.post('/api/v1/reviews/', json=invalid_data)
        self.assertEqual(response.status_code, 400)