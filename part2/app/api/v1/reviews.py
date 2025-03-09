from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Models for references (user and place)
user_model = api.model('ReviewUser', {
    'id': fields.String(description='User identifier'),
    'first_name': fields.String(description='User first name'),
    'last_name': fields.String(description='User last name'),
    'email': fields.String(description='User email')
})

place_summary_model = api.model('ReviewPlace', {
    'id': fields.String(description='Place identifier'),
    'title': fields.String(description='Place title')
})

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# Model for detailed review information
review_output_model = api.model('ReviewOutput', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user'),
    'place_id': fields.String(description='ID of the place')
})

# Define an enriched response model
review_response_model = api.model('ReviewResponse', {
    'id': fields.String(description='Review identifier'),
    'text': fields.String(description='Review content'),
    'rating': fields.Integer(description='Rating (1-5)'),
    'user_id': fields.String(description='User identifier'),
    'place_id': fields.String(description='Place identifier'),
    'created_at': fields.String(description='Creation date'),
    'updated_at': fields.String(description='Last update date'),
    'user': fields.Nested(user_model),
    'place': fields.Nested(place_summary_model)
})

@api.route('/')
class ReviewList(Resource):
    @api.doc('create_review')
    @api.expect(review_model)
    @api.marshal_with(review_response_model, code=201, mask=False)  # Add mask=False here
    def post(self):
        """Register a new review"""
        try:
            # Create the review with the facade
            review = facade.create_review(api.payload)
            
            # Add logs for diagnostics
            print(f"Review created with ID: {review.get('id')}")
            print(f"User ID: {review.get('user_id')}, Place ID: {review.get('place_id')}")
            
            # Enrich the response with handling for cases where user/place is None
            enriched_review = review.copy()
            
            # Secure handling of user information
            try:
                user = facade.get_user(review.get('user_id'))
                if user:
                    enriched_review['user'] = user
                else:
                    print(f"Warning: User {review.get('user_id')} not found")
                    enriched_review['user'] = {
                        'id': review.get('user_id'),
                        'first_name': '(unknown)',
                        'last_name': '(unknown)',
                        'email': '(unknown)'
                    }
            except Exception as e:
                print(f"Error getting user: {str(e)}")
                enriched_review['user'] = {
                    'id': review.get('user_id'),
                    'first_name': '(error)',
                    'last_name': '(error)',
                    'email': '(error)'
                }
                
            # Secure handling of place information
            try:
                place = facade.get_place(review.get('place_id'))
                if place:
                    enriched_review['place'] = {
                        'id': place.get('id'),
                        'title': place.get('title', '(no title)')
                    }
                else:
                    print(f"Warning: Place {review.get('place_id')} not found")
                    enriched_review['place'] = {
                        'id': review.get('place_id'),
                        'title': '(unknown place)'
                    }
            except Exception as e:
                print(f"Error getting place: {str(e)}")
                enriched_review['place'] = {
                    'id': review.get('place_id'),
                    'title': '(error)'
                }
            
            return enriched_review, 201
            
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            # Capture and trace ALL possible errors
            import traceback
            print(f"CRITICAL ERROR in POST /reviews/: {str(e)}")
            traceback.print_exc()  # Display the complete stack trace
            api.abort(500, f"An internal error occurred: {str(e)}")

    @api.response(200, 'List of reviews retrieved successfully')
    @api.marshal_list_with(review_response_model, mask=False)  # Add mask=False here
    def get(self):
        """Retrieve a list of all reviews"""
        # Retrieve all reviews
        reviews = facade.get_all_reviews()
        
        # Enrich each review with user and place information
        enriched_reviews = []
        for review in reviews:
            enriched_review = review.copy()
            
            # Add user information
            try:
                user = facade.get_user(review.get('user_id'))
                if user:
                    enriched_review['user'] = user
                else:
                    enriched_review['user'] = {
                        'id': review.get('user_id'),
                        'first_name': '(unknown)',
                        'last_name': '(unknown)',
                        'email': '(unknown)'
                    }
            except Exception as e:
                print(f"Error getting user for review {review.get('id')}: {str(e)}")
                enriched_review['user'] = {
                    'id': review.get('user_id'),
                    'first_name': '(error)',
                    'last_name': '(error)',
                    'email': '(error)'
                }
            
            # Add place information
            try:
                place = facade.get_place(review.get('place_id'))
                if place:
                    enriched_review['place'] = {
                        'id': place.get('id'),
                        'title': place.get('title', '(no title)')
                    }
                else:
                    enriched_review['place'] = {
                        'id': review.get('place_id'),
                        'title': '(unknown place)'
                    }
            except Exception as e:
                print(f"Error getting place for review {review.get('id')}: {str(e)}")
                enriched_review['place'] = {
                    'id': review.get('place_id'),
                    'title': '(error)'
                }
            
            enriched_reviews.append(enriched_review)
        
        return enriched_reviews, 200

@api.route('/<string:review_id>')
@api.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    @api.marshal_with(review_response_model, mask=False)
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if review is None:
            api.abort(404, f"Review with ID {review_id} not found")
        
        # Enrich the review with user and place information
        enriched_review = review.copy()
        
        # Add user information 
        try:
            user = facade.get_user(review.get('user_id'))
            if user:
                enriched_review['user'] = user
            else:
                enriched_review['user'] = {
                    'id': review.get('user_id'),
                    'first_name': '(unknown)',
                    'last_name': '(unknown)',
                    'email': '(unknown)'
                }
        except Exception as e:
            enriched_review['user'] = {
                'id': review.get('user_id'),
                'first_name': '(error)',
                'last_name': '(error)',
                'email': '(error)'
            }
        
        # Add place information
        try:
            place = facade.get_place(review.get('place_id'))
            if place:
                enriched_review['place'] = {
                    'id': place.get('id'),
                    'title': place.get('title', '(no title)')
                }
            else:
                enriched_review['place'] = {
                    'id': review.get('place_id'),
                    'title': '(unknown place)'
                }
        except Exception as e:
            enriched_review['place'] = {
                'id': review.get('place_id'),
                'title': '(error)'
            }
        
        return enriched_review, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        try:
            review_data = api.payload
            result = facade.update_review(review_id, review_data)
            if result is None:
                api.abort(404, f"Review with ID {review_id} not found")
            return result, 200
        except ValueError as e:
            return {'message': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        result = facade.delete_review(review_id)
        if not result:
            api.abort(404, f"Review with ID {review_id} not found")
        return {'message': 'Review deleted successfully'}, 200

