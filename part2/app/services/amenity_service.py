#!/usr/bin/python3
"""Service pour les opérations liées aux équipements"""

class AmenityService:
    """Service pour la gestion des équipements"""
    
    def __init__(self, storage):
        """Initialise le service avec le stockage"""
        self.storage = storage
    
    def get_amenity(self, amenity_id):
        """Récupère un équipement par son ID"""
        # Import Amenity ici pour éviter les importations circulaires
        from app.models.amenity import Amenity
        return self.storage.get(Amenity, amenity_id)
    
    def get_all_amenities(self):
        """Récupère tous les équipements"""
        # Import Amenity ici pour éviter les importations circulaires
        from app.models.amenity import Amenity
        return self.storage.all(Amenity)
    
    def create_amenity(self, amenity_data):
        """Crée un nouvel équipement"""
        from app.models.amenity import Amenity
        amenity = Amenity(**amenity_data)
        self.storage.new(amenity)
        self.storage.save()
        return amenity
    
    def update_amenity(self, amenity_id, data):
        """Met à jour un équipement existant"""
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            # Import ici pour éviter les importations circulaires
            from app.error_handlers import NotFoundError
            raise NotFoundError(f"Amenity {amenity_id} not found")
            
        for key, value in data.items():
            if hasattr(amenity, key):
                setattr(amenity, key, value)
                
        self.storage.save()
        return amenity
    
    # Note: nous gardons la méthode delete_amenity même si elle n'est pas exposée via l'API
    def delete_amenity(self, amenity_id):
        """Supprime un équipement"""
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            # Import ici pour éviter les importations circulaires
            from app.error_handlers import NotFoundError
            raise NotFoundError(f"Amenity {amenity_id} not found")
            
        self.storage.delete(amenity)
        self.storage.save()
        return True
    
    # Supprimez ces méthodes si elles existent
    # def get_place_amenities(self, place_id):
    #    ...
    # def add_amenity_to_place(self, place_id, amenity_id):
    #    ...
    # def remove_amenity_from_place(self, place_id, amenity_id):
    #    ...