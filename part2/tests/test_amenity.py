import os
import sys
import unittest
import json

# Add project path to system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.amenity import Amenity
from hbnb.part2.api.v1.app import app
from models import storage

def test_amenity_creation():
    """
    Test Amenity creation with valid data
    
    This test verifies that:
    - An Amenity instance is created successfully
    - The name attribute is set correctly
    """
    amenity = Amenity(name="Wi-Fi")
    assert amenity.name == "Wi-Fi"
    print("Amenity creation test passed!")

class TestAmenityAPI(unittest.TestCase):
    """Test cases for the Amenity API endpoints"""

    @classmethod
    def setUpClass(cls):
        """Set up the test client"""
        cls.client = app.test_client()
        cls.client.testing = True

    def setUp(self):
        """Clean up the storage before each test"""
        storage._FileStorage__objects = {}  # Reset storage
        storage.save()

    def test_get_amenities_empty(self):
        """Test GET /api/v1/amenities/ when no amenities exist"""
        response = self.client.get("/api/v1/amenities/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_post_amenity(self):
        """Test POST /api/v1/amenities/ with valid data"""
        data = {"name": "Pool"}
        response = self.client.post(
            "/api/v1/amenities/", 
            data=json.dumps(data), 
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)
        self.assertEqual(response.json["name"], "Pool")

    def test_get_amenities_after_post(self):
        """Test GET /api/v1/amenities/ after adding an amenity"""
        # Create an amenity
        self.client.post(
            "/api/v1/amenities/", 
            data=json.dumps({"name": "Gym"}), 
            content_type="application/json"
        )

        # Check if the amenity is in the list
        response = self.client.get("/api/v1/amenities/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]["name"], "Gym")

    def test_post_amenity_missing_name(self):
        """Test POST /api/v1/amenities/ with missing 'name'"""
        response = self.client.post(
            "/api/v1/amenities/", 
            data=json.dumps({}), 
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Missing 'name' field"})

if __name__ == "__main__":
    test_amenity_creation()  # Run existing test
    unittest.main()
