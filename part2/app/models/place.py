# models/place.py
from .base_model import BaseModel

class Place(BaseModel):
    """Class representing a place"""

    def __init__(self, title: str, description: str, price: float, 
                 latitude: float, longitude: float, owner):
        """
        Initialize a new place
        Args:
            title (str): Place title
            description (str): Place description
            price (float): Price per night
            latitude (float): Latitude
            longitude (float): Longitude
            owner (User): Place owner
        """
        super().__init__()
        self.validate_title(title)
        self.validate_coordinates(latitude, longitude)
        self.validate_price(price)

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # Initialize empty reviews list
        self.amenities = []

    @staticmethod
    def validate_title(title: str):
        """Validate title"""
        if not title or len(title) > 100:
            raise ValueError("Title must be between 1 and 100 characters")

    @staticmethod
    def validate_coordinates(lat: float, lon: float):
        """Validate geographic coordinates"""
        if not -90 <= lat <= 90:
            raise ValueError("Invalid latitude")
        if not -180 <= lon <= 180:
            raise ValueError("Invalid longitude")

    @staticmethod
    def validate_price(price: float):
        """Validate price"""
        if price < 0:
            raise ValueError("Price cannot be negative")

    def add_review(self, review):
        """Add a review to the place"""
        if review not in self.reviews:  # Avoid duplicates
            self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def to_dict(self):
        """Convert place to dictionary"""
        place_dict = super().to_dict()
        place_dict.update({
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner.id
        })
        return place_dict
