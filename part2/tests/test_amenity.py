import unittest
import json
from app import create_app
from app.db import db

class AmenityApiTestCase(unittest.TestCase):
    """Test case for the Amenity API endpoints"""

    def setUp(self):
        """Set up the test client and database"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.amenity_data = {'name': 'Wi-Fi'}

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Tear down test database"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_amenity_not_found(self):
        """Test retrieving an amenity that does not exist"""
        res = self.client.get('/api/v1/amenities/invalid-id')
        self.assertEqual(res.status_code, 404)

    def test_create_amenity(self):
        """Test creating a new amenity"""
        res = self.client.post('/api/v1/amenities/',
                               data=json.dumps(self.amenity_data),
                               content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertIn('name', res.get_json())
        self.assertEqual(res.get_json()['name'], 'Wi-Fi')

    def test_update_amenity_not_found(self):
        """Test updating a non-existing amenity"""
        res = self.client.put('/api/v1/amenities/invalid-id',
                              data=json.dumps(self.amenity_data),
                              content_type='application/json')
        self.assertEqual(res.status_code, 404)

    def test_update_amenity_invalid_data(self):
        """Test updating an amenity with invalid data"""
        res = self.client.put('/api/v1/amenities/valid-id',
                              data=json.dumps({}),  # Envoi de données vides
                              content_type='application/json')
        self.assertEqual(res.status_code, 400)

if __name__ == '__main__':
    unittest.main()
