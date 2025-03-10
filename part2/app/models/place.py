#!/usr/bin/python3
"""Modèle Place"""
from app.models.base_model import BaseModel

class Place(BaseModel):
    """Modèle pour les lieux"""
    
    def __init__(self, **kwargs):
        """Initialise un lieu"""
        super().__init__(**kwargs)
        self.name = kwargs.get('name', '')
        self.user_id = kwargs.get('user_id', '')
        self.description = kwargs.get('description', '')
        self.price_by_night = kwargs.get('price_by_night', 0)
        self.latitude = kwargs.get('latitude', 0.0)
        self.longitude = kwargs.get('longitude', 0.0)
        
        # Stocker directement les IDs des amenities dans la place
        self.amenity_ids = kwargs.get('amenity_ids', [])
