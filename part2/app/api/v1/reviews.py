from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Opérations sur les reviews')

# Modèle pour la validation et la documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Texte de la review'),
    'rating': fields.Integer(required=True, description='Note de la place (1-5)'),
    'user_id': fields.String(required=True, description="ID de l'utilisateur"),
    'place_id': fields.String(required=True, description="ID de la place")
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review créée avec succès')
    @api.response(400, 'Données invalides')
    def post(self):
        """Créer une nouvelle review"""
        review_data = api.payload
        review = facade.HBnBFacade().create_review(review_data)
        if review:
            return review, 201
        return {'message': 'Données invalides'}, 400

    @api.response(200, 'Liste des reviews récupérée avec succès')
    def get(self):
        """Récupérer toutes les reviews"""
        reviews = facade.HBnBFacade().get_all_reviews()
        return reviews, 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Détails de la review récupérés avec succès')
    @api.response(404, 'Review non trouvée')
    def get(self, review_id):
        """Récupérer les détails d'une review"""
        review = facade.HBnBFacade().get_review(review_id)
        if review:
            return review, 200
        return {'message': 'Review non trouvée'}, 404

    @api.expect(review_model)
    @api.response(200, 'Review mise à jour avec succès')
    @api.response(400, 'Données invalides')
    @api.response(404, 'Review non trouvée')
    def put(self, review_id):
        """Mettre à jour une review"""
        review_data = api.payload
        updated = facade.HBnBFacade().update_review(review_id, review_data)
        if updated:
            return {'message': 'Review mise à jour avec succès'}, 200
        return {'message': 'Review non trouvée ou données invalides'}, 404

    @api.response(200, 'Review supprimée avec succès')
    @api.response(404, 'Review non trouvée')
    def delete(self, review_id):
        """Supprimer une review"""
        deleted = facade.HBnBFacade().delete_review(review_id)
        if deleted:
            return {'message': 'Review supprimée avec succès'}, 200
        return {'message': 'Review non trouvée'}, 404

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'Liste des reviews pour la place récupérée avec succès')
    @api.response(404, 'Place non trouvée')
    def get(self, place_id):
        """Récupérer toutes les reviews associées à une place"""
        reviews = facade.HBnBFacade().get_reviews_by_place(place_id)
        if reviews is not None:
            return reviews, 200
        return {'message': 'Place non trouvée'}, 404
