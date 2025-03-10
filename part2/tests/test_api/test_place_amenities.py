# tests/test_api/test_place_amenities.py
import unittest
import json
from unittest.mock import patch, Mock
from api import create_app

class TestPlaceAmenitiesAPI(unittest.TestCase):
    def setUp(self):
        """Initialise l'environnement de test"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.test_place = {
            "id": "test-place-id",
            "name": "Test Place",
            "amenities": []
        }

    @patch('models.storage.facade')
    def test_get_place_amenities(self, mock_facade):
        """Test GET /places/<place_id>/amenities"""
        # Configure le mock
        mock_place = Mock()
        mock_amenity = Mock()
        mock_amenity.to_dict.return_value = {"id": "test-amenity-id", "name": "WiFi"}
        mock_place.amenities = [mock_amenity]
        mock_facade.get_place.return_value = mock_place
        
        # Fait la requête
        response = self.client.get('/api/v1/places/test-place-id/amenities')
        
        # Vérifie les résultats
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'WiFi')

    @patch('models.storage.facade')
    @patch('auth.auth.auth_required')
    def test_link_amenity_to_place(self, mock_auth_required, mock_facade):
        """Test POST /places/<place_id>/amenities/<amenity_id>"""
        # Configure les mocks
        mock_auth_required.return_value = lambda x: x
        mock_place = Mock()
        mock_place.to_dict.return_value = self.test_place
        mock_facade.add_amenity_to_place.return_value = None
        mock_facade.get_place.return_value = mock_place
        
        # Fait la requête
        response = self.client.post('/api/v1/places/test-place-id/amenities/test-amenity-id')
        
        # Vérifie les résultats
        self.assertEqual(response.status_code, 201)

    @patch('models.storage.facade')
    @patch('auth.auth.auth_required')
    def test_unlink_amenity_from_place(self, mock_auth_required, mock_facade):
        """Test DELETE /places/<place_id>/amenities/<amenity_id>"""
        # Configure les mocks
        mock_auth_required.return_value = lambda x: x
        
        # Fait la requête
        response = self.client.delete('/api/v1/places/test-place-id/amenities/test-amenity-id')
        
        # Vérifie les résultats
        self.assertEqual(response.status_code, 200)
