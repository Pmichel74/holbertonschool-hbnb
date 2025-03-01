from uuid import uuid4
from datetime import datetime
from app.models.place import Place
from app.models.user import User
from app.models.amenity import Amenity

class Facade:
    def __init__(self):
        """Initialize databases"""
        self.users_db = {}
        self.places_db = {}
        self.amenities_db = {}
        self.reviews_db = {}
        
        # Optionnel: Ajouter quelques utilisateurs de test
        self._create_test_users()

    def _create_test_users(self):
        """Créer des utilisateurs de test pour le développement"""
        test_users = [
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe@example.com',
                'is_admin': True
            },
            {
                'first_name': 'Jane',
                'last_name': 'Smith',
                'email': 'jane.smith@example.com'
            }
        ]
        
        # Créer les utilisateurs
        for user_data in test_users:
            self.create_user(user_data)

    # Méthodes pour les utilisateurs
    def get_users(self):
        return list(self.users_db.values())

    def get_user(self, user_id):
        return self.users_db.get(user_id)

    def create_user(self, user_data):
        """Create a new user"""
        # Validation code...
        
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            is_admin=user_data.get('is_admin', False)
        )
        
        # Assurez-vous que tous les champs sont inclus dans le dictionnaire
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

    # Ajoute cette méthode à ta façade
    def debug_print_user(self, user_id):
        """Debug utility to print user data"""
        if not hasattr(self, 'users_db'):
            print("users_db doesn't exist!")
            return
            
        if user_id not in self.users_db:
            print(f"User {user_id} not found in users_db!")
            return
            
        user = self.users_db[user_id]
        print(f"User {user_id} data:")
        for key, value in user.items():
            print(f"  {key}: {value}")

    # Ajoute cette méthode à ta façade
    def list_users_debug(self):
        """Afficher tous les utilisateurs pour débogage"""
        print("\n--- DEBUG: LISTE DES UTILISATEURS ---")
        if not hasattr(self, 'users_db'):
            print("users_db n'existe pas!")
            return []
            
        if not self.users_db:
            print("users_db est vide!")
            return []
            
        for user_id, user in self.users_db.items():
            print(f"Utilisateur ID: {user_id}")
            print(f"  Prénom: {user.get('first_name', '(manquant)')}")
            print(f"  Nom: {user.get('last_name', '(manquant)')}")
            print(f"  Email: {user.get('email', '(manquant)')}")
            print("---")
        
        return list(self.users_db.values())

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
        """Créer une nouvelle place
        
        Args:
            place_data (dict): Données de la place à créer
            
        Returns:
            dict: La place créée
            
        Raises:
            ValueError: Si les données sont invalides
        """
        try:
            # Validation du titre (obligatoire selon l'énoncé)
            if not place_data.get('title'):
                raise ValueError("Le titre est obligatoire")
            
            if len(place_data.get('title', '')) > 100:
                raise ValueError("Le titre ne doit pas dépasser 100 caractères")
                
            # Validation du prix (positif si spécifié)
            if 'price' in place_data and float(place_data['price']) < 0:
                raise ValueError("Le prix ne peut pas être négatif")
                
            # Validation de latitude et longitude
            if 'latitude' in place_data and not -90 <= float(place_data['latitude']) <= 90:
                raise ValueError("La latitude doit être comprise entre -90 et 90")
                
            if 'longitude' in place_data and not -180 <= float(place_data['longitude']) <= 180:
                raise ValueError("La longitude doit être comprise entre -180 et 180")
            
            # Vérification du propriétaire (si spécifié)
            owner_id = place_data.get('owner_id', '')
            if owner_id:
                if not hasattr(self, 'users_db'):
                    self.users_db = {}
                    
                if owner_id not in self.users_db:
                    # Option: créer automatiquement un utilisateur pour démonstration
                    user_data = {
                        'first_name': 'Owner',
                        'last_name': f'Of Place',
                        'email': f'owner_{owner_id[:8]}@example.com'
                    }
                    self.create_user(user_data)
                    # Utiliser l'ID du nouvel utilisateur
                    owner_id = list(self.users_db.keys())[-1]
            
            # Génération d'un nouvel ID
            place_id = str(uuid4())
            
            # Création de l'objet place
            place = {
                'id': place_id,
                'title': place_data.get('title', 'Untitled'),
                'description': place_data.get('description', ''),
                'price': float(place_data.get('price', 0.0)),
                'latitude': float(place_data.get('latitude', 0.0)),
                'longitude': float(place_data.get('longitude', 0.0)),
                'owner_id': owner_id,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            # Ensure places_db exists
            if not hasattr(self, 'places_db'):
                self.places_db = {}
            
            # Store place
            self.places_db[place_id] = place
            return place
        except Exception as e:
            print(f"Error in create_place: {str(e)}")
            # Return a minimal valid response to avoid 500
            return {
                'id': str(uuid4()),
                'title': 'Error occurred',
                'description': str(e),
                'price': 0.0,
                'latitude': 0.0, 
                'longitude': 0.0,
                'owner_id': '',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }

    def get_place(self, place_id):
        """Récupérer un lieu par son ID"""
        if not hasattr(self, 'places_db'):
            self.places_db = {}
        
        if place_id not in self.places_db:
            return None
        
        place = self.places_db[place_id].copy()
        
        # DEBUGGING - print what we know
        owner_id = place.get('owner_id')
        print(f"Place {place_id} has owner_id: {owner_id}")
        
        # Initialize users_db if needed
        if not hasattr(self, 'users_db'):
            self.users_db = {}
            print("Warning: users_db was not initialized")
        
        # Debugging - check users_db content
        print(f"users_db has {len(self.users_db)} entries")
        if owner_id and owner_id in self.users_db:
            print(f"Found owner {owner_id} in users_db!")
            owner = self.users_db[owner_id]
            print(f"Owner data: {owner}")
            
            # Ensure owner data is complete
            place['owner'] = {
                'id': owner_id,
                'first_name': owner.get('first_name', '(missing)'),
                'last_name': owner.get('last_name', '(missing)'),
                'email': owner.get('email', '(missing)')
            }
        else:
            print(f"Owner {owner_id} not found in users_db!")
            place['owner'] = {
                'id': owner_id or '',
                'first_name': '(unknown)',
                'last_name': '(unknown)',
                'email': '(unknown)'
            }
        
        # Rest of the function...
        
        return place

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

    def delete_place(self, place_id):
        """Supprimer une place par son ID
        
        Args:
            place_id (str): ID de la place à supprimer
            
        Returns:
            bool: True si supprimée, False si non trouvée
        """
        # Initialiser places_db si nécessaire
        if not hasattr(self, 'places_db'):
            self.places_db = {}
        
        # Vérifier si la place existe
        if place_id not in self.places_db:
            return False
        
        # Supprimer la place
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
        review = {
            'id': review_id,
            'text': review_data.get('text', ''),
            'rating': review_data.get('rating', 0),
            'user_id': review_data.get('user_id', ''),
            'place_id': review_data.get('place_id', '')
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
            if key not in ['id', 'user_id', 'place_id']:
                review[key] = value
        
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
        """Récupérer tous les lieux
        
        Returns:
            list: Liste de tous les lieux
        """
        try:
            # Initialiser places_db si nécessaire
            if not hasattr(self, 'places_db'):
                self.places_db = {}
            
            # Retourne une liste des valeurs avec structure cohérente
            places = []
            for place_id, place in self.places_db.items():
                # Copie défensive
                place_copy = place.copy() if isinstance(place, dict) else {}
                
                # S'assurer que tous les champs requis sont présents
                for field in ['id', 'title', 'description', 'price', 'latitude', 'longitude', 
                            'owner_id', 'created_at', 'updated_at']:
                    if field not in place_copy:
                        if field in ['price', 'latitude', 'longitude']:
                            place_copy[field] = 0.0
                        elif field in ['created_at', 'updated_at']:
                            place_copy[field] = datetime.now().isoformat()
                        else:
                            place_copy[field] = ''
                
                places.append(place_copy)
            
            return places
            
        except Exception as e:
            print(f"Erreur dans get_places(): {str(e)}")
            return []  # Retourner une liste vide en cas d'erreur
