# app/services/facade.py

from models import storage
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User

class HBNBFacade:
    """Façade pour gérer toute la logique métier de l'application"""

    @staticmethod
    def get_all_objects(cls):
        """Récupère tous les objets d'une classe donnée"""
        return storage.all(cls).values()

    @staticmethod
    def get_object_by_id(cls, obj_id):
        """Récupère un objet par son ID"""
        return storage.get(cls, obj_id)

    @staticmethod
    def create_object(cls, data):
        """Crée un nouvel objet"""
        obj = cls(**data)
        obj.save()
        return obj

    @staticmethod
    def update_object(obj, data, ignore_fields=None):
        """Met à jour un objet avec les données fournies"""
        if ignore_fields is None:
            ignore_fields = ['id', 'created_at', 'updated_at']
        
        for key, value in data.items():
            if key not in ignore_fields:
                setattr(obj, key, value)
        obj.save()
        return obj

    @staticmethod
    def delete_object(obj):
        """Supprime un objet"""
        storage.delete(obj)
        storage.save()

    # Méthodes spécifiques pour Amenity
    def get_all_amenities(self):
        """Récupère toutes les amenities"""
        return self.get_all_objects(Amenity)

    def get_amenity(self, amenity_id):
        """Récupère une amenity par son ID"""
        return self.get_object_by_id(Amenity, amenity_id)

    def create_amenity(self, data):
        """Crée une nouvelle amenity"""
        return self.create_object(Amenity, data)

    # Méthodes spécifiques pour Place
    def get_all_places(self):
        """Récupère tous les places"""
        return self.get_all_objects(Place)

    def get_place(self, place_id):
        """Récupère un place par son ID"""
        return self.get_object_by_id(Place, place_id)

    def create_place(self, data):
        """Crée un nouveau place"""
        return self.create_object(Place, data)

    # Méthodes spécifiques pour Review
    def get_place_reviews(self, place_id):
        """Récupère toutes les reviews d'un place"""
        place = self.get_place(place_id)
        if place:
            return place.reviews
        return None

    def create_review(self, place_id, data):
        """Crée une nouvelle review pour un place"""
        place = self.get_place(place_id)
        if place:
            data['place_id'] = place_id
            return self.create_object(Review, data)
        return None

    # Méthodes spécifiques pour User
    def get_all_users(self):
        """Récupère tous les utilisateurs"""
        return self.get_all_objects(User)

    def get_user(self, user_id):
        """Récupère un utilisateur par son ID"""
        return self.get_object_by_id(User, user_id)

    def create_user(self, data):
        """Crée un nouvel utilisateur"""
        return self.create_object(User, data)
