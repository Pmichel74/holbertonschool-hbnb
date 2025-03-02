import uuid
from datetime import datetime
from .base_model import BaseModel
from .user import User

class Place(BaseModel):
    """Class representing a rental place
    
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
        """Initialize a new Place
        
        Args:
            title (str): Place title (required)
            owner (User): User instance of who owns the place
            description (str): Detailed description of the place
            price (float): Price per night
            latitude (float): Geographic latitude
            longitude (float): Geographic longitude
        """
        super().__init__(**kwargs)
        
        # Validate required fields
        self.validate_title(title)
        self.validate_owner(owner)
        
        # Set properties
        self.title = title
        self._owner = owner  # Store the actual User instance
        self.description = description
        self.price = price  # Will use the setter with validation
        self.latitude = latitude
        self.longitude = longitude
        self.amenities = []
        self.reviews = []
    
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
            
        # Ensure owner is a User instance
        from .user import User
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User instance")
    
    @property
    def owner(self):
        """Get the owner User instance"""
        return self._owner
    
    @owner.setter
    def owner(self, user):
        """Set the owner with validation"""
        self.validate_owner(user)
        self._owner = user
    
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
            'owner_id': self.owner.id if self.owner else None,
            'amenities': [amenity.id for amenity in self.amenities] if self.amenities else []
        })
        return place_dict

