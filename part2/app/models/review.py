# models/review.py
from .base_model import BaseModel

class Review(BaseModel):
    """Class representing a review
    
    Attributes:
        id (str): Unique identifier for each review
        text (str): Content of the review
        rating (int): Rating between 1 and 5
        place (Place): Place being reviewed
        user (User): User who wrote the review
        created_at (DateTime): Timestamp when the review is created
        updated_at (DateTime): Timestamp when the review is last updated
    """

    def __init__(self, text, rating, place, user, **kwargs):
        """Initialize a new review
        
        Args:
            text (str): Review content
            rating (int): Rating between 1 and 5
            place (Place): Place being reviewed
            user (User): User writing the review
        """
        super().__init__(**kwargs)
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
    def validate_text(text):
        """Validate review content"""
        if not text or not text.strip():
            raise ValueError("Review content cannot be empty")

    @staticmethod
    def validate_rating(rating):
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
            'place_id': self.place.id if self.place else None,
            'user_id': self.user.id if self.user else None
        })
        return review_dict

    def create_review(self, review_data):
        """Create a new review with validation
        
        Args:
            review_data (dict): Review data
                
        Returns:
            dict: The newly created review
            
        Raises:
            ValueError: If the review data is invalid
        """
        # Text validation
        if not review_data.get('text'):
            raise ValueError("Review text cannot be empty")
        
        # Rating validation
        rating = review_data.get('rating')
        if rating is not None:
            try:
                rating = int(rating)
                if not 1 <= rating <= 5:
                    raise ValueError("Rating must be between 1 and 5")
            except (ValueError, TypeError):
                raise ValueError("Rating must be an integer between 1 and 5")
        
        # User ID validation
        if not review_data.get('user_id') or review_data['user_id'] not in self.users_db:
            raise ValueError(f"User with ID {review_data.get('user_id')} does not exist")
        
        # Place ID validation
        if not review_data.get('place_id') or review_data['place_id'] not in self.places_db:
            raise ValueError(f"Place with ID {review_data.get('place_id')} does not exist")

