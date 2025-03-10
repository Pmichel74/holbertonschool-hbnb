#!/usr/bin/python3
"""Modèle Amenity"""
from app.models.base_model import BaseModel

class Amenity(BaseModel):
    """Modèle pour les équipements"""
    
    def __init__(self, **kwargs):
        """Initialise un équipement"""
        super().__init__(**kwargs)
        self.name = kwargs.get('name', '')
