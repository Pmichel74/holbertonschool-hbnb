#!/usr/bin/python3
"""Routes API pour l'authentification"""
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.auth_service import AuthService
from app.error_handlers import ValidationError, AuthError
from app.persistence.storage_engine import storage

api = Namespace('auth', description='Opérations d\'authentification')

# Modèles Swagger pour la documentation de l'API
login_model = api.model('Login', {
    'email': fields.String(required=True, description='Email de l\'utilisateur'),
    'password': fields.String(required=True, description='Mot de passe')
})

token_model = api.model('Token', {
    'access_token': fields.String(description='Token d\'accès JWT'),
    'token_type': fields.String(default='bearer'),
    'expires_in': fields.Integer(description='Durée de validité du token en secondes')
})

# Service d'authentification
auth_service = AuthService(storage)

@api.route('/login')
class Login(Resource):
    @api.doc('login',
             responses={
                 200: 'Login successful',
                 401: 'Authentication failed',
                 400: 'Validation Error',
                 500: 'Internal Server Error'
             })
    @api.expect(login_model)
    @api.marshal_with(token_model)
    def post(self):
        """Authentifie un utilisateur et retourne un token JWT"""
        try:
            data = request.get_json()
            
            if not data:
                api.abort(400, "Aucune donnée fournie")
                
            if 'email' not in data or not data['email']:
                api.abort(400, "Email requis")
                
            if 'password' not in data or not data['password']:
                api.abort(400, "Mot de passe requis")
                
            token_data = auth_service.authenticate(data['email'], data['password'])
            return token_data
        except AuthError as e:
            api.abort(401, str(e))
        except Exception as e:
            api.abort(500, str(e))