#!/usr/bin/python3
"""Routes API pour la gestion des équipements"""
from flask import request
from flask_restx import Namespace, Resource, fields
from app.error_handlers import ValidationError, NotFoundError
from app.persistence.storage_engine import storage

api = Namespace('amenities', description='Opérations sur les équipements')

# Modèles Swagger pour la documentation de l'API
amenity_input_model = api.model('AmenityInput', {
    'name': fields.String(required=True, description='Nom de l\'équipement'),
})

amenity_model = api.model('Amenity', {
    'id': fields.String(description='ID unique'),
    'name': fields.String(description='Nom de l\'équipement'),
    'created_at': fields.DateTime(description='Date de création'),
    'updated_at': fields.DateTime(description='Date de mise à jour')
})

# Initialiser le service
from app.services.amenity_service import AmenityService
amenity_service = AmenityService(storage)

@api.route('/')
class AmenityList(Resource):
    """Gestion de la collection d'équipements"""
    
    @api.doc('list_amenities', 
             responses={
                 200: 'Success',
                 500: 'Internal Server Error'
             })
    @api.marshal_list_with(amenity_model)
    def get(self):
        """Liste tous les équipements"""
        try:
            amenities = amenity_service.get_all_amenities()
            return [amenity.to_dict() for amenity in amenities]
        except Exception as e:
            api.abort(500, str(e))

    @api.doc('create_amenity',
             responses={
                 201: 'Amenity Created',
                 400: 'Validation Error',
                 500: 'Internal Server Error'
             })
    @api.expect(amenity_input_model)
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        """Crée un nouvel équipement"""
        try:
            data = request.get_json()
            
            if not data:
                api.abort(400, "Aucune donnée fournie")
                
            if 'name' not in data or not data['name']:
                api.abort(400, "Le nom de l'équipement est obligatoire")
                
            amenity = amenity_service.create_amenity(data)
            return amenity.to_dict(), 201
        except ValidationError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, str(e))

@api.route('/<amenity_id>')
@api.param('amenity_id', 'L\'identifiant de l\'équipement')
@api.response(404, 'Équipement non trouvé')
class AmenityResource(Resource):
    """Gestion d'un équipement spécifique"""
    
    @api.doc('get_amenity',
             responses={
                 200: 'Success',
                 404: 'Amenity Not Found',
                 500: 'Internal Server Error'
             })
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Récupère un équipement par son ID"""
        try:
            amenity = amenity_service.get_amenity(amenity_id)
            if not amenity:
                api.abort(404, f"Équipement {amenity_id} non trouvé")
            return amenity.to_dict()
        except NotFoundError as e:
            api.abort(404, str(e))
        except Exception as e:
            api.abort(500, str(e))

    @api.doc('update_amenity',
             responses={
                 200: 'Success',
                 400: 'Validation Error',
                 404: 'Amenity Not Found',
                 500: 'Internal Server Error'
             })
    @api.expect(amenity_input_model)
    @api.marshal_with(amenity_model)
    def put(self, amenity_id):
        """Met à jour un équipement"""
        try:
            data = request.get_json()
            
            if not data:
                api.abort(400, "Aucune donnée fournie")
                
            updated_amenity = amenity_service.update_amenity(amenity_id, data)
            return updated_amenity.to_dict()
        except NotFoundError as e:
            api.abort(404, str(e))
        except ValidationError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, str(e))

