import unittest
import json
from app import create_app

class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        
        # Créer d'abord un utilisateur pour les tests
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "Owner",
            "email": "test.owner@example.com"
        })
        user_data = json.loads(user_response.data)
        self.user_id = user_data['id']
        
        # Créer également une commodité pour les tests
        amenity_response = self.client.post('/api/v1/amenities/', json={
            "name": "Test Amenity"
        })
        amenity_data = json.loads(amenity_response.data)
        self.amenity_id = amenity_data['id']
        
        # Données de test pour les places
        self.test_place_data = {
            "title": "Cozy Apartment",
            "description": "A beautiful place in the heart of the city",
            "price": 150.0,
            "latitude": 48.856614,
            "longitude": 2.352222,
            "owner_id": self.user_id,
            "amenities": [self.amenity_id]
        }

    def test_create_place_valid(self):
        """Test creating a valid place"""
        response = self.client.post('/api/v1/places/', json=self.test_place_data)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['title'], self.test_place_data['title'])
        self.assertEqual(data['description'], self.test_place_data['description'])
        self.assertEqual(data['price'], self.test_place_data['price'])
        self.assertEqual(data['latitude'], self.test_place_data['latitude'])
        self.assertEqual(data['longitude'], self.test_place_data['longitude'])
        self.assertEqual(data['owner_id'], self.test_place_data['owner_id'])
        self.assertEqual(len(data['amenities']), 1)

    def test_create_place_empty_title(self):
        """Test creating a place with empty title"""
        invalid_data = dict(self.test_place_data)
        invalid_data['title'] = ""
        response = self.client.post('/api/v1/places/', json=invalid_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('message', data)

    def test_create_place_negative_price(self):
        """Test creating a place with negative price"""
        invalid_data = dict(self.test_place_data)
        invalid_data['price'] = -50.0
        response = self.client.post('/api/v1/places/', json=invalid_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('message', data)

    def test_create_place_invalid_latitude(self):
        """Test creating a place with invalid latitude"""
        # Test with latitude too high
        invalid_data = dict(self.test_place_data)
        invalid_data['latitude'] = 100.0
        response = self.client.post('/api/v1/places/', json=invalid_data)
        self.assertEqual(response.status_code, 400)
        
        # Test with latitude too low
        invalid_data['latitude'] = -100.0
        response = self.client.post('/api/v1/places/', json=invalid_data)
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_longitude(self):
        """Test creating a place with invalid longitude"""
        # Test with longitude too high
        invalid_data = dict(self.test_place_data)
        invalid_data['longitude'] = 200.0
        response = self.client.post('/api/v1/places/', json=invalid_data)
        self.assertEqual(response.status_code, 400)
        
        # Test with longitude too low
        invalid_data['longitude'] = -200.0
        response = self.client.post('/api/v1/places/', json=invalid_data)
        self.assertEqual(response.status_code, 400)

    def test_create_place_nonexistent_owner(self):
        """Test creating a place with non-existent owner"""
        invalid_data = dict(self.test_place_data)
        invalid_data['owner_id'] = "non-existent-owner-id"
        response = self.client.post('/api/v1/places/', json=invalid_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('message', data)

    def test_create_place_nonexistent_amenity(self):
        """Test creating a place with non-existent amenity"""
        invalid_data = dict(self.test_place_data)
        invalid_data['amenities'] = ["non-existent-amenity-id"]
        response = self.client.post('/api/v1/places/', json=invalid_data)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('message', data)

    def test_get_places(self):
        """Test getting all places"""
        # D'abord créer un place
        self.client.post('/api/v1/places/', json=self.test_place_data)
        
        # Récupérer tous les places
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_get_place_by_id(self):
        """Test getting a place by ID"""
        # D'abord créer un place
        create_response = self.client.post('/api/v1/places/', json=self.test_place_data)
        create_data = json.loads(create_response.data)
        place_id = create_data['id']
        
        # Récupérer le place par ID
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], place_id)
        self.assertEqual(data['title'], self.test_place_data['title'])
        
        # Vérifier que owner contient les détails de l'utilisateur
        self.assertIn('owner', data)
        self.assertEqual(data['owner']['id'], self.user_id)
        
        # Vérifier que les commodités sont incluses
        self.assertIn('amenities', data)
        self.assertEqual(len(data['amenities']), 1)
        self.assertEqual(data['amenities'][0]['id'], self.amenity_id)

    def test_get_nonexistent_place(self):
        """Test getting a place that doesn't exist"""
        response = self.client.get('/api/v1/places/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_update_place(self):
        """Test updating a place"""
        # D'abord créer un place
        create_response = self.client.post('/api/v1/places/', json=self.test_place_data)
        create_data = json.loads(create_response.data)
        place_id = create_data['id']
        
        # Mettre à jour le place
        update_data = {
            "title": "Updated Place Title",
            "description": "Updated description",
            "price": 200.0
        }
        response = self.client.put(f'/api/v1/places/{place_id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], update_data['title'])
        self.assertEqual(data['description'], update_data['description'])
        self.assertEqual(data['price'], update_data['price'])
        
        # Vérifier que l'owner_id n'a pas changé
        self.assertEqual(data['owner_id'], self.test_place_data['owner_id'])

    def test_update_place_invalid_data(self):
        """Test updating a place with invalid data"""
        # D'abord créer un place
        create_response = self.client.post('/api/v1/places/', json=self.test_place_data)
        create_data = json.loads(create_response.data)
        place_id = create_data['id']
        
        # Essayer de mettre à jour avec des données invalides
        update_data = {
            "latitude": 100.0  # Latitude invalide
        }
        response = self.client.put(f'/api/v1/places/{place_id}', json=update_data)
        self.assertEqual(response.status_code, 400)

    def test_update_nonexistent_place(self):
        """Test updating a non-existent place"""
        update_data = {
            "title": "Updated Place"
        }
        response = self.client.put('/api/v1/places/nonexistent-id', json=update_data)
        self.assertEqual(response.status_code, 404)

    def test_place_with_amenities(self):
        """Test creating and retrieving a place with multiple amenities"""
        # Créer une deuxième commodité
        second_amenity_response = self.client.post('/api/v1/amenities/', json={
            "name": "Second Amenity"
        })
        second_amenity_data = json.loads(second_amenity_response.data)
        second_amenity_id = second_amenity_data['id']
        
        # Créer un place avec deux commodités
        place_data = dict(self.test_place_data)
        place_data['amenities'] = [self.amenity_id, second_amenity_id]
        
        create_response = self.client.post('/api/v1/places/', json=place_data)
        self.assertEqual(create_response.status_code, 201)
        create_data = json.loads(create_response.data)
        place_id = create_data['id']
        
        # Récupérer le place et vérifier ses commodités
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['amenities']), 2)
        
        # Vérifier que les deux commodités sont présentes
        amenity_ids = [amenity['id'] for amenity in data['amenities']]
        self.assertIn(self.amenity_id, amenity_ids)
        self.assertIn(second_amenity_id, amenity_ids)


if __name__ == '__main__':
    unittest.main()