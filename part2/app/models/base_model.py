#!/usr/bin/python3
"""Modèle de base pour tous les modèles"""
import uuid
from datetime import datetime

class BaseModel:
    """Classe de base pour tous les modèles HBNB"""
    
    def __init__(self, **kwargs):
        """Initialise un modèle de base"""
        self.id = kwargs.get('id', str(uuid.uuid4()))
        
        # Conversion des dates si elles sont fournies en string
        if 'created_at' in kwargs and isinstance(kwargs['created_at'], str):
            self.created_at = datetime.fromisoformat(kwargs['created_at'].replace('Z', '+00:00'))
        else:
            self.created_at = kwargs.get('created_at', datetime.now())
            
        if 'updated_at' in kwargs and isinstance(kwargs['updated_at'], str):
            self.updated_at = datetime.fromisoformat(kwargs['updated_at'].replace('Z', '+00:00'))
        else:
            self.updated_at = kwargs.get('updated_at', datetime.now())
    
    def __str__(self):
        """Représentation string du modèle"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
    
    def save(self):
        """Met à jour updated_at avec l'heure actuelle"""
        from app.persistence.storage_engine import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()
    
    def delete(self):
        """Supprime l'instance courante du stockage"""
        from app.persistence.storage_engine import storage
        storage.delete(self)
        storage.save()
    
    def to_dict(self):
        """Convertit l'instance en dictionnaire"""
        result = self.__dict__.copy()
        result['__class__'] = self.__class__.__name__
        
        # Conversion des dates en string ISO
        if 'created_at' in result and isinstance(result['created_at'], datetime):
            result['created_at'] = result['created_at'].isoformat()
            
        if 'updated_at' in result and isinstance(result['updated_at'], datetime):
            result['updated_at'] = result['updated_at'].isoformat()
            
        return result
