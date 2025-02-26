from uuid import uuid4
from app.models.amenity import Amenity
from app.persistence.repository import AmenityRepository

# Simulation d'une base de données
users_db = {}

# Crée une instance d'AmenityRepository pour gérer les commodités
amenity_repo = AmenityRepository()

# ------------------- Gestion des UTILISATEURS -------------------

def get_users():
    """Retrieve all users."""
    return list(users_db.values())

def get_user(user_id):
    """Retrieve a user by their ID."""
    return users_db.get(user_id)

def create_user(data):
    """Create a new user."""
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
    """Update an existing user."""
    if user_id not in users_db:
        return None
    
    user = users_db[user_id]
    user.update({
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'email': data['email']
    })
    return user

# ------------------- Gestion des COMMODITÉS (Amenities) -------------------

def get_all_amenities():
    """Retrieve all amenities."""
    return [amenity.to_dict() for amenity in amenity_repo.get_all()]

def get_amenity(amenity_id):
    """Retrieve an amenity by ID."""
    amenity = amenity_repo.get(amenity_id)
    return amenity.to_dict() if amenity else None

def create_amenity(data):
    """Create a new amenity and add it to the database."""
    try:
        amenity = Amenity(name=data['name'])
    except ValueError as e:
        return {"error": str(e)}

    amenity_repo.add(amenity)  # Utilise le repository pour ajouter la commodité
    return amenity.to_dict()

def update_amenity(amenity_id, data):
    """Update an existing amenity."""
    amenity = amenity_repo.get(amenity_id)
    if not amenity:
        return None

    try:
        amenity.validate_name(data['name'])
        amenity.name = data['name']
    except ValueError as e:
        return {"error": str(e)}

    amenity_repo.update(amenity_id, data)  # Utilise le repository pour mettre à jour la commodité
    return amenity.to_dict()
