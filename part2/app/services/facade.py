from uuid import uuid4

class Facade:
    def __init__(self):
        self.reviews_db = {}
        self.places_db = {}

    # Méthodes pour les utilisateurs
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

    # Méthodes pour les commodités
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

    def create_place(self, place_data):
        """Créer un nouveau place"""
        place_id = str(uuid4())
        
        # Valider le prix, la latitude et la longitude
        if place_data.get('price', 0) < 0:
            raise ValueError("Le prix ne peut pas être négatif")
        
        if not -90 <= place_data.get('latitude', 0) <= 90:
            raise ValueError("La latitude doit être entre -90 et 90")
            
        if not -180 <= place_data.get('longitude', 0) <= 180:
            raise ValueError("La longitude doit être entre -180 et 180")
        
        # Vérifier que le propriétaire existe
        if place_data.get('owner_id') and place_data['owner_id'] not in self.users_db:
            raise ValueError(f"Propriétaire avec ID {place_data['owner_id']} n'existe pas")
        
        # Initialiser les places_db si nécessaire
        if not hasattr(self, 'places_db'):
            self.places_db = {}
        
        # Créer l'objet place
        place = {
            'id': place_id,
            'title': place_data.get('title', ''),
            'description': place_data.get('description', ''),
            'price': place_data.get('price', 0.0),
            'latitude': place_data.get('latitude', 0.0),
            'longitude': place_data.get('longitude', 0.0),
            'owner_id': place_data.get('owner_id', ''),
            'amenities': place_data.get('amenities', [])
        }
        
        # Enregistrer dans la "base de données"
        self.places_db[place_id] = place
        return place

    def get_place(self, place_id):
        """Get a place by ID"""
        return self.places_db.get(place_id)

    def get_all_places(self):
        """Récupérer tous les places
        
        Returns:
            list: Liste de tous les places avec informations de base
        """
        # Vérifier que places_db existe
        if not hasattr(self, 'places_db'):
            self.places_db = {}
        
        return [
            {
                'id': place['id'],
                'title': place['title'],
                'latitude': place['latitude'],
                'longitude': place['longitude']
            }
            for place in self.places_db.values()
        ]

    def update_place(self, place_id, place_data):
        """Mettre à jour un place existant
        
        Args:
            place_id (str): ID du place à mettre à jour
            place_data (dict): Nouvelles données du place
            
        Returns:
            dict: Le place mis à jour, ou None si non trouvé
            
        Raises:
            ValueError: Si les données sont invalides
        """
        # Vérifier que places_db existe
        if not hasattr(self, 'places_db'):
            self.places_db = {}
        
        # Vérifier que le place existe
        if place_id not in self.places_db:
            return None
        
        place = self.places_db[place_id]
        
        # Valider les données mises à jour
        if 'price' in place_data and place_data['price'] < 0:
            raise ValueError("Le prix ne peut pas être négatif")
        
        if 'latitude' in place_data and not -90 <= place_data['latitude'] <= 90:
            raise ValueError("La latitude doit être entre -90 et 90")
            
        if 'longitude' in place_data and not -180 <= place_data['longitude'] <= 180:
            raise ValueError("La longitude doit être entre -180 et 180")
        
        # Vérifier que le propriétaire existe si mis à jour
        if 'owner_id' in place_data and place_data['owner_id'] not in self.users_db:
            raise ValueError(f"Propriétaire avec ID {place_data['owner_id']} n'existe pas")
        
        # Mettre à jour les attributs (sauf l'ID)
        for key, value in place_data.items():
            if key != 'id':
                place[key] = value
        
        return place

    def create_review(self, review_data):
        """Create a new review with validation"""
        if not all(key in review_data for key in ['text', 'rating', 'user_id', 'place_id']):
            raise ValueError("Missing required fields")
        
        if not isinstance(review_data['rating'], int) or not 1 <= review_data['rating'] <= 5:
            raise ValueError("Rating must be an integer between 1 and 5")
            
        review_id = str(uuid4())
        review = {
            'id': review_id,
            **review_data
        }
        self.reviews_db[review_id] = review
        return review

    def get_review(self, review_id):
        """Get a review by ID"""
        return self.reviews_db.get(review_id)

    def get_all_reviews(self):
        """Get all reviews"""
        return list(self.reviews_db.values())

    def update_review(self, review_id, review_data):
        """Update a review"""
        if review_id not in self.reviews_db:
            return None
        review = self.reviews_db[review_id]
        review.update(review_data)
        return review

    def delete_review(self, review_id):
        """Delete a review"""
        if review_id in self.reviews_db:
            del self.reviews_db[review_id]
            return True
        return False

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place"""
        return [
            review for review in self.reviews_db.values()
            if review.get('place_id') == place_id
        ]
