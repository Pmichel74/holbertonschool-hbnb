from app import db
from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    # Repository for User model with extended operations beyond basic CRUD
    
    def __init__(self):
        # Initialize with User model
        super().__init__(User)
    
    def get_by_email(self, email):
        # Find user by email address
        return self.model.query.filter_by(email=email).first()
    
    def get_all_admins(self):
        # Get all users with admin privileges
        return self.model.query.filter_by(is_admin=True).all()
    
    def create_user(self, user_data):
        # Create a new user with proper password hashing
        # Create a new user instance
        user = User()
        
        # Set attributes from user_data
        for key, value in user_data.items():
            if key != 'password':
                setattr(user, key, value)
        
        # Handle password separately to ensure it's hashed
        if 'password' in user_data:
            user.hash_password(user_data['password'])
        
        # Add to database and commit
        db.session.add(user)
        db.session.commit()
        
        return user
    
    def update_user(self, user_id, user_data):
        # Update user with proper password handling
        user = self.get(user_id)
        if not user:
            return None
        
        # Handle password separately
        password = user_data.pop('password', None)
        
        # Update other attributes
        for key, value in user_data.items():
            setattr(user, key, value)
        
        # Update password if provided
        if password:
            user.hash_password(password)
        
        # Commit changes
        db.session.commit()
        
        return user
