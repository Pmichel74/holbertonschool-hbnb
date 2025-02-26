from uuid import uuid4

class User:
    """Represents a user in the system.
    
    This class manages user information including identification,
    personal details and contact information.

    Attributes:
        id (str): Unique identifier for the user
        email (str): User's email address
        first_name (str): User's first name
        last_name (str): User's last name
    """
    def __init__(self, first_name, last_name, email, id=None):
        """Initialize a new User instance.
        
        Args:
            first_name (str): User's first name
            last_name (str): User's last name 
            email (str): User's email address
            id (str, optional): Unique identifier. Defaults to generated UUID.
        """
        self.id = id or str(uuid4())
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def to_dict(self):
        """Convert user instance to dictionary representation.
        
        Returns:
            dict: Dictionary containing user attributes
        """
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name
        }
