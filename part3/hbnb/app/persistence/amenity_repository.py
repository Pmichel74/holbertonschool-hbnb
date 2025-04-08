from app import db
from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository

class AmenityRepository(SQLAlchemyRepository):
    # Repository for Amenity model with extended operations beyond basic CRUD
    
    def __init__(self):
        # Initialize with Amenity model
        super().__init__(Amenity)
    
    def get_by_name(self, name):
        # Find amenity by name
        return self.model.query.filter_by(name=name).first()
    
    def create_amenity(self, amenity_data):
        # Create a new amenity
        amenity = Amenity()
        
        # Set attributes from amenity_data
        for key, value in amenity_data.items():
            setattr(amenity, key, value)
        
        # Add to database and commit
        db.session.add(amenity)
        db.session.commit()
        
        return amenity
    
    def update_amenity(self, amenity_id, amenity_data):
        # Update amenity
        amenity = self.get(amenity_id)
        if not amenity:
            return None
        
        # Update attributes
        for key, value in amenity_data.items():
            setattr(amenity, key, value)
        
        # Commit changes
        db.session.commit()
        
        return amenity
