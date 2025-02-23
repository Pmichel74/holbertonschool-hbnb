# models/user.py
from .base_model import BaseModel
import re

class User(BaseModel):
    """Class representing a user"""

    def __init__(self, first_name: str, last_name: str, email: str, is_admin: bool = False):
        """
        Initialize a new user
        Args:
            first_name (str): User's first name
            last_name (str): User's last name
            email (str): User's email
            is_admin (bool): Administrator status (default: False)
        """
        super().__init__()
        self.validate_name(first_name, "first_name")
        self.validate_name(last_name, "last_name")
        self.validate_email(email)
        
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []  # List of places owned by the user
        self.reviews = []  # List of reviews written by the user

    @staticmethod
    def validate_name(name: str, field: str):
        """Validate the name format"""
        if not name or len(name) > 50:
            raise ValueError(f"{field} must be between 1 and 50 characters")

    @staticmethod
    def validate_email(email: str):
        """Validate email format"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")

    def add_place(self, place):
        """Add a place to the user"""
        self.places.append(place)

    def add_review(self, review):
        """Add a review to the user"""
        self.reviews.append(review)

    def to_dict(self):
        """Convert user to dictionary"""
        user_dict = super().to_dict()
        user_dict.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        })
        return user_dict
