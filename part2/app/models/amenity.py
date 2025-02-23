# models/amenity.py
from .base_model import BaseModel

class Amenity(BaseModel):
    """Class representing an amenity"""

    def __init__(self, name: str):
        """
        Initialize a new amenity
        Args:
            name (str): Name of the amenity
        """
        super().__init__()
        self.validate_name(name)
        self.name = name
        self.places = []  # List of places with this amenity

    @staticmethod
    def validate_name(name: str):
        """Validate amenity name"""
        if not name or len(name) > 50:
            raise ValueError("Amenity name must be between 1 and 50 characters")

    def add_place(self, place):
        """Add a place to the amenity"""
        if place not in self.places:
            self.places.append(place)
            place.add_amenity(self)

    def to_dict(self):
        """Convert amenity to dictionary"""
        amenity_dict = super().to_dict()
        amenity_dict.update({
            'name': self.name
        })
        return amenity_dict
