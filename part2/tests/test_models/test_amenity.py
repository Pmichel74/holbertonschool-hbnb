# tests/test_models/test_amenity.py
#!/usr/bin/python3
"""Module de test pour la classe Amenity"""
import unittest
from models.amenity import Amenity
from models.base_model import BaseModel
from datetime import datetime


class TestAmenity(unittest.TestCase):
    """Tests pour la classe Amenity"""

    def setUp(self):
        """Initialisation avant chaque test"""
        self.amenity = Amenity()

    def test_inheritance(self):
        """Test si Amenity hérite bien de BaseModel"""
        self.assertIsInstance(self.amenity, BaseModel)
        self.assertIsInstance(self.amenity, Amenity)

    def test_attributes(self):
        """Test la présence et le type des attributs"""
        self.assertTrue(hasattr(self.amenity, 'id'))
        self.assertTrue(hasattr(self.amenity, 'created_at'))
        self.assertTrue(hasattr(self.amenity, 'updated_at'))
        self.assertTrue(hasattr(self.amenity, 'name'))
        
        # Vérification des types
        self.assertIsInstance(self.amenity.id, str)
        self.assertIsInstance(self.amenity.created_at, datetime)
        self.assertIsInstance(self.amenity.updated_at, datetime)
        self.assertIsInstance(self.amenity.name, str)

    def test_name_default(self):
        """Test si l'attribut name a une valeur par défaut vide"""
        self.assertEqual(self.amenity.name, "")

    def test_str_representation(self):
        """Test la représentation string de l'objet"""
        string = str(self.amenity)
        self.assertIn("[Amenity]", string)
        self.assertIn("id", string)
        self.assertIn("created_at", string)
        self.assertIn("updated_at", string)

    def test_to_dict(self):
        """Test la méthode to_dict"""
        amenity_dict = self.amenity.to_dict()
        
        self.assertIsInstance(amenity_dict, dict)
        self.assertEqual(amenity_dict['__class__'], 'Amenity')
        self.assertIn('id', amenity_dict)
        self.assertIn('created_at', amenity_dict)
        self.assertIn('updated_at', amenity_dict)
        self.assertIsInstance(amenity_dict['created_at'], str)
        self.assertIsInstance(amenity_dict['updated_at'], str)

    def test_init_with_kwargs(self):
        """Test l'initialisation avec des arguments nommés"""
        test_dict = {
            'id': '123',
            'name': 'WiFi',
            'created_at': '2024-01-01T00:00:00.000000',
            'updated_at': '2024-01-01T00:00:00.000000'
        }
        amenity = Amenity(**test_dict)
        
        self.assertEqual(amenity.id, '123')
        self.assertEqual(amenity.name, 'WiFi')
        self.assertIsInstance(amenity.created_at, datetime)
        self.assertIsInstance(amenity.updated_at, datetime)

    def test_save(self):
        """Test la méthode save"""
        old_updated_at = self.amenity.updated_at
        self.amenity.save()
        self.assertNotEqual(old_updated_at, self.amenity.updated_at)

if __name__ == '__main__':
    unittest.main()
