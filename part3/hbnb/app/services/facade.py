from app.persistence.repository import SQLAlchemyRepository
from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.amenity_repository import AmenityRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

# User methods
    def create_user(self, user_data):
        return self.user_repo.create_user(user_data)

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_by_email(self, email):
        return self.user_repo.get_by_email(email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        return self.user_repo.update_user(user_id, user_data)

# Amenities methods
    def create_amenity(self, amenity_data):
        return self.amenity_repo.create_amenity(amenity_data)

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_repo.update_amenity(amenity_id, amenity_data)
    
# Place methods
    def create_place(self, place_data):
        """
        Creates a new place after validating owner and amenities
        """
        # Validate owner exists
        owner_id = place_data.get('owner_id')
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError(f"Owner with ID {owner_id} does not exist")
    
        # Validate amenities if provided
        if 'amenities' in place_data and place_data['amenities']:
            valid_amenities = []
            for amenity_id in place_data['amenities']:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity with ID {amenity_id} does not exist")
                valid_amenities.append(amenity_id)
            place_data['amenities'] = valid_amenities
    
        # Create and save place
        return self.place_repo.create_place(place_data)

    def get_place(self, place_id):
        """
        Retrieves a place by ID
        """
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """
        Retrieves all places
        """
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """
        Updates a place after validating related data
        """
        place = self.get_place(place_id)
        if not place:
            return None
    
        # Validate owner if changing
        if 'owner_id' in place_data:
            owner = self.get_user(place_data.get('owner_id'))
            if not owner:
                raise ValueError(f"Owner with ID {place_data.get('owner_id')} does not exist")
    
        # Validate amenities if changing
        if 'amenities' in place_data and place_data['amenities']:
            valid_amenities = []
            for amenity_id in place_data['amenities']:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity with ID {amenity_id} does not exist")
                valid_amenities.append(amenity_id)
            place_data['amenities'] = valid_amenities
    
        # Update place
        return self.place_repo.update_place(place_id, place_data)

    def get_place_with_details(self, place_id):
        """
        Gets place with detailed info about owner and amenities
        """
        place = self.get_place(place_id)
        if not place:
            return None
    
        # Get owner details
        owner = place.owner
        owner_details = None
        if owner:
            owner_details = {
                'id': owner.id,
                'first_name': owner.first_name,
                'last_name': owner.last_name,
                'email': owner.email
            }
    
        # Get amenities details
        amenity_details = []
        for amenity in place.amenities:
            amenity_details.append({
                'id': amenity.id,
                'name': amenity.name
            })
    
        # Create detailed response with all place info
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': owner_details,
            'amenities': amenity_details,
            'created_at': place.created_at,
            'updated_at': place.updated_at
        }
    
    def delete_place(self, place_id):
        """
        Deletes a place and all its associated reviews
        """
        place = self.get_place(place_id)
        if not place:
            return False
        
        # Delete the place
        self.place_repo.delete(place_id)
        return True

# Review methods
    def create_review(self, review_data):
        """
        Creates a new review after validating user_id, place_id, and rating
        """
        # Validate user exists
        user = self.get_user(review_data.get('user_id'))
        if not user:
            raise ValueError(f"User with ID {review_data.get('user_id')} does not exist")
        
        # Validate place exists
        place = self.get_place(review_data.get('place_id'))
        if not place:
            raise ValueError(f"Place with ID {review_data.get('place_id')} does not exist")
        
        # Create and save review
        return self.review_repo.create_review(review_data)

    def get_review(self, review_id):
        """
        Retrieves a review by ID
        """
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """
        Retrieves all reviews
        """
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """
        Retrieves all reviews for a specific place
        """
        # First verify that the place exists
        place = self.get_place(place_id)
        if not place:
            return None
        
        # Get reviews directly from the relationship
        return place.reviews

    def update_review(self, review_id, review_data):
        """
        Updates a review after validation
        """
        review = self.get_review(review_id)
        if not review:
            return None
        
        # Validate user_id if it's being updated
        if 'user_id' in review_data:
            user = self.get_user(review_data.get('user_id'))
            if not user:
                raise ValueError(f"User with ID {review_data.get('user_id')} does not exist")
        
        # Validate place_id if it's being updated
        if 'place_id' in review_data:
            place = self.get_place(review_data.get('place_id'))
            if not place:
                raise ValueError(f"Place with ID {review_data.get('place_id')} does not exist")
        
        # Update review
        return self.review_repo.update_review(review_id, review_data)

    def delete_review(self, review_id):
        """
        Deletes a review
        """
        review = self.get_review(review_id)
        if not review:
            return False
        
        self.review_repo.delete(review_id)
        return True

    # Update the get_place_with_details method to include reviews
    def get_place_with_details(self, place_id):
        """Get a place with owner, amenities and reviews details"""
        place = self.get_place(place_id)
        if not place:
            return None
        
        # Get owner details
        owner = place.owner
        owner_details = None
        if owner:
            owner_details = {
                'id': owner.id,
                'first_name': owner.first_name,
                'last_name': owner.last_name,
                'email': owner.email
            }
        
        # Get amenities details
        amenity_details = []
        for amenity in place.amenities:
            amenity_details.append({
                'id': amenity.id,
                'name': amenity.name
            })
        
        # Get reviews details
        review_details = []
        for review in place.reviews:
            review_details.append({
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id
            })
        
        # Create detailed response with all place info
        from datetime import datetime
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': owner_details,
            'amenities': amenity_details,
            'reviews': review_details,
            'created_at': place.created_at if isinstance(place.created_at, str) else place.created_at.isoformat() if isinstance(place.created_at, datetime) else str(place.created_at),
            'updated_at': place.updated_at if isinstance(place.updated_at, str) else place.updated_at.isoformat() if isinstance(place.updated_at, datetime) else str(place.updated_at)
        }
    
facade = HBnBFacade()
