import unittest
import json
from app import create_app

class TestAmenityEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        
        # Données de test pour les commodités
        self.test_amenity_data = {
            "name": "WiFi"
        }

    def test_create_amenity_valid(self):
        """Test creating a valid amenity"""
        response = self.client.post('/api/v1/amenities/', json=self.test_amenity_data)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['name'], self.test_amenity_data['name'])

    def test_create_amenity_empty_name(self):
        """Test creating an amenity with empty name"""
        invalid_data = {"name": ""}
        response = self.client.post('/api/v1/amenities/', json=invalid_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('message', data)

    def test_create_amenity_missing_name(self):
        """Test creating an amenity with missing name field"""
        invalid_data = {}
        response = self.client.post('/api/v1/amenities/', json=invalid_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('message', data)

    def test_get_amenities(self):
        """Test getting all amenities"""
        # D'abord créer une commodité
        self.client.post('/api/v1/amenities/', json=self.test_amenity_data)
        
        # Récupérer toutes les commodités
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_get_amenity_by_id(self):
        """Test getting an amenity by ID"""
        # D'abord créer une commodité
        create_response = self.client.post('/api/v1/amenities/', json=self.test_amenity_data)
        create_data = json.loads(create_response.data)
        amenity_id = create_data['id']
        
        # Récupérer la commodité par ID
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], amenity_id)
        self.assertEqual(data['name'], self.test_amenity_data['name'])

    def test_get_nonexistent_amenity(self):
        """Test getting an amenity that doesn't exist"""
        response = self.client.get('/api/v1/amenities/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_update_amenity(self):
        """Test updating an amenity"""
        # D'abord créer une commodité
        create_response = self.client.post('/api/v1/amenities/', json=self.test_amenity_data)
        create_data = json.loads(create_response.data)
        amenity_id = create_data['id']
        
        # Mettre à jour la commodité
        update_data = {
            "name": "High-Speed WiFi"
        }
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], update_data['name'])
        self.assertEqual(data['id'], amenity_id)

    def test_update_amenity_empty_name(self):
        """Test updating an amenity with empty name"""
        # D'abord créer une commodité
        create_response = self.client.post('/api/v1/amenities/', json=self.test_amenity_data)
        create_data = json.loads(create_response.data)
        amenity_id = create_data['id']
        
        # Essayer de mettre à jour avec un nom vide
        update_data = {
            "name": ""
        }
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json=update_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('message', data)

    def test_update_nonexistent_amenity(self):
        """Test updating a non-existent amenity"""
        update_data = {
            "name": "Updated Amenity"
        }
        response = self.client.put('/api/v1/amenities/nonexistent-id', json=update_data)
        self.assertEqual(response.status_code, 404)

    def test_create_duplicate_amenity(self):
        """Test creating amenities with the same name (should be allowed)"""
        # Créer la première commodité
        first_response = self.client.post('/api/v1/amenities/', json=self.test_amenity_data)
        self.assertEqual(first_response.status_code, 201)
        
        # Créer une deuxième commodité avec le même nom
        second_response = self.client.post('/api/v1/amenities/', json=self.test_amenity_data)
        self.assertEqual(second_response.status_code, 201)
        
        # Vérifier que les IDs sont différents
        first_data = json.loads(first_response.data)
        second_data = json.loads(second_response.data)
        self.assertNotEqual(first_data['id'], second_data['id'])


if __name__ == '__main__':
    unittest.main()