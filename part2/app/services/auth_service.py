#!/usr/bin/python3
"""Service d'authentification"""
import datetime
import jwt
from flask import current_app
from app.error_handlers import AuthError

class AuthService:
    """Service pour gérer l'authentification"""
    
    def __init__(self, storage):
        """Initialise le service avec le stockage"""
        self.storage = storage
    
    def authenticate(self, email, password):
        """Authentifie un utilisateur et génère un token JWT"""
        # Importer User ici pour éviter les imports circulaires
        from app.models.user import User
        
        # Récupérer tous les utilisateurs
        users = self.storage.all(User)
        
        # Trouver l'utilisateur par email
        user = None
        for u in users:
            if u.email == email:
                user = u
                break
        
        # Vérifier si l'utilisateur existe et si le mot de passe correspond
        if not user or not user.check_password(password):
            raise AuthError("Email ou mot de passe invalide")
        
        # Générer le token JWT
        payload = {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])
        }
        token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
        
        # Construire la réponse
        return {
            'access_token': token,
            'token_type': 'bearer',
            'expires_in': current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
        }
    
    def verify_token(self, token):
        """Vérifie un token JWT et retourne l'ID de l'utilisateur"""
        try:
            payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            raise AuthError("Token expiré")
        except jwt.InvalidTokenError:
            raise AuthError("Token invalide")