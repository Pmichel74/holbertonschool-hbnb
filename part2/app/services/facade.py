from app.models.user import User

class HBnBFacade:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HBnBFacade, cls).__new__(cls)
            cls._instance.users = {}
        return cls._instance

    def __init__(self):
        # Ensure users exists even if __init__ is called multiple times
        if not hasattr(self, 'users'):
            self.users = {}

    def create_user(self, user_data):
        """Create a new user"""
        try:
            # Validate data
            required_fields = ['first_name', 'last_name', 'email', 'password']
            for field in required_fields:
                if field not in user_data:
                    raise ValueError(f"The field {field} is missing")

            # Create the user
            user = User(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                password=user_data['password']
            )
            
            self.users[user.id] = user
            return user
        except Exception as e:
            raise ValueError(f"Error creating user: {str(e)}")

    def get_user_by_email(self, email):
        """Find a user by email"""
        if not email:
            return None
        return next((user for user in self.users.values() if user.email == email), None)

# Global facade instance
facade = HBnBFacade()
