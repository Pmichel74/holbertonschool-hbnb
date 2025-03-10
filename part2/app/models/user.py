#!/usr/bin/python3
"""Modèle User"""
from app.models.base_model import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash

class User(BaseModel):
    """Modèle pour les utilisateurs"""
    
    def __init__(self, **kwargs):
        """Initialise un utilisateur"""
        super().__init__(**kwargs)
        self.email = kwargs.get('email', '')
        self.password_hash = kwargs.get('password_hash', '')
        self.first_name = kwargs.get('first_name', '')
        self.last_name = kwargs.get('last_name', '')
        
        # Si un mot de passe est fourni, le hacher
        if 'password' in kwargs:
            self.set_password(kwargs['password'])
    
    def set_password(self, password):
        """Définit un mot de passe hashé"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Vérifie un mot de passe"""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convertit l'instance en dictionnaire"""
        data = super().to_dict()
        # Ne jamais renvoyer le hash du mot de passe
        if 'password_hash' in data:
            del data['password_hash']
        return data
