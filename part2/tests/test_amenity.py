import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.amenity import Amenity

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

if __name__ == '__main__':
    test_amenity_creation()