cat > /home/patri/hbnb/part2/temp_fix/user_service.py << 'EOF'
#!/usr/bin/python3
"""Service pour les opérations liées aux utilisateurs"""

class UserService:
    """Service pour la gestion des utilisateurs"""
    
    def __init__(self, storage):
        """Initialise le service avec le stockage"""
        self.storage = storage
    
    def get(self, user_id):
        """Récupère un utilisateur par son ID"""
        # Import User ici pour éviter les importations circulaires
        from app.models.user import User
        return self.storage.get(User, user_id)
    
    def get_all(self):
        """Récupère tous les utilisateurs"""
        # Import User ici pour éviter les importations circulaires
        from app.models.user import User
        return self.storage.all(User)
    
    def create(self, user_data):
        """Crée un nouvel utilisateur"""
        # Import User ici pour éviter les importations circulaires
        from app.models.user import User
        user = User(**user_data)
        # Assurez-vous de hacher le mot de passe avant de stocker
        if 'password' in user_data:
            user.set_password(user_data['password'])
        self.storage.new(user)
        self.storage.save()
        return user
    
    def update(self, user_id, data, ignore_fields=None):
        """Met à jour un utilisateur existant"""
        if ignore_fields is None:
            ignore_fields = []
            
        user = self.get(user_id)
        if not user:
            # Import ici pour éviter les importations circulaires
            from app.error_handlers import NotFoundError
            raise NotFoundError(f"User {user_id} not found")
            
        # Traitement spécial pour le mot de passe
        if 'password' in data:
            user.set_password(data['password'])
            data.pop('password')  # Retirez le mot de passe des attributs à définir
            
        for key, value in data.items():
            if key not in ignore_fields and hasattr(user, key):
                setattr(user, key, value)
                
        self.storage.save()
        return user
    
    def delete(self, user_id):
        """Supprime un utilisateur"""
        user = self.get(user_id)
        if not user:
            # Import ici pour éviter les importations circulaires
            from app.error_handlers import NotFoundError
            raise NotFoundError(f"User {user_id} not found")
            
        self.storage.delete(user)
        self.storage.save()
        return True
EOF