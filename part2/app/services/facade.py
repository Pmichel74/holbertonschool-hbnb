from uuid import uuid4

# Simulation d'une base de données avec un dictionnaire
users_db = {}

def get_users():
    """Récupère tous les utilisateurs"""
    return list(users_db.values())

def get_user(user_id):
    """Récupère un utilisateur par son ID"""
    return users_db.get(user_id)

def create_user(data):
    """Crée un nouvel utilisateur"""
    user_id = str(uuid4())
    user = {
        'id': user_id,
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'email': data['email']
    }
    users_db[user_id] = user
    return user

def update_user(user_id, data):
    """Met à jour un utilisateur existant"""
    if user_id not in users_db:
        return None
    
    user = users_db[user_id]
    user.update({
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'email': data['email']
    })
    return user
