from uuid import uuid4
from datetime import datetime
from app.models.place import Place
from app.models.user import User
from app.models.amenity import Amenity

class Facade:
    def __init__(self):
        """Initialiser les bases de données"""
        self.users_db = {}
        self.places_db = {}
        self.amenities_db = {}
        self.reviews_db = {}
        
        # Commenter ou supprimer cette ligne :
        # self._create_test_users()

    def _create_test_users(self):
        """Créer des utilisateurs de test pour le développement"""
        test_users = [
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe@example.com',
                'is_admin': True,
                'is_test_user': True  # Ajouter ce flag
            },
            {
                'first_name': 'Jane',
                'last_name': 'Smith',
                'email': 'jane.smith@example.com',
                'is_test_user': True  # Ajouter ce flag
            }
        ]
        
        # Créer les utilisateurs
        for user_data in test_users:
            self.create_user(user_data)

    # Méthodes utilisateur
    def get_users(self):
        """Obtenir tous les utilisateurs non-test"""
        # Filtrer les utilisateurs de test
        return [user for user in self.users_db.values() if not user.get('is_test_user', False)]

    def get_user(self, user_id):
        return self.users_db.get(user_id)

    def create_user(self, user_data):
        """Créer un nouvel utilisateur"""
        # Code de validation...
        
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            is_admin=user_data.get('is_admin', False)
        )
        
        # S'assurer que tous les champs sont inclus dans le dictionnaire
        user_dict = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin,
            'created_at': user.created_at.isoformat() if hasattr(user.created_at, 'isoformat') else user.created_at,
            'updated_at': user.updated_at.isoformat() if hasattr(user.updated_at, 'isoformat') else user.updated_at
        }
        
        self.users_db[user.id] = user_dict
        return user_dict

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

    def debug_print_user(self, user_id):
        """Utilitaire de débogage pour imprimer les données utilisateur"""
        if not hasattr(self, 'users_db'):
            print("users_db n'existe pas !")
            return
            
        if user_id not in self.users_db:
            print(f"Utilisateur {user_id} non trouvé dans users_db !")
            return
            
        user = self.users_db[user_id]
        print(f"Données de l'utilisateur {user_id} :")
        for key, value in user.items():
            print(f"  {key}: {value}")

    def list_users_debug(self):
        """Afficher tous les utilisateurs pour le débogage"""
        print("\n--- DÉBOGAGE : LISTE DES UTILISATEURS ---")
        if not hasattr(self, 'users_db'):
            print("users_db n'existe pas !")
            return []
            
        if not self.users_db:
            print("users_db est vide !")
            return []
            
        for user_id, user in self.users_db.items():
            print(f"User ID: {user_id}")
            print(f"  First name: {user.get('first_name', '(missing)')}")
            print(f"  Last name: {user.get('last_name', '(missing)')}")
            print(f"  Email: {user.get('email', '(missing)')}")
            print("---")
        
        return list(self.users_db.values())

    # Methods for amenities
    def create_amenity(self, amenity_data):
        """Create a new amenity
        
        Args:
            amenity_data (dict): Amenity data containing name
            
        Returns:
            dict: The created amenity with all attributes
        """
        if not amenity_data.get('name'):
            raise ValueError("Name is required")
        
        # Initialize amenities_db if needed
        if not hasattr(self, 'amenities_db'):
            self.amenities_db = {}
        
        # Create new amenity with timestamps
        amenity_id = str(uuid4())
        current_time = datetime.now().isoformat()
        
        amenity = {
            'id': amenity_id,
            'name': amenity_data['name'],
            'created_at': current_time,
            'updated_at': current_time,
            'places': []  # Empty list of initially associated places
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
        # Make sure amenities_db exists
        if not hasattr(self, 'amenities_db'):
            self.amenities_db = {}
        
        # Ensure each amenity has a places field
        for amenity_id, amenity in self.amenities_db.items():
            if 'places' not in amenity:
                amenity['places'] = []
        
        return list(self.amenities_db.values())

    def update_amenity(self, amenity_id, amenity_data):
        """Update an existing amenity
        
        Args:
            amenity_id (str): ID of the amenity to update
            amenity_data (dict): New amenity data
        
        Returns:
            dict: Updated amenity
        
        Raises:
            ValueError: If amenity not found or data is invalid
        """
        # Verify amenity exists
        if not hasattr(self, 'amenities_db') or amenity_id not in self.amenities_db:
            raise ValueError("Amenity not found")
        
        # Validate name is not empty if provided
        if 'name' in amenity_data and not amenity_data['name'].strip():
            raise ValueError("Name is required and cannot be empty")
        
        amenity = self.amenities_db[amenity_id]
        
        # Update name if provided
        if 'name' in amenity_data:
            amenity['name'] = amenity_data['name']
        
        # Update the timestamp
        amenity['updated_at'] = datetime.now().isoformat()
        
        # Ensure the places field exists
        if 'places' not in amenity:
            amenity['places'] = []
        
        return amenity

    def create_place(self, place_data):
        """Create a new place
        
        Args:
            place_data (dict): Data for the place to create
            
        Returns:
            dict: The created place
            
        Raises:
            ValueError: If the data is invalid
        """
        # Title validation (required according to the requirements)
        if not place_data.get('title'):
            raise ValueError("Title is required")
        
        if len(place_data.get('title', '')) > 100:
            raise ValueError("Title must not exceed 100 characters")
            
        # Owner validation - REQUIRED and MUST EXIST
        owner_id = place_data.get('owner_id')
        if not owner_id:
            raise ValueError("Owner ID is required")
            
        # Initialize users_db if needed
        if not hasattr(self, 'users_db'):
            self.users_db = {}
            
        # Check if owner exists
        if owner_id not in self.users_db:
            raise ValueError(f"Owner with ID {owner_id} does not exist")
        
        # Price validation (positive if specified)
        if 'price' in place_data and float(place_data['price']) < 0:
            raise ValueError("Price cannot be negative")
            
        # Latitude and longitude validation
        if 'latitude' in place_data and not -90 <= float(place_data['latitude']) <= 90:
            raise ValueError("Latitude must be between -90 and 90")
            
        if 'longitude' in place_data and not -180 <= float(place_data['longitude']) <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        
        try:
            # Extract the amenities
            amenity_ids = place_data.get('amenities', [])
            
            # Make sure amenities_db exists
            if not hasattr(self, 'amenities_db'):
                self.amenities_db = {}
            
            # Transform IDs into complete amenity objects
            amenities_objects = []
            for amenity_id in amenity_ids:
                if amenity_id in self.amenities_db:
                    # Get the amenity name
                    amenity = self.amenities_db[amenity_id]
                    amenities_objects.append({
                        'id': amenity_id,
                        'name': amenity.get('name', 'Unknown amenity')
                    })
            
            # Generate a new ID
            place_id = str(uuid4())
            
            # Get owner information
            owner = self.users_db[owner_id]
            
            # Create place object
            place = {
                'id': place_id,
                'title': place_data.get('title', 'Untitled'),
                'description': place_data.get('description', ''),
                'price': float(place_data.get('price', 0.0)),
                'latitude': float(place_data.get('latitude', 0.0)),
                'longitude': float(place_data.get('longitude', 0.0)),
                'owner_id': owner_id,  # Keep this for internal reference
                'amenities': amenities_objects,  # To display the full name of amenities
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                # Add owner details for API response
                'owner': {
                    'id': owner_id,
                    'first_name': owner.get('first_name', ''),
                    'last_name': owner.get('last_name', ''),
                    'email': owner.get('email', '')
                }
            }
            
            # Ensure places_db exists
            if not hasattr(self, 'places_db'):
                self.places_db = {}
            
            # Store place
            self.places_db[place_id] = place
            return place
        except Exception as e:
            print(f"Error in create_place: {str(e)}")
            raise ValueError(f"Failed to create place: {str(e)}")

    def get_place(self, place_id):
        """Get a place by its ID"""
        if not hasattr(self, 'places_db'):
            self.places_db = {}
        
        if place_id not in self.places_db:
            return None
        
        place = self.places_db[place_id].copy()
        
        # Handle owner like you already do
        owner_id = place.get('owner_id')
        if owner_id and owner_id in self.users_db:
            owner = self.users_db[owner_id]
            place['owner'] = {
                'id': owner_id,
                'first_name': owner.get('first_name', '(missing)'),
                'last_name': owner.get('last_name', '(missing)'),
                'email': owner.get('email', '(missing)')
            }
        else:
            place['owner'] = {
                'id': owner_id or '',
                'first_name': '(unknown)',
                'last_name': '(unknown)',
                'email': '(unknown)'
            }
        
        # NEW CODE: Transform amenity IDs into complete objects
        amenity_ids = place.get('amenities', [])
        amenities_objects = []
        
        # Make sure amenities_db exists
        if not hasattr(self, 'amenities_db'):
            self.amenities_db = {}
        
        # If place is a dictionary, use dictionary access instead of attribute access
        if isinstance(place, dict):
            place_amenity_id = place.get('amenity_id')
        else:
            place_amenity_id = place.amenity_id

        # Now compare using the correctly accessed amenity_id
        for amenity in self.amenities_db:
            if isinstance(amenity, dict):
                amenity_id = amenity.get('id')
            else:
                amenity_id = amenity

            if amenity_id == place_amenity_id:
                # Do something with the amenity
                pass
        
        return place

    def get_all_places(self):
        """Get all places with full details
        
        Returns:
            list: List of all places with complete information
        """
        # Reuse get_places() which already works correctly
        return self.get_places()

    def update_place(self, place_id, place_data):
        """Update an existing place"""
        # Check that places_db exists
        if not hasattr(self, 'places_db'):
            self.places_db = {}
        
        # Check if the place exists
        if place_id not in self.places_db:
            return None
        
        place = self.places_db[place_id]
        
        # Validate updated data
        if 'price' in place_data and place_data['price'] < 0:
            raise ValueError("Price cannot be negative")
        
        if 'latitude' in place_data and not -90 <= place_data['latitude'] <= 90:
            raise ValueError("Latitude must be between -90 and 90")
            
        if 'longitude' in place_data and not -180 <= place_data['longitude'] <= 180:
            raise ValueError("Longitude must be between -180 et 180")
        
        # Check if owner_id is being updated and if the new owner exists
        owner_id = place_data.get('owner_id', place.get('owner_id'))
        if 'owner_id' in place_data and place_data['owner_id'] not in self.users_db:
            raise ValueError(f"Owner with ID {place_data['owner_id']} does not exist")
        
        # Update attributes (except ID)
        for key, value in place_data.items():
            if key != 'id':
                place[key] = value
        
        # Update timestamp
        place['updated_at'] = datetime.now().isoformat()
        
        # Update owner information after possible owner_id change
        if owner_id and owner_id in self.users_db:
            owner = self.users_db[owner_id]
            place['owner'] = {
                'id': owner_id,
                'first_name': owner.get('first_name', ''),
                'last_name': owner.get('last_name', ''),
                'email': owner.get('email', '')
            }
        
        # Handle amenities if they are updated
        if 'amenities' in place_data:
            # Make sure amenities_db exists
            if not hasattr(self, 'amenities_db'):
                self.amenities_db = {}
            
            # Transform amenity IDs into complete objects for API response
            amenity_ids = place_data['amenities']
            amenities_objects = []
            
            for amenity_id in amenity_ids:
                if amenity_id in self.amenities_db:
                    # Récupérer l'amenity de la base de données
                    amenity = self.amenities_db[amenity_id]
                    
                    # Créer un objet complet pour la réponse API
                    amenity_object = {
                        'id': amenity_id,
                        'name': amenity.get('name', 'Unknown amenity'),
                        'created_at': amenity.get('created_at', datetime.now().isoformat()),
                        'updated_at': amenity.get('updated_at', datetime.now().isoformat())
                    }
                    
                    amenities_objects.append(amenity_object)
                    
                    # Mettre à jour les références croisées
                    if 'places' not in amenity:
                        amenity['places'] = []
                    if place_id not in amenity['places']:
                        amenity['places'].append(place_id)
            
            # Mettre à jour place avec les objets amenities
            place['amenities'] = amenities_objects
        
        return place

    def delete_place(self, place_id):
        """Delete a place by its ID"""
        # Initialize places_db if necessary
        if not hasattr(self, 'places_db'):
            self.places_db = {}
        
        # Check if the place exists
        if place_id not in self.places_db:
            return False
        
        # Delete the place
        del self.places_db[place_id]
        return True

    def create_review(self, review_data):
        """Create a new review
        
        Args:
            review_data (dict): Review data including text, rating, user_id, place_id
                
        Returns:
            dict: The newly created review
            
        Raises:
            ValueError: If the review data is invalid
        """
        # Validate user_id
        if not review_data.get('user_id') or review_data['user_id'] not in self.users_db:
            raise ValueError(f"User with ID {review_data.get('user_id')} does not exist")
        
        # Validate place_id
        if not hasattr(self, 'places_db'):
            self.places_db = {}
        
        if not review_data.get('place_id') or review_data['place_id'] not in self.places_db:
            raise ValueError(f"Place with ID {review_data.get('place_id')} does not exist")
        
        # Validate rating
        if 'rating' in review_data:
            try:
                rating = int(review_data['rating'])
                if not 1 <= rating <= 5:
                    raise ValueError("Rating must be between 1 and 5")
                review_data['rating'] = rating
            except (ValueError, TypeError):
                raise ValueError("Rating must be an integer between 1 and 5")
        
        # Validate text
        if not review_data.get('text'):
            raise ValueError("Review text is required")
        
        # Initialize reviews_db if needed
        if not hasattr(self, 'reviews_db'):
            self.reviews_db = {}
        
        # Create review object
        review_id = str(uuid4())
        current_time = datetime.now().isoformat()
        
        review = {
            'id': review_id,
            'text': review_data.get('text', ''),
            'rating': review_data.get('rating', 0),
            'user_id': review_data.get('user_id', ''),
            'place_id': review_data.get('place_id', ''),
            'created_at': current_time,
            'updated_at': current_time
        }
        
        # Save to "database"
        self.reviews_db[review_id] = review
        return review

    def get_review(self, review_id):
        """Get review by ID
        
        Args:
            review_id (str): ID of the review to retrieve
            
        Returns:
            dict: The review data if found, or None if not found
        """
        # Initialize reviews_db if needed
        if not hasattr(self, 'reviews_db'):
            self.reviews_db = {}
        
        return self.reviews_db.get(review_id)

    def get_all_reviews(self):
        """Get all reviews
        
        Returns:
            list: List of all reviews
        """
        # Initialize reviews_db if needed
        if not hasattr(self, 'reviews_db'):
            self.reviews_db = {}
        
        return list(self.reviews_db.values())

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place
        
        Args:
            place_id (str): ID of the place
            
        Returns:
            list: List of reviews for this place
            
        Raises:
            ValueError: If the place does not exist
        """
        # Validate place exists
        if not hasattr(self, 'places_db'):
            self.places_db = {}
        
        if place_id not in self.places_db:
            raise ValueError(f"Place with ID {place_id} does not exist")
        
        # Initialize reviews_db if needed
        if not hasattr(self, 'reviews_db'):
            self.reviews_db = {}
        
        # Filter reviews by place_id
        return [
            review for review in self.reviews_db.values()
            if review.get('place_id') == place_id
        ]

    def update_review(self, review_id, review_data):
        """Update an existing review
        
        Args:
            review_id (str): ID of the review to update
            review_data (dict): New review data
            
        Returns:
            dict: The updated review, or None if not found
            
        Raises:
            ValueError: If the data is invalid
        """
        # Initialize reviews_db if needed
        if not hasattr(self, 'reviews_db'):
            self.reviews_db = {}
        
        # Check if review exists
        if review_id not in self.reviews_db:
            return None
        
        review = self.reviews_db[review_id]
        
        # Prevent changing user_id or place_id
        if 'user_id' in review_data and review_data['user_id'] != review['user_id']:
            raise ValueError("User ID cannot be changed in a review update")
            
        if 'place_id' in review_data and review_data['place_id'] != review['place_id']:
            raise ValueError("Place ID cannot be changed in a review update")
        
        # Validate rating if provided
        if 'rating' in review_data:
            try:
                rating = int(review_data['rating'])
                if not 1 <= rating <= 5:
                    raise ValueError("Rating must be between 1 and 5")
                review_data['rating'] = rating
            except (ValueError, TypeError):
                raise ValueError("Rating must be an integer between 1 and 5")
        
        # Validate text if provided
        if 'text' in review_data and not review_data['text']:
            raise ValueError("Review text is required")
        
        # Update attributes (except id, user_id, place_id)
        for key, value in review_data.items():
            if key not in ['id', 'user_id', 'place_id', 'created_at']:
                review[key] = value
        
        # Update the timestamp
        review['updated_at'] = datetime.now().isoformat()
        
        return review

    def delete_review(self, review_id):
        """Delete a review
        
        Args:
            review_id (str): ID of the review to delete
            
        Returns:
            bool: True if successfully deleted, False otherwise
        """
        # Initialize reviews_db if needed
        if not hasattr(self, 'reviews_db'):
            self.reviews_db = {}
        
        # Check if review exists
        if review_id not in self.reviews_db:
            return False
        
        # Delete the review
        del self.reviews_db[review_id]
        return True

    def get_places(self):
        """Get all places
        
        Returns:
            list: List of all places with detailed amenities
        """
        try:
            # Initialize places_db if needed
            if not hasattr(self, 'places_db'):
                self.places_db = {}
            
            # Make sure amenities_db exists
            if not hasattr(self, 'amenities_db'):
                self.amenities_db = {}
            
            # Returns a list of values with consistent structure
            places = []
            for place_id, place in self.places_db.items():
                # Defensive copy
                place_copy = place.copy() if isinstance(place, dict) else {}
                
                # Ensure all required fields are present
                for field in ['id', 'title', 'description', 'price', 'latitude', 'longitude', 
                            'owner_id', 'created_at', 'updated_at']:
                    if field not in place_copy:
                        if field in ['price', 'latitude', 'longitude']:
                            place_copy[field] = 0.0
                        elif field in ['created_at', 'updated_at']:
                            place_copy[field] = datetime.now().isoformat()
                        else:
                            place_copy[field] = ''
                
                # Ajouter les informations du propriétaire
                owner_id = place_copy.get('owner_id')
                if owner_id and owner_id in self.users_db:
                    owner = self.users_db[owner_id]
                    place_copy['owner'] = {
                        'id': owner_id,
                        'first_name': owner.get('first_name', ''),
                        'last_name': owner.get('last_name', ''),
                        'email': owner.get('email', '')
                    }
                else:
                    place_copy['owner'] = {
                        'id': owner_id or '',
                        'first_name': '(unknown)',
                        'last_name': '(unknown)',
                        'email': '(unknown)'
                    }
                
                # Gérer les amenities
                # Si place_copy['amenities'] est déjà une liste d'objets avec id et name,
                # nous pouvons la conserver telle quelle
                if isinstance(place_copy.get('amenities'), list):
                    amenities_in_place = place_copy.get('amenities', [])
                    
                    # Si les éléments de la liste sont des dictionnaires avec 'id' et 'name', on les conserve
                    if all(isinstance(a, dict) and 'id' in a and 'name' in a for a in amenities_in_place):
                        # Déjà au bon format, ne rien faire
                        pass
                    # Si ce sont des ID (chaînes), les convertir en objets
                    elif all(isinstance(a, str) for a in amenities_in_place):
                        amenities_objects = []
                        for amenity_id in amenities_in_place:
                            if amenity_id in self.amenities_db:
                                amenity = self.amenities_db[amenity_id]
                                amenities_objects.append({
                                    'id': amenity_id,
                                    'name': amenity.get('name', 'Unknown amenity')
                                })
                        place_copy['amenities'] = amenities_objects
                    # Sinon, initialiser à une liste vide
                    else:
                        place_copy['amenities'] = []
                else:
                    place_copy['amenities'] = []
                
                places.append(place_copy)
            
            return places
            
        except Exception as e:
            print(f"Error in get_places(): {str(e)}")
            import traceback
            traceback.print_exc()  # Affiche la pile d'appel complète
            return []  # Return empty list in case of error
