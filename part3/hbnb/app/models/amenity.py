from app import db
from app.models.base_model import BaseModel
from sqlalchemy.orm import validates, relationship
from app.models.associations import place_amenity

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)
    
    # Relationships
    places = relationship("Place", secondary=place_amenity, back_populates="amenities")

    @validates('name')
    def validate_name(self, key, value):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Amenity name is required and must be a non-empty string")
        if len(value) > 50:
            raise ValueError("Amenity name must be at most 50 characters long")
        return value.strip()

    def update(self, data):
        """Update the attributes of the amenity"""
        super().update(data)
