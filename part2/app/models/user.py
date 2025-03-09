from .base_model import BaseModel
import re
from app import bcrypt  # Import bcrypt from the app package

class User(BaseModel):
    """Represents a user in the system.
    
    This class manages user information including identification,
    personal details and contact information.

    Attributes:
        id (str): Unique identifier for the user
        first_name (str): User's first name, max 50 characters
        last_name (str): User's last name, max 50 characters
        email (str): User's email address
        password (str): User's hashed password
        is_admin (bool): Admin status, defaults to False
        created_at (DateTime): Timestamp when the user is created
        updated_at (DateTime): Timestamp when the user is last updated
    """
    def __init__(self, first_name, last_name, email, password=None, is_admin=False, **kwargs):
        """Initialize a new User instance.
        
        Args:
            first_name (str): User's first name
            last_name (str): User's last name 
            email (str): User's email address
            password (str, optional): User's password. Defaults to None.
            is_admin (bool, optional): Admin status. Defaults to False.
        """
        super().__init__(**kwargs)
        
        # Explicit validation with clear error messages
        if not first_name or first_name.strip() == "":
            raise ValueError("First name cannot be empty")
        if len(first_name) > 50:
            raise ValueError("First name must be 50 characters or less")
            
        if not last_name or last_name.strip() == "":
            raise ValueError("Last name cannot be empty")
        if len(last_name) > 50:
            raise ValueError("Last name must be 50 characters or less")
            
        if not email or email.strip() == "":
            raise ValueError("Email cannot be empty")
        
        # Email format validation
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")
        
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.password = None  # Initialize password as None
        self.reviews = []  # List of reviews by this user
        
        # Hash the password if provided
        if password:
            self.hash_password(password)
    
    def hash_password(self, password):
        """Hash the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify if provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
    
    def add_review(self, review):
        """Add a review to the user's reviews"""
        if review not in self.reviews:
            self.reviews.append(review)
    
    def to_dict(self):
        """Convert user instance to dictionary representation."""
        user_dict = super().to_dict()
        user_dict.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        })  # Password not included for security reasons
        return user_dict
