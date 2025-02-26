from uuid import uuid4

# Simulation of a database using dictionaries
users_db = {}
amenities_db = {}

# ------------------ USERS MANAGEMENT ------------------

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

# ------------------ AMENITIES MANAGEMENT ------------------

def get_amenities():
    """Retrieve all amenities."""
    return list(amenities_db.values())

def get_amenity(amenity_id):
    """Retrieve an amenity by its ID."""
    return amenities_db.get(amenity_id)

def create_amenity(data):
    """Create a new amenity."""
    name = data.get("name")
    if not name:
        return None, "Invalid input data"

    amenity_id = str(uuid4())
    amenity = {
        "id": amenity_id,
        "name": name
    }
    amenities_db[amenity_id] = amenity
    return amenity, None

def update_amenity(amenity_id, data):
    """Update an existing amenity."""
    if amenity_id not in amenities_db:
        return None, "Amenity not found"
    
    name = data.get("name")
    if not name:
        return None, "Invalid input data"

    amenities_db[amenity_id]["name"] = name
    return amenities_db[amenity_id], None
