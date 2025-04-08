from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import facade
from datetime import datetime

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Forbidden - Cannot review your own place or already reviewed')
    @jwt_required()
    def post(self):
        """Register a new review"""
        try:
            # Get the current user's identity from the JWT token
            current_user_id = get_jwt_identity()
            
            review_data = api.payload
            
            # Ne remplacez pas user_id s'il est déjà fourni et correct
            if 'user_id' not in review_data or review_data['user_id'] != current_user_id:
                review_data['user_id'] = current_user_id
            
            # Get the place to check ownership
            place = facade.get_place(review_data['place_id'])
            if not place:
                return {'error': 'Place not found'}, 404
                
            # Check if the current user is the owner of the place
            if place.owner_id == current_user_id:
                return {'error': 'You cannot review your own place'}, 400
                
            # Check if the user has already reviewed this place
            reviews = facade.get_reviews_by_place(review_data['place_id'])
            if reviews:
                for review in reviews:
                    if review.user_id == current_user_id:
                        return {'error': 'You have already reviewed this place'}, 400
            new_review = facade.create_review(review_data)
            
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user_id,
                'place_id': new_review.place_id,
                'created_at': new_review.created_at.isoformat() if isinstance(new_review.created_at, datetime) else str(new_review.created_at),
                'updated_at': new_review.updated_at.isoformat() if isinstance(new_review.updated_at, datetime) else str(new_review.updated_at)
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'created_at': review.created_at.isoformat() if isinstance(review.created_at, datetime) else str(review.created_at),
            'updated_at': review.updated_at.isoformat() if isinstance(review.updated_at, datetime) else str(review.updated_at)
        } for review in reviews], 200

@api.route('/<string:review_id>')
@api.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
            
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id,
            'created_at': review.created_at.isoformat() if isinstance(review.created_at, datetime) else str(review.created_at),
            'updated_at': review.updated_at.isoformat() if isinstance(review.updated_at, datetime) else str(review.updated_at)
        }, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Forbidden - Can only modify your own reviews')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        try:
            # Get the current user's identity
            current_user_id = get_jwt_identity()
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            user_id = current_user_id
            
            # Get the review to check ownership
            review = facade.get_review(review_id)
            if not review:
                return {'error': 'Review not found'}, 404
                
            # Check if the current user is the creator of the review or an admin
            if not is_admin and str(review.user_id) != str(user_id):
                return {'error': 'Unauthorized action'}, 403
            
            review_data = api.payload
            
            # Ensure user_id cannot be changed
            if 'user_id' in review_data:
                review_data['user_id'] = current_user_id
                
            # Ensure place_id cannot be changed
            if 'place_id' in review_data and review_data['place_id'] != review.place_id:
                return {'error': 'Cannot change the place of a review'}, 400
            updated_review = facade.update_review(review_id, review_data)
            
            if not updated_review:
                return {'error': 'Review not found'}, 404
                
            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'user_id': updated_review.user_id,
                'place_id': updated_review.place_id,
                'created_at': updated_review.created_at.isoformat() if isinstance(updated_review.created_at, datetime) else str(updated_review.created_at),
                'updated_at': updated_review.updated_at.isoformat() if isinstance(updated_review.updated_at, datetime) else str(updated_review.updated_at)
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Forbidden - Can only delete your own reviews')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        # Get the current user's identity
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        user_id = current_user_id
        
        # Get the review to check ownership
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        # Check if the current user is the creator of the review or an admin
        if not is_admin and str(review.user_id) != str(user_id):
            return {'error': 'Unauthorized action'}, 403
            
        success = facade.delete_review(review_id)
        if not success:
            return {'error': 'Review not found'}, 404
        return {'message': 'Review deleted successfully'}, 200
