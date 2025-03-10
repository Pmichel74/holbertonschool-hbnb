#!/usr/bin/python3
"""Initialisation des namespaces de l'API v1"""

def get_namespaces():
    """Retourne la liste des namespaces API"""
    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.reviews import api as reviews_ns
    
    return [users_ns, places_ns, auth_ns, amenities_ns, reviews_ns]
