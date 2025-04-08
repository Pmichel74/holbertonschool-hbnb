from app import db
from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    # Repository for Place model with extended operations beyond basic CRUD
    
    def __init__(self):
        # Initialize with Place model
        super().__init__(Place)
    
    def get_by_owner(self, owner_id):
        # Find places by owner ID
        return self.model.query.filter_by(owner_id=owner_id).all()
    
    def get_by_price_range(self, min_price, max_price):
        # Find places within a price range
        return self.model.query.filter(
            self.model.price >= min_price,
            self.model.price <= max_price
        ).all()
    
    def create_place(self, place_data):
        # Create a new place
        place = Place()
        
        # Handle amenities separately if provided
        amenities_data = place_data.pop('amenities', None)
        
        # Set attributes from place_data
        for key, value in place_data.items():
            setattr(place, key, value)
        
        # Handle amenities if provided
        if amenities_data:
            from app.models.amenity import Amenity
            amenities = []
            for amenity_id in amenities_data:
                amenity = Amenity.query.get(amenity_id)
                if amenity:
                    amenities.append(amenity)
            place.amenities = amenities
        
        # Add to database and commit
        db.session.add(place)
        db.session.commit()
        
        return place
    
    def update_place(self, place_id, place_data):
        # Update place
        place = self.get(place_id)
        if not place:
            return None
        
        # Handle amenities separately if provided
        amenities_data = place_data.pop('amenities', None)
        
        # Update attributes
        for key, value in place_data.items():
            setattr(place, key, value)
        
        # Handle amenities if provided
        if amenities_data:
            from app.models.amenity import Amenity
            amenities = []
            for amenity_id in amenities_data:
                amenity = Amenity.query.get(amenity_id)
                if amenity:
                    amenities.append(amenity)
            place.amenities = amenities
        
        # Commit changes
        db.session.commit()
        
        return place
