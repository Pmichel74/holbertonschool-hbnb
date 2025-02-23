import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.user import User

def test_user_creation():
    """
    Test User creation with valid data
    
    This test verifies that:
    - A User instance is created successfully
    - All attributes are set correctly
    - Default values are properly initialized
    """
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False
    print("User creation test passed!")

if __name__ == '__main__':
    test_user_creation()