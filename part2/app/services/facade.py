from app.models.user import User

class HBnBFacade:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HBnBFacade, cls).__new__(cls)
            cls._instance.users = {}
        return cls._instance

    def __init__(self):
        # Assurons-nous que users existe même si __init__ est appelé plusieurs fois
        if not hasattr(self, 'users'):
            self.users = {}

    def create_user(self, user_data):
        """Crée un nouvel utilisateur"""
        try:
            # Validation des données
            required_fields = ['first_name', 'last_name', 'email', 'password']
            for field in required_fields:
                if field not in user_data:
                    raise ValueError(f"Le champ {field} est manquant")

            # Création de l'utilisateur
            user = User(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                password=user_data['password']
            )
            
            self.users[user.id] = user
            return user
        except Exception as e:
            raise ValueError(f"Erreur lors de la création de l'utilisateur: {str(e)}")

    def get_user_by_email(self, email):
        """Recherche un utilisateur par email"""
        if not email:
            return None
        return next((user for user in self.users.values() if user.email == email), None)

# Instance globale de la facade
facade = HBnBFacade()
