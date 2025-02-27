from uuid import uuid4

class Facade:
    def __init__(self):
        # Initialisation des "bases de données"
        self.users_db = {}
        self.amenities_db = {}

    # Méthodes pour les utilisateurs (inchangées)
    def get_users(self):
        return list(self.users_db.values())

    def get_user(self, user_id):
        return self.users_db.get(user_id)

    def create_user(self, data):
        user_id = str(uuid4())
        user = {
            'id': user_id,
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email']
        }
        self.users_db[user_id] = user
        return user

    def update_user(self, user_id, data):
        if user_id not in self.users_db:
            return None
        
        user = self.users_db[user_id]
        user.update({
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email']
        })
        return user

    # Méthodes pour les commodités (corrigées)
    def create_amenity(self, amenity_data):
        """Create a new amenity
        
        Args:
            amenity_data (dict): Dictionary containing amenity data (name)
                
        Returns:
            dict: The newly created amenity
                
        Raises:
            ValueError: If the amenity data is invalid
        """
        if not amenity_data.get('name'):
            raise ValueError("Amenity name is required")
                
        amenity_id = str(uuid4())
        amenity = {
            'id': amenity_id,
            'name': amenity_data['name']
        }
        self.amenities_db[amenity_id] = amenity
        return amenity

    def get_amenity(self, amenity_id):
        """Get amenity by ID
        
        Args:
            amenity_id (str): The ID of the amenity to retrieve
                
        Returns:
            dict: The amenity data if found
                
        Raises:
            ValueError: If the amenity is not found
        """
        amenity = self.amenities_db.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")
        return amenity

    def get_all_amenities(self):
        """Get all amenities
        
        Returns:
            list: List of all amenities
        """
        return list(self.amenities_db.values())

    def update_amenity(self, amenity_id, amenity_data):
        """Update an existing amenity
        
        Args:
            amenity_id (str): The ID of the amenity to update
            amenity_data (dict): New amenity data (name)
                
        Returns:
            dict: The updated amenity data
                
        Raises:
            ValueError: If the amenity is not found or data is invalid
        """
        amenity = self.get_amenity(amenity_id)  # This will raise ValueError if not found
        
        if not amenity_data.get('name'):
            raise ValueError("Amenity name is required")
                
        amenity['name'] = amenity_data['name']
        return amenity
