import uuid
from datetime import datetime

class BaseModel:
    """Base class for all models in the application"""
    
    def __init__(self):
        """Initialize base model with UUID and timestamps"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update object attributes based on dictionary input
        
        Args:
            data (dict): Dictionary of attributes to update
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
