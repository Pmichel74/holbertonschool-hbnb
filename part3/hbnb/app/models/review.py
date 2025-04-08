from app import db
from app.models.base_model import BaseModel
from sqlalchemy.orm import validates, relationship

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="reviews")
    place = relationship("Place", back_populates="reviews")

    @validates('text')
    def validate_text(self, key, value):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Text is required and must be a non-empty string")
        if len(value) > 1000:
            raise ValueError("Text must be at most 1000 characters long")
        return value.strip()

    @validates('rating')
    def validate_rating(self, key, value):
        try:
            rating_value = int(value)
            if rating_value < 1 or rating_value > 5:
                raise ValueError("Rating must be between 1 and 5")
            return rating_value
        except (ValueError, TypeError):
            if isinstance(value, (int, float)) and (value < 1 or value > 5):
                raise ValueError("Rating must be between 1 and 5")
            raise ValueError("Rating must be a number between 1 and 5")

    def update(self, data):
        """Update the attributes of the review"""
        super().update(data)
