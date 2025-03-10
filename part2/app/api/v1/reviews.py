#!/usr/bin/python3
"""Routes API pour la gestion des avis"""
from flask import request
from flask_restx import Namespace, Resource, fields
from app.middlewares.validation_middleware import ValidationMiddleware
from app.error_handlers import ValidationError, NotFoundError
from app.persistence.storage_engine import storage

api = Namespace('reviews', description='Opérations sur les avis')

# Modèles Swagger pour la documentation de l'API
review_input_model = api.model('ReviewInput', {
    'place_id': fields.String(required=True, description='ID du lieu'),
    'user_id': fields.String(required=True, description='ID de l\'utilisateur'),
    'text': fields.String(required=True, description='Texte de l\'avis'),
    'rating': fields.Integer(description='Note (0-5 étoiles)', min=0, max=5)
})

review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(description='Texte de l\'avis'),
    'rating': fields.Integer(description='Note (0-5 étoiles)', min=0, max=5)
})

review_model = api.model('Review', {
    'id': fields.String(description='ID unique'),
    'place_id': fields.String(description='ID du lieu'),
    'user_id': fields.String(description='ID de l\'utilisateur'),
    'text': fields.String(description='Texte de l\'avis'),
    'rating': fields.Integer(description='Note (0-5 étoiles)'),
    'created_at': fields.DateTime(description='Date de création'),
    'updated_at': fields.DateTime(description='Date de mise à jour')
})

# Initialiser le service
from app.services.review_service import ReviewService
review_service = ReviewService(storage)

@api.route('/')
class ReviewList(Resource):
    """Gestion de la collection d'avis"""
    
    @api.doc('list_reviews', 
             responses={
                 200: 'Success',
                 500: 'Internal Server Error'
             })
    @api.marshal_list_with(review_model)
    def get(self):
        """Liste tous les avis"""
        try:
            reviews = review_service.get_all_reviews()
            return [review.to_dict() for review in reviews]
        except Exception as e:
            api.abort(500, str(e))

    @api.doc('create_review',
             responses={
                 201: 'Review Created',
                 400: 'Validation Error',
                 404: 'User or Place Not Found',
                 500: 'Internal Server Error'
             })
    @api.expect(review_input_model)
    @api.marshal_with(review_model, code=201)
    @ValidationMiddleware.validate_review_data()
    def post(self):
        """Crée un nouvel avis"""
        try:
            data = request.get_json()
            review = review_service.create_review(data)
            return review.to_dict(), 201
        except ValidationError as e:
            api.abort(400, str(e))
        except NotFoundError as e:
            api.abort(404, str(e))
        except Exception as e:
            api.abort(500, str(e))

@api.route('/<review_id>')
@api.param('review_id', 'L\'identifiant de l\'avis')
@api.response(404, 'Avis non trouvé')
class ReviewResource(Resource):
    """Gestion d'un avis spécifique"""

    @api.doc('get_review',
             responses={
                 200: 'Success',
                 404: 'Review Not Found',
                 500: 'Internal Server Error'
             })
    @api.marshal_with(review_model)
    def get(self, review_id):
        """Récupère un avis par son ID"""
        try:
            review = review_service.get_review(review_id)
            if not review:
                api.abort(404, f"Avis {review_id} non trouvé")
            return review.to_dict()
        except NotFoundError as e:
            api.abort(404, str(e))
        except Exception as e:
            api.abort(500, str(e))

    @api.doc('update_review',
             responses={
                 200: 'Success',
                 400: 'Validation Error',
                 404: 'Review Not Found',
                 500: 'Internal Server Error'
             })
    @api.expect(review_update_model)
    @api.marshal_with(review_model)
    @ValidationMiddleware.validate_review_data()
    def put(self, review_id):
        """Met à jour un avis"""
        try:
            data = request.get_json()
            updated_review = review_service.update_review(review_id, data)
            return updated_review.to_dict()
        except NotFoundError as e:
            api.abort(404, str(e))
        except ValidationError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, str(e))

    @api.doc('delete_review',
             responses={
                 204: 'Review Deleted',
                 404: 'Review Not Found',
                 500: 'Internal Server Error'
             })
    @api.response(204, 'Avis supprimé')
    def delete(self, review_id):
        """Supprime un avis"""
        try:
            review_service.delete_review(review_id)
            return '', 204
        except NotFoundError as e:
            api.abort(404, str(e))
        except Exception as e:
            api.abort(500, str(e))

@api.route('/places/<place_id>')
@api.param('place_id', 'L\'identifiant du lieu')
class PlaceReviews(Resource):
    """Gestion des avis pour un lieu spécifique"""
    
    @api.doc('get_place_reviews',
             responses={
                 200: 'Success',
                 404: 'Place Not Found',
                 500: 'Internal Server Error'
             })
    @api.marshal_list_with(review_model)
    def get(self, place_id):
        """Récupère tous les avis pour un lieu spécifique"""
        try:
            # Vérifier si le lieu existe
            from app.models.place import Place
            place = storage.get(Place, place_id)
            if not place:
                api.abort(404, f"Lieu {place_id} non trouvé")
                
            reviews = review_service.get_place_reviews(place_id)
            return [review.to_dict() for review in reviews]
        except NotFoundError as e:
            api.abort(404, str(e))
        except Exception as e:
            api.abort(500, str(e))

@api.route('/users/<user_id>')
@api.param('user_id', 'L\'identifiant de l\'utilisateur')
class UserReviews(Resource):
    """Gestion des avis écrits par un utilisateur spécifique"""
    
    @api.doc('get_user_reviews',
             responses={
                 200: 'Success',
                 404: 'User Not Found',
                 500: 'Internal Server Error'
             })
    @api.marshal_list_with(review_model)
    def get(self, user_id):
        """Récupère tous les avis écrits par un utilisateur spécifique"""
        try:
            # Vérifier si l'utilisateur existe
            from app.models.user import User
            user = storage.get(User, user_id)
            if not user:
                api.abort(404, f"Utilisateur {user_id} non trouvé")
                
            reviews = review_service.get_user_reviews(user_id)
            return [review.to_dict() for review in reviews]
        except NotFoundError as e:
            api.abort(404, str(e))
        except Exception as e:
            api.abort(500, str(e))
