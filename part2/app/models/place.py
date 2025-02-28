import uuid
from datetime import datetime
from app.models.base_model import BaseModel

class Place(BaseModel):
    """Place Model for HBnB"""
    
    def __init__(self, *args, **kwargs):
        """Initialize Place instance"""
        super().__init__(*args, **kwargs)
        self.title = kwargs.get('title', '')
        self.description = kwargs.get('description', '')
        self._price = kwargs.get('price', 0.0)
        self._latitude = kwargs.get('latitude', 0.0)
        self._longitude = kwargs.get('longitude', 0.0)
        self.owner_id = kwargs.get('owner_id', '')
        self.amenities = kwargs.get('amenities', [])
        
    @property
    def price(self):
        """Getter for price attribute"""
        return self._price
    
    @price.setter
    def price(self, value):
        """Setter for price attribute with validation"""
        if not isinstance(value, (int, float)):
            raise ValueError("Price must be a number")
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = float(value)
    
    @property
    def latitude(self):
        """Getter for latitude attribute"""
        return self._latitude
    
    @latitude.setter
    def latitude(self, value):
        """Setter for latitude attribute with validation"""
        if not isinstance(value, (int, float)):
            raise ValueError("Latitude must be a number")
        if value < -90 or value > 90:
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = float(value)
    
    @property
    def longitude(self):
        """Getter for longitude attribute"""
        return self._longitude
    
    @longitude.setter
    def longitude(self, value):
        """Setter for longitude attribute with validation"""
        if not isinstance(value, (int, float)):
            raise ValueError("Longitude must be a number")
        if value < -180 or value > 180:
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = float(value)
        
    def to_dict(self):
        """Return dictionary of Place instance"""
        place_dict = super().to_dict()
        place_dict['price'] = self.price
        place_dict['latitude'] = self.latitude
        place_dict['longitude'] = self.longitude
        return place_dict
