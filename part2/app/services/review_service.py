#!/usr/bin/python3
"""Service pour les opérations liées aux avis"""

class ReviewService:
    """Service pour la gestion des avis"""
    
    def __init__(self, storage):
        """Initialise le service avec le stockage"""
        self.storage = storage
    
    def get_review(self, review_id):
        """Récupère un avis par son ID"""
        # Import Review ici pour éviter les importations circulaires
        from app.models.review import Review
        return self.storage.get(Review, review_id)
    
    def get_all_reviews(self):
        """Récupère tous les avis"""
        # Import Review ici pour éviter les importations circulaires
        from app.models.review import Review
        return self.storage.all(Review)
    
    def get_place_reviews(self, place_id):
        """Récupère tous les avis pour un lieu spécifique"""
        from app.models.review import Review
        all_reviews = self.storage.all(Review)
        return [review for review in all_reviews if review.place_id == place_id]
    
    def get_user_reviews(self, user_id):
        """Récupère tous les avis écrits par un utilisateur spécifique"""
        from app.models.review import Review
        all_reviews = self.storage.all(Review)
        return [review for review in all_reviews if review.user_id == user_id]
    
    def create_review(self, review_data):
        """Crée un nouvel avis"""
        from app.models.review import Review
        
        # Vérifier si l'utilisateur et le lieu existent
        from app.models.user import User
        from app.models.place import Place
        
        user = self.storage.get(User, review_data.get('user_id'))
        place = self.storage.get(Place, review_data.get('place_id'))
        
        if not user:
            from app.error_handlers import NotFoundError
            raise NotFoundError(f"User {review_data.get('user_id')} not found")
            
        if not place:
            from app.error_handlers import NotFoundError
            raise NotFoundError(f"Place {review_data.get('place_id')} not found")
            
        # Vérifier que le rating est dans la plage acceptable
        if 'rating' in review_data and (review_data['rating'] < 0 or review_data['rating'] > 5):
            from app.error_handlers import ValidationError
            raise ValidationError("Rating must be between 0 and 5")
            
        # Créer l'avis
        review = Review(**review_data)
        self.storage.new(review)
        self.storage.save()
        return review
    
    def update_review(self, review_id, data):
        """Met à jour un avis existant"""
        review = self.get_review(review_id)
        if not review:
            from app.error_handlers import NotFoundError
            raise NotFoundError(f"Review {review_id} not found")
            
        # Vérifier que le rating est dans la plage acceptable
        if 'rating' in data and (data['rating'] < 0 or data['rating'] > 5):
            from app.error_handlers import ValidationError
            raise ValidationError("Rating must be between 0 and 5")
            
        # Ne pas permettre de modifier l'utilisateur ou le lieu associé
        protected_fields = ['user_id', 'place_id']
        for field in protected_fields:
            if field in data:
                data.pop(field)
                
        for key, value in data.items():
            if hasattr(review, key):
                setattr(review, key, value)
                
        self.storage.save()
        return review
    
    def delete_review(self, review_id):
        """Supprime un avis"""
        review = self.get_review(review_id)
        if not review:
            from app.error_handlers import NotFoundError
            raise NotFoundError(f"Review {review_id} not found")
            
        self.storage.delete(review)
        self.storage.save()
        return True
