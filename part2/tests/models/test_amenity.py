import unittest
from app.models.amenity import Amenity

class TestAmenity(unittest.TestCase):
    """Test cases for Amenity class"""

    def test_amenity_creation(self):
        """Test amenity creation"""
        amenity = Amenity(name="Wi-Fi")
        self.assertEqual(amenity.name, "Wi-Fi")

    def test_invalid_name(self):
        """Test amenity creation with invalid name"""
        with self.assertRaises(ValueError):
            Amenity(name="A" * 51)  # Name too long

if __name__ == '__main__':
    unittest.main()
