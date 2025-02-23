import unittest
from time import sleep
from datetime import datetime
from app.models.base_model import BaseModel

class TestBaseModel(unittest.TestCase):
    """Test cases for BaseModel class"""

    def test_base_model_init(self):
        """Test BaseModel initialization"""
        base = BaseModel()
        self.assertIsNotNone(base.id)
        self.assertIsNotNone(base.created_at)
        self.assertIsNotNone(base.updated_at)
        self.assertIsInstance(base.created_at, datetime)
        self.assertIsInstance(base.updated_at, datetime)

    def test_base_model_save(self):
        """Test save method updates timestamp"""
        base = BaseModel()
        first_updated_at = base.updated_at
        sleep(0.1)  # Add small delay to ensure different timestamps
        base.save()
        self.assertNotEqual(first_updated_at, base.updated_at)
        self.assertGreater(base.updated_at, first_updated_at)

if __name__ == '__main__':
    unittest.main()
