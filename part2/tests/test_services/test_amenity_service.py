# tests/test_services/test_amenity_service.py
import unittest
from unittest.mock import Mock
from services.amenity_service import AmenityService
from models.amenity import Amenity

class TestAmenityService(unittest.TestCase):
    def setUp(self):
        """Initialise l'environnement de test"""
        self.storage = Mock()
        self.service = AmenityService(self.storage)
        
        # Mock d'un amenity pour les tests
        self.test_amenity = Amenity(
            id="test-amenity-id",
            name="WiFi"
        )

    def test_create_amenity(self):
        """Test la création d'un amenity"""
        # Prépare les données
        data = {"name": "WiFi"}
        
        # Configure le mock
        self.storage.new = Mock()
        self.storage.save = Mock()
        
        # Exécute la méthode
        result = self.service.create(data)
        
        # Vérifie les résultats
        self.storage.new.assert_called_once()
        self.storage.save.assert_called_once()
        self.assertEqual(result.name, "WiFi")

    def test_create_amenity_without_name(self):
        """Test la création d'un amenity sans nom"""
        with self.assertRaises(ValueError):
            self.service.create({})

    def test_get_all_amenities(self):
        """Test la récupération de tous les amenities"""
        # Configure le mock
        self.storage.all.return_value = {
            "amenity1": self.test_amenity
        }
        
        # Exécute la méthode
        result = self.service.get_all()
        
        # Vérifie les résultats
        self.storage.all.assert_called_once_with(Amenity)
        self.assertEqual(len(list(result)), 1)

    def test_get_amenity(self):
        """Test la récupération d'un amenity spécifique"""
        # Configure le mock
        self.storage.get.return_value = self.test_amenity
        
        # Exécute la méthode
        result = self.service.get("test-amenity-id")
        
        # Vérifie les résultats
        self.storage.get.assert_called_once_with(Amenity, "test-amenity-id")
        self.assertEqual(result.id, "test-amenity-id")

    def test_update_amenity(self):
        """Test la mise à jour d'un amenity"""
        # Configure le mock
        self.storage.get.return_value = self.test_amenity
        self.storage.save = Mock()
        
        # Exécute la méthode
        result = self.service.update("test-amenity-id", {"name": "5G WiFi"})
        
        # Vérifie les résultats
        self.assertEqual(result.name, "5G WiFi")
        self.storage.save.assert_called_once()

    def test_delete_amenity(self):
        """Test la suppression d'un amenity"""
        # Configure le mock
        self.storage.get.return_value = self.test_amenity
        self.storage.delete = Mock()
        self.storage.save = Mock()
        
        # Exécute la méthode
        self.service.delete("test-amenity-id")
        
        # Vérifie les résultats
        self.storage.delete.assert_called_once_with(self.test_amenity)
        self.storage.save.assert_called_once()
