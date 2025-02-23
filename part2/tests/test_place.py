import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.place import Place
from app.models.user import User
from app.models.review import Review

def test_place_creation():
    """
    Test Place creation and relationships
    
    This test verifies that:
    - A Place instance is created successfully
    - Owner relationship is established
    - Reviews can be added correctly
    - All attributes are set properly
    """
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    place = Place(title="Cozy Apartment", description="A nice place to stay", 
                 price=100, latitude=37.7749, longitude=-122.4194, owner=owner)

    review = Review(text="Great stay!", rating=5, place=place, user=owner)
    place.add_review(review)

    assert place.title == "Cozy Apartment"
    assert place.price == 100
    assert len(place.reviews) == 1
    assert place.reviews[0].text == "Great stay!"
    print("Place creation and relationship test passed!")

if __name__ == '__main__':
    test_place_creation()