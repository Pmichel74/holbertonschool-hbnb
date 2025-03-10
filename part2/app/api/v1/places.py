#!/usr/bin/python3
"""Routes API pour la gestion des lieux"""
from flask import request
from flask_restx import Namespace, Resource, fields
from app.middlewares.validation_middleware import ValidationMiddleware
from app.error_handlers import ValidationError, NotFoundError
from app.persistence.storage_engine import storage

api = Namespace('places', description='Opérations sur les lieux')

# S'assurer que le modèle Swagger inclut correctement amenity_ids
place_input_model = api.model('PlaceInput', {
    'name': fields.String(required=True, description='Nom du lieu'),
    'user_id': fields.String(required=True, description='ID du propriétaire'),
    'description': fields.String(description='Description du lieu'),
    'price_by_night': fields.Float(description='Prix par nuit'),
    'latitude': fields.Float(description='Latitude'),
    'longitude': fields.Float(description='Longitude'),
    'amenity_ids': fields.List(fields.String, description='Liste des ID des équipements')
})

place_update_model = api.model('PlaceUpdate', {
    'name': fields.String(description='Nom du lieu'),
    'description': fields.String(description='Description du lieu'),
    'price_by_night': fields.Float(description='Prix par nuit'),
    'latitude': fields.Float(description='Latitude'),
    'longitude': fields.Float(description='Longitude'),
    'amenity_ids': fields.List(fields.String, description='Liste des ID des équipements')
})

place_model = api.model('Place', {
    'id': fields.String(description='ID unique'),
    'name': fields.String(description='Nom du lieu'),
    'user_id': fields.String(description='ID du propriétaire'),
    'description': fields.String(description='Description du lieu'),
    'price_by_night': fields.Float(description='Prix par nuit'),
    'latitude': fields.Float(description='Latitude'),
    'longitude': fields.Float(description='Longitude'),
    'amenity_ids': fields.List(fields.String, description='Liste des ID des équipements'),
    'created_at': fields.DateTime(description='Date de création'),
    'updated_at': fields.DateTime(description='Date de mise à jour')
})

# Initialiser les services - nous utilisons ici une classe locale pour éviter les dépendances circulaires
class UserServiceTemp:
    """Version simplifiée de UserService pour vérifier si un utilisateur existe"""
    def __init__(self, storage):
        self.storage = storage
        
    def get(self, user_id):
        from app.models.user import User
        return self.storage.get(User, user_id)

# Créer les services
from app.services.place_service import PlaceService
place_service = PlaceService(storage)
user_service = UserServiceTemp(storage)

@api.route('/')
class PlaceList(Resource):
    """Gestion de la collection de lieux"""
    
    @api.doc('list_places', 
             responses={
                 200: 'Success',
                 500: 'Internal Server Error'
             })
    @api.marshal_list_with(place_model)
    def get(self):
        """Liste tous les lieux"""
        try:
            places = place_service.get_all_places()
            return [place.to_dict() for place in places]
        except Exception as e:
            api.abort(500, str(e))

    @api.doc('create_place',
             responses={
                 201: 'Place Created',
                 400: 'Validation Error',
                 404: 'User Not Found',
                 500: 'Internal Server Error'
             })
    @api.expect(place_input_model)
    @api.marshal_with(place_model, code=201)
    @ValidationMiddleware.validate_place_data()
    def post(self):
        """Crée un nouveau lieu"""
        try:
            data = request.get_json()
            
            # Vérifier si l'utilisateur existe
            user = user_service.get(data['user_id'])
            if not user:
                api.abort(404, f"Utilisateur {data['user_id']} non trouvé")
                
            place = place_service.create_place(data)
            return place.to_dict(), 201
        except ValidationError as e:
            api.abort(400, str(e))
        except NotFoundError as e:
            api.abort(404, str(e))
        except Exception as e:
            api.abort(500, str(e))

@api.route('/<place_id>')
@api.param('place_id', 'L\'identifiant du lieu')
@api.response(404, 'Lieu non trouvé')
class PlaceResource(Resource):
    """Gestion d'un lieu spécifique"""
    
    @api.doc('get_place',
             responses={
                 200: 'Success',
                 404: 'Place Not Found',
                 500: 'Internal Server Error'
             })
    @api.marshal_with(place_model)
    def get(self, place_id):
        """Récupère un lieu par son ID"""
        try:
            place = place_service.get_place(place_id)
            if not place:
                api.abort(404, f"Lieu {place_id} non trouvé")
            return place.to_dict()
        except NotFoundError as e:
            api.abort(404, str(e))
        except Exception as e:
            api.abort(500, str(e))

    @api.doc('update_place',
             responses={
                 200: 'Success',
                 400: 'Validation Error',
                 404: 'Place Not Found',
                 500: 'Internal Server Error'
             })
    @api.expect(place_update_model)
    @api.marshal_with(place_model)
    @ValidationMiddleware.validate_place_data()
    def put(self, place_id):
        """Met à jour un lieu"""
        try:
            data = request.get_json()
            updated_place = place_service.update_place(place_id, data)
            return updated_place.to_dict()
        except NotFoundError as e:
            api.abort(404, str(e))
        except ValidationError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, str(e))

@api.route('/user/<user_id>')
@api.param('user_id', 'L\'identifiant de l\'utilisateur')
class UserPlaces(Resource):
    """Gestion des lieux d'un utilisateur spécifique"""
    
    @api.doc('get_user_places',
             responses={
                 200: 'Success',
                 404: 'User Not Found',
                 500: 'Internal Server Error'
             })
    @api.marshal_list_with(place_model)
    def get(self, user_id):
        """Récupère tous les lieux d'un utilisateur"""
        try:
            user = user_service.get(user_id)
            if not user:
                api.abort(404, f"Utilisateur {user_id} non trouvé")
                
            places = place_service.get_places_by_user(user_id)
            return [place.to_dict() for place in places]
        except NotFoundError as e:
            api.abort(404, str(e))
        except Exception as e:
            api.abort(500, str(e))
