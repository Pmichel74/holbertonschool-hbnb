from uuid import uuid4

# Simulation of a database using a dictionary
users_db = {}

def get_users():
    """Retrieve all users.
    
    Returns:
        list: List of all users in the database.
    """
    return list(users_db.values())

def get_user(user_id):
    """Retrieve a user by their ID.
    
    Args:
        user_id (str): Unique identifier of the user.
    
    Returns:
        dict: User data if found, None otherwise.
    """
    return users_db.get(user_id)

def create_user(data):
    """Create a new user.
    
    Args:
        data (dict): Dictionary containing user data
                     (first_name, last_name, email).
    
    Returns:
        dict: The newly created user data.
    """
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
    """Update an existing user.
    
    Args:
        user_id (str): Unique identifier of the user to update.
        data (dict): New user data (first_name, last_name, email).
    
    Returns:
        dict: Updated user data if user exists, None otherwise.
    """
    if user_id not in users_db:
        return None
    
    user = users_db[user_id]
    user.update({
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'email': data['email']
    })
    return user
