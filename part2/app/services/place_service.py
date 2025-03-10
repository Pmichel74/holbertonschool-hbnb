#!/usr/bin/python3
"""Service pour les opérations liées aux lieux"""

class PlaceService:
    """Service pour la gestion des lieux"""
    
    def __init__(self, storage):
        """Initialise le service avec le stockage"""
        self.storage = storage
    
    def get_place(self, place_id):
        """Récupère un lieu par son ID"""
        # Import Place ici pour éviter les importations circulaires
        from app.models.place import Place
        return self.storage.get(Place, place_id)
    
    def get_all_places(self):
        """Récupère tous les lieux"""
        # Import Place ici pour éviter les importations circulaires
        from app.models.place import Place
        return self.storage.all(Place)
    
    def get_places_by_user(self, user_id):
        """Récupère tous les lieux associés à un utilisateur"""
        from app.models.place import Place
        all_places = self.storage.all(Place)
        return [place for place in all_places if place.user_id == user_id]
    
    def create_place(self, place_data):
        """Crée un nouveau lieu"""
        from app.models.place import Place
        place = Place(**place_data)
        self.storage.new(place)
        self.storage.save()
        return place
    
    def update_place(self, place_id, data, ignore_fields=None):
        """Met à jour un lieu existant, y compris les amenity_ids"""
        if ignore_fields is None:
            ignore_fields = []
            
        place = self.get_place(place_id)
        if not place:
            # Import ici pour éviter les importations circulaires
            from app.error_handlers import NotFoundError
            raise NotFoundError(f"Place {place_id} not found")
            
        # Si amenity_ids est fourni, vérifier que tous les IDs existent
        if 'amenity_ids' in data:
            from app.models.amenity import Amenity
            for amenity_id in data['amenity_ids']:
                amenity = self.storage.get(Amenity, amenity_id)
                if not amenity:
                    from app.error_handlers import NotFoundError
                    raise NotFoundError(f"Amenity {amenity_id} not found")
                    
        for key, value in data.items():
            if key not in ignore_fields and hasattr(place, key):
                setattr(place, key, value)
                
        self.storage.save()
        return place
    
    def delete_place(self, place_id):
        """Supprime un lieu"""
        place = self.get_place(place_id)
        if not place:
            # Import ici pour éviter les importations circulaires
            from app.error_handlers import NotFoundError
            raise NotFoundError(f"Place {place_id} not found")
            
        self.storage.delete(place)
        self.storage.save()
        return True
