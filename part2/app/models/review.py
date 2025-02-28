# models/review.py
from .base_model import BaseModel

class Review(BaseModel):
    """Class representing a review"""

    def __init__(self, text: str, rating: int, place, user):
        """
        Initialize a new review
        Args:
            text (str): Review content
            rating (int): Rating between 1 and 5
            place (Place): Place being reviewed
            user (User): User writing the review
        """
        super().__init__()
        self.validate_text(text)
        self.validate_rating(rating)
        self.validate_relationships(place, user)

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

        # Update relationships
        self.place.add_review(self)
        self.user.add_review(self)

    @staticmethod
    def validate_text(text: str):
        """Validate review content"""
        if not text or not text.strip():
            raise ValueError("Review content cannot be empty")

    @staticmethod
    def validate_rating(rating: int):
        """Validate rating"""
        if not isinstance(rating, int) or not 1 <= rating <= 5:
            raise ValueError("Rating must be an integer between 1 and 5")

    @staticmethod
    def validate_relationships(place, user):
        """Validate Place and User relationships"""
        if not place:
            raise ValueError("Review must be associated with a place")
        if not user:
            raise ValueError("Review must be associated with a user")

    def to_dict(self):
        """Convert review to dictionary"""
        review_dict = super().to_dict()
        review_dict.update({
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place.id,
            'user_id': self.user.id
        })
        return review_dict
