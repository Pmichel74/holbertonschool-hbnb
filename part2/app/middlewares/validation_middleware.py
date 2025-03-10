#!/usr/bin/python3
"""Middleware de validation des données"""
from functools import wraps
from flask import request
import re
from app.error_handlers import ValidationError

class ValidationMiddleware:
    """Middleware pour la validation des données reçues"""
    
    @staticmethod
    def validate_user_data():
        """Décorateur pour valider les données utilisateur"""
        def decorator(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                data = request.get_json()
                
                # Vérification de la présence des champs obligatoires
                if not data:
                    raise ValidationError("Aucune donnée fournie")
                
                if request.method == 'POST':
                    if 'email' not in data or not data['email']:
                        raise ValidationError("L'email est obligatoire")
                    
                    if 'password' not in data or not data['password']:
                        raise ValidationError("Le mot de passe est obligatoire")
                
                # Validation du format d'email s'il est présent
                if 'email' in data and data['email']:
                    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                    if not re.match(email_pattern, data['email']):
                        raise ValidationError("Format d'email invalide")
                
                # Validation de la complexité du mot de passe s'il est présent
                if 'password' in data and data['password']:
                    if len(data['password']) < 6:
                        raise ValidationError("Le mot de passe doit contenir au moins 6 caractères")
                
                return f(*args, **kwargs)
            return decorated
        return decorator
    
    @staticmethod
    def validate_place_data():
        """Décorateur pour valider les données de lieu"""
        def decorator(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                data = request.get_json()
                
                # Vérification de la présence des champs obligatoires
                if not data:
                    raise ValidationError("Aucune donnée fournie")
                
                # Pour la création, ces champs sont obligatoires
                if request.method == 'POST':
                    if 'name' not in data or not data['name']:
                        raise ValidationError("Le nom du lieu est obligatoire")
                    
                    if 'user_id' not in data or not data['user_id']:
                        raise ValidationError("L'ID de l'utilisateur est obligatoire")
                
                # Validation des types numériques
                if 'price_by_night' in data and data['price_by_night'] is not None:
                    try:
                        price = float(data['price_by_night'])
                        if price < 0:
                            raise ValidationError("Le prix par nuit doit être positif")
                    except (ValueError, TypeError):
                        raise ValidationError("Le prix par nuit doit être un nombre")
                
                # Validation que amenity_ids est une liste si présent
                if 'amenity_ids' in data:
                    if not isinstance(data['amenity_ids'], list):
                        raise ValidationError("amenity_ids doit être une liste")
                
                return f(*args, **kwargs)
            return decorated
        return decorator

    @staticmethod
    def validate_review_data():
        """Décorateur pour valider les données d'avis"""
        def decorator(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                data = request.get_json()
                
                # Vérification de la présence des champs obligatoires
                if not data:
                    raise ValidationError("Aucune donnée fournie")
                
                # Pour la création, ces champs sont obligatoires
                if request.method == 'POST':
                    if 'text' not in data or not data['text']:
                        raise ValidationError("Le texte de l'avis est obligatoire")
                    
                    if 'user_id' not in data or not data['user_id']:
                        raise ValidationError("L'ID de l'utilisateur est obligatoire")
                    
                    if 'place_id' not in data or not data['place_id']:
                        raise ValidationError("L'ID du lieu est obligatoire")
                
                # Validation du rating s'il est présent
                if 'rating' in data:
                    try:
                        rating = int(data['rating'])
                        if rating < 0 or rating > 5:
                            raise ValidationError("La note doit être entre 0 et 5")
                    except (ValueError, TypeError):
                        raise ValidationError("La note doit être un nombre entier")
                
                return f(*args, **kwargs)
            return decorated
        return decorator
