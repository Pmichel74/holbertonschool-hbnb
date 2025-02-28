from uuid import uuid4
#from app.models.place import Place
#from app.models.user import User
#from app.models.amenity import Amenity

class Facade:
    def __init__(self):
        self.users_db = {}
        self.amenities_db = {}
        self.reviews_db = {}  # Ajouté pour gérer les reviews

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
        """Récupérer un place par son ID
        
        Args:
            place_id (str): ID du place à récupérer
            
        Returns:
            dict: Détails du place incluant le propriétaire, les commodités et les reviews,
                ou None si non trouvé
        """
        # Vérifier que places_db existe
        if not hasattr(self, 'places_db'):
            self.places_db = {}
        
        place = self.places_db.get(place_id)
        if not place:
            return None
        
        # Construire la réponse détaillée avec propriétaire et commodités
        place_result = dict(place)  # Copie pour ne pas modifier l'original
        
        # Récupérer les détails du propriétaire
        owner = self.get_user(place['owner_id'])
        if owner:
            place_result['owner'] = {
                'id': owner['id'],
                'first_name': owner['first_name'],
                'last_name': owner['last_name'],
                'email': owner['email']
            }
        else:
            place_result['owner'] = None
            
        # Récupérer les détails des commodités
        amenities_list = []
        for amenity_id in place.get('amenities', []):
            try:
                amenity = self.get_amenity(amenity_id)
                amenities_list.append({
                    'id': amenity['id'],
                    'name': amenity['name']
                })
            except ValueError:
                # Ignorer les commodités qui n'existent pas
                pass
        
        place_result['amenities'] = amenities_list
        
        # Ajouter les reviews associées à la place
        reviews_list = []
        for review in self.reviews_db.values():
            if review.get('place_id') == place_id:
                reviews_list.append(review)
        place_result['reviews'] = reviews_list
        
        return place_result

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

    # Méthodes pour les reviews
    def create_review(self, review_data):
        """Créer une nouvelle review"""
        # Validation : texte non vide, rating entre 1 et 5
        if not review_data.get('text'):
            raise ValueError("Le texte de la review est requis")
        if 'rating' not in review_data or not (1 <= review_data['rating'] <= 5):
            raise ValueError("La note (rating) doit être entre 1 et 5")
        # Vérifier que l'utilisateur existe
        user_id = review_data.get('user_id')
        if user_id not in self.users_db:
            raise ValueError(f"Utilisateur avec ID {user_id} n'existe pas")
        # Vérifier que la place existe
        place_id = review_data.get('place_id')
        if not hasattr(self, 'places_db') or place_id not in self.places_db:
            raise ValueError(f"Place avec ID {place_id} n'existe pas")
        
        review_id = str(uuid4())
        review = {
            'id': review_id,
            'text': review_data.get('text'),
            'rating': review_data.get('rating'),
            'user_id': user_id,
            'place_id': place_id
        }
        self.reviews_db[review_id] = review
        return review

    def get_review(self, review_id):
        """Récupérer une review par son ID"""
        return self.reviews_db.get(review_id)

    def get_all_reviews(self):
        """Récupérer toutes les reviews"""
        return list(self.reviews_db.values())

    def get_reviews_by_place(self, place_id):
        """Récupérer toutes les reviews pour une place spécifique"""
        # Vérifier que la place existe
        if not hasattr(self, 'places_db') or place_id not in self.places_db:
            return None
        return [review for review in self.reviews_db.values() if review.get('place_id') == place_id]

    def update_review(self, review_id, review_data):
        """Mettre à jour une review existante"""
        review = self.reviews_db.get(review_id)
        if not review:
            return None
        # Mise à jour uniquement des champs 'text' et 'rating'
        if 'text' in review_data:
            review['text'] = review_data['text']
        if 'rating' in review_data:
            if not (1 <= review_data['rating'] <= 5):
                raise ValueError("La note (rating) doit être entre 1 et 5")
            review['rating'] = review_data['rating']
        return review

    def delete_review(self, review_id):
        """Supprimer une review par son ID"""
        if review_id in self.reviews_db:
            del self.reviews_db[review_id]
            return True
        return False

# Instance globale pour un accès direct depuis les autres modules
facade = Facade()
