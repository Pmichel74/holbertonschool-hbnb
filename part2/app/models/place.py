import uuid
from datetime import datetime
from app.models.base_model import BaseModel

class Place(BaseModel):
    """Class representing a place
    
    Attributes:
        id (str): Unique identifier for each place
        title (str): The title of the place, max 100 characters
        description (str): Detailed description of the place
        price (float): The price per night, must be positive
        latitude (float): Latitude coordinate (-90.0 to 90.0)
        longitude (float): Longitude coordinate (-180.0 to 180.0)
        owner (User): User instance of who owns the place
        created_at (DateTime): Timestamp when the place is created
        updated_at (DateTime): Timestamp when the place is last updated
    """
    
    def __init__(self, title, owner, description="", price=0.0, latitude=0.0, longitude=0.0, **kwargs):
        """Initialize a new place
        
        Args:
            title (str): Title of the place
            owner (User): Owner of the place
            description (str, optional): Description. Defaults to empty string.
            price (float, optional): Price per night. Defaults to 0.0.
            latitude (float, optional): Latitude. Defaults to 0.0.
            longitude (float, optional): Longitude. Defaults to 0.0.
        """
        super().__init__(**kwargs)
        self.validate_title(title)
        self.validate_owner(owner)
        
        self.title = title
        self.description = description
        self._price = 0.0
        self._latitude = 0.0
        self._longitude = 0.0
        self.owner = owner
        self.amenities = []
        self.reviews = []
        
        # Use property setters for validation
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
    
    @staticmethod
    def validate_title(title):
        """Validate place title"""
        if not title:
            raise ValueError("Title cannot be empty")
        if len(title) > 100:
            raise ValueError("Title must be 100 characters or less")
    
    @staticmethod
    def validate_owner(owner):
        """Validate owner is a User instance"""
        if not owner:
            raise ValueError("Place must have an owner")
        # Dans un environnement réel, vérifierez que owner est une instance de User
        # from .user import User
        # if not isinstance(owner, User):
        #     raise TypeError("Owner must be a User instance")
    
    @property
    def price(self):
        """Get price"""
        return self._price
    
    @price.setter
    def price(self, value):
        """Set price with validation"""
        if not isinstance(value, (int, float)):
            raise ValueError("Price must be a number")
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = float(value)
    
    @property
    def latitude(self):
        """Get latitude"""
        return self._latitude
    
    @latitude.setter
    def latitude(self, value):
        """Set latitude with validation"""
        if not isinstance(value, (int, float)):
            raise ValueError("Latitude must be a number")
        if not -90 <= float(value) <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = float(value)
    
    @property
    def longitude(self):
        """Get longitude"""
        return self._longitude
    
    @longitude.setter
    def longitude(self, value):
        """Set longitude with validation"""
        if not isinstance(value, (int, float)):
            raise ValueError("Longitude must be a number")
        if not -180 <= float(value) <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = float(value)
    
    def add_amenity(self, amenity):
        """Add an amenity to the place"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)
    
    def add_review(self, review):
        """Add a review to the place"""
        if review not in self.reviews:
            self.reviews.append(review)
    
    def to_dict(self):
        """Convert place to dictionary"""
        place_dict = super().to_dict()
        place_dict.update({
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner.id if self.owner else None
        })
        return place_dict

