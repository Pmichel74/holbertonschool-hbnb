# app/business_logic/user_logic.py
from app.db import get_user_by_id, get_all_users, add_user, delete_user

def get_user_by_id(user_id):
    """Récupérer un utilisateur par ID"""
    return get_user_by_id(user_id)

def update_user(user_id, data):
    """Mettre à jour un utilisateur"""
    user = get_user_by_id(user_id)
    if not user:
        return None

    if 'first_name' in data:
        user.first_name = data['first_name']
    
    if 'last_name' in data:
        user.last_name = data['last_name']
    
    if 'email' in data:
        user.email = data['email']
    
    if 'is_admin' in data:
        user.is_admin = data['is_admin']

    # Simuler la mise à jour dans la base de données
    add_user(user)  # On remplace simplement l'ancien utilisateur par le nouveau
    return user

def get_all_users():
    """Récupérer tous les utilisateurs"""
    return get_all_users()
