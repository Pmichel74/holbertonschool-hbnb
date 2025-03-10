#!/usr/bin/python3
"""Modèle Review"""
from app.models.base_model import BaseModel

class Review(BaseModel):
    """Modèle pour les avis sur les lieux"""
    
    def __init__(self, **kwargs):
        """Initialise un avis"""
        super().__init__(**kwargs)
        self.place_id = kwargs.get('place_id', '')
        self.user_id = kwargs.get('user_id', '')
        self.text = kwargs.get('text', '')
        # Score sur 5 étoiles (optionnel)
        self.rating = kwargs.get('rating', 0)

    def to_dict(self):
        """Retourne le dictionnaire de l'avis"""
        review_dict = super().to_dict()
        review_dict['rating'] = int(self.rating)
        return review_dict
