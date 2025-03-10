#!/usr/bin/python3
"""Middleware d'authentification"""
from functools import wraps
from flask import request
from app.services.auth_service import AuthService
from app.error_handlers import AuthError
from flask_restx import abort
from app.persistence.storage_engine import storage

# Initialiser le service d'auth avec le stockage
auth_service = AuthService(storage)

class AuthMiddleware:
    """Middleware pour gérer l'authentification via JWT"""
    
    @staticmethod
    def token_required(f):
        """Décorateur qui vérifie le token JWT dans les en-têtes de la requête"""
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            
            # Vérifier si le token est présent dans les en-têtes
            auth_header = request.headers.get('Authorization')
            if auth_header:
                if auth_header.startswith('Bearer '):
                    token = auth_header.split(' ')[1]
            
            if not token:
                abort(401, 'Token d\'authentification manquant')
            
            try:
                # Vérifier le token et récupérer l'ID utilisateur
                user_id = auth_service.verify_token(token)
                # Ajouter l'ID utilisateur aux arguments de la fonction
                kwargs['current_user_id'] = user_id
            except AuthError as e:
                abort(401, str(e))
            
            return f(*args, **kwargs)
        return decorated