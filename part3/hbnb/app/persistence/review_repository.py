from app import db
from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository

class ReviewRepository(SQLAlchemyRepository):
    # Repository for Review model with extended operations beyond basic CRUD
    
    def __init__(self):
        # Initialize with Review model
        super().__init__(Review)
    
    def get_by_place(self, place_id):
        # Find reviews by place ID
        return self.model.query.filter_by(place_id=place_id).all()
    
    def get_by_user(self, user_id):
        # Find reviews by user ID
        return self.model.query.filter_by(user_id=user_id).all()
    
    def get_by_rating(self, rating):
        # Find reviews by rating
        return self.model.query.filter_by(rating=rating).all()
    
    def create_review(self, review_data):
        # Create a new review
        review = Review()
        
        # Set attributes from review_data
        for key, value in review_data.items():
            setattr(review, key, value)
        
        # Add to database and commit
        db.session.add(review)
        db.session.commit()
        
        return review
    
    def update_review(self, review_id, review_data):
        # Update review
        review = self.get(review_id)
        if not review:
            return None
        
        # Update attributes
        for key, value in review_data.items():
            setattr(review, key, value)
        
        # Commit changes
        db.session.commit()
        
        return review
