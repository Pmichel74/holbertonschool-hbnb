import unittest
from app.models.place import Place
from app.models.user import User
from app.models.review import Review

class TestPlace(unittest.TestCase):
    """Test cases for Place class"""

    def setUp(self):
        """Set up test fixtures"""
        self.owner = User(
            first_name="Alice",
            last_name="Smith",
            email="alice@example.com"
        )
        self.place = Place(
            title="Cozy Apartment",
            description="A nice place to stay",
            price=100,
            latitude=37.7749,
            longitude=-122.4194,
            owner=self.owner
        )

    def test_place_creation(self):
        """Test place creation with relationships"""
        review = Review(
            text="Great stay!",
            rating=5,
            place=self.place,
            user=self.owner
        )
        self.place.add_review(review)

        self.assertEqual(self.place.title, "Cozy Apartment")
        self.assertEqual(self.place.price, 100)
        self.assertEqual(len(self.place.reviews), 1)
        self.assertEqual(self.place.reviews[0].text, "Great stay!")

if __name__ == '__main__':
    unittest.main()
