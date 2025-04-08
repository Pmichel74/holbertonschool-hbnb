from app import db
from app.models.base_model import BaseModel
from sqlalchemy.orm import validates, relationship
from app.models.associations import place_amenity

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="places")
    reviews = relationship("Review", back_populates="place", cascade="all, delete-orphan")
    amenities = relationship("Amenity", secondary=place_amenity, back_populates="places")

    @validates('title', 'description')
    def validate_string(self, key, value):
        field_name = key.title()
        max_length = 100 if key == 'title' else 1000
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError(f"{field_name} is required and must be a non-empty string")
        if len(value) > max_length:
            raise ValueError(f"{field_name} must be at most {max_length} characters long")
        return value.strip()

    @validates('price')
    def validate_price(self, key, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Price must be a number")
        if value <= 0:
            raise ValueError("Price cannot be negative or null")
        return float(value)

    @validates('latitude')
    def validate_latitude(self, key, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Latitude must be a number")
        if value < -90 or value > 90:
            raise ValueError("Latitude must be between -90 and 90")
        return float(value)

    @validates('longitude')
    def validate_longitude(self, key, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Longitude must be a number")
        if value < -180 or value > 180:
            raise ValueError("Longitude must be between -180 and 180")
        return float(value)

    def update(self, data):
        """Update the attributes of the place"""
        super().update(data)
