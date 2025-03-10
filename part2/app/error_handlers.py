#!/usr/bin/python3
"""Définitions et gestionnaires d'erreurs personnalisées"""
from flask import jsonify

class HBNBError(Exception):
    """Classe de base pour les erreurs personnalisées de HBNB"""
    pass

class ValidationError(HBNBError):
    """Erreur levée lors d'une validation échouée"""
    pass

class NotFoundError(HBNBError):
    """Erreur levée lorsqu'une ressource n'est pas trouvée"""
    pass

class AuthError(HBNBError):
    """Erreur levée lors d'un problème d'authentification"""
    pass

class StorageError(HBNBError):
    """Erreur levée lors d'un problème avec le stockage"""
    pass

def register_error_handlers(app):
    """Enregistre les gestionnaires d'erreurs dans l'application Flask"""
    
    @app.errorhandler(HBNBError)
    def handle_hbnb_error(error):
        """Gestionnaire pour les erreurs HBNB génériques"""
        response = {
            'error': str(error),
            'type': error.__class__.__name__
        }
        return jsonify(response), 500
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """Gestionnaire pour les erreurs de validation"""
        response = {
            'error': str(error),
            'type': 'ValidationError'
        }
        return jsonify(response), 400
    
    @app.errorhandler(NotFoundError)
    def handle_not_found_error(error):
        """Gestionnaire pour les erreurs de ressource non trouvée"""
        response = {
            'error': str(error),
            'type': 'NotFoundError'
        }
        return jsonify(response), 404
    
    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        """Gestionnaire pour les erreurs d'authentification"""
        response = {
            'error': str(error),
            'type': 'AuthError'
        }
        return jsonify(response), 401
    
    @app.errorhandler(404)
    def not_found(e):
        """Gestionnaire pour les routes non trouvées"""
        response = {
            'error': 'Not Found',
            'message': 'The requested URL was not found on the server.'
        }
        return jsonify(response), 404
