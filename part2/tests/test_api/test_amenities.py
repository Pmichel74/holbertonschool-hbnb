# tests/test_api/test_amenities.py
import unittest
import json
from unittest.mock import patch, Mock
from api import create_app
from models import storage
from models.amenity import Amenity

class TestAmenitiesAPI(unittest.TestCase):
    def setUp(self):
        """Initialise l'environnement de test"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.test_amenity = {
            "id": "test-amenity-id",
            "name": "WiFi",
            "created_at": "2024-03-09T14:15:00",
            "updated_at": "2024-03-09T14:15:00"
        }

    @patch('models.storage.facade')
    def test_get_amenities(self, mock_facade):
        """Test GET /amenities"""
        # Configure le mock
        mock_amenity = Mock()
        mock_amenity.to_dict.return_value = self.test_amenity
        mock_facade.get_amenities.return_value = [mock_amenity]
        
        # Fait la requête
        response = self.client.get('/api/v1/amenities')
        
        # Vérifie les résultats
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'WiFi')

    @patch('models.storage.facade')
    def test_get_amenity(self, mock_facade):
        """Test GET /amenities/<amenity_id>"""
        # Configure le mock
        mock_amenity = Mock()
        mock_amenity.to_dict.return_value = self.test_amenity
        mock_facade.get_amenity.return_value = mock_amenity
        
        # Fait la requête
        response = self.client.get('/api/v1/amenities/test-amenity-id')
        
        # Vérifie les résultats
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'WiFi')

    @patch('models.storage.facade')
    @patch('auth.auth.admin_required')
    def test_create_amenity(self, mock_admin_required, mock_facade):
        """Test POST /amenities"""
        # Configure les mocks
        mock_admin_required.return_value = lambda x: x
        mock_amenity = Mock()
        mock_amenity.to_dict.return_value = self.test_amenity
        mock_facade.create_amenity.return_value = mock_amenity
        
        # Fait la requête
        response = self.client.post(
            '/api/v1/amenities',
            json={"name": "WiFi"}
        )
        
        # Vérifie les résultats
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'WiFi')

    @patch('models.storage.facade')
    @patch('auth.auth.admin_required')
    def test_update_amenity(self, mock_admin_required, mock_facade):
        """Test PUT /amenities/<amenity_id>"""
        # Configure les mocks
        mock_admin_required.return_value = lambda x: x
        mock_amenity = Mock()
        mock_amenity.to_dict.return_value = {**self.test_amenity, "name": "5G WiFi"}
        mock_facade.update_amenity.return_value = mock_amenity
        
        # Fait la requête
        response = self.client.put(
            '/api/v1/amenities/test-amenity-id',
            json={"name": "5G WiFi"}
        )
        
        # Vérifie les résultats
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], '5G WiFi')

    @patch('models.storage.facade')
    @patch('auth.auth.admin_required')
    def test_delete_amenity(self, mock_admin_required, mock_facade):
        """Test DELETE /amenities/<amenity_id>"""
        # Configure les mocks
        mock_admin_required.return_value = lambda x: x
        
        # Fait la requête
        response = self.client.delete('/api/v1/amenities/test-amenity-id')
        
        # Vérifie les résultats
        self.assertEqual(response.status_code, 200)
