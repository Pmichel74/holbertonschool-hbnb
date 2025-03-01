from uuid import uuid4
from datetime import datetime

class BaseModel:
    """Base class for all models"""
    
    def __init__(self, **kwargs):
        """Initialize base model with common attributes"""
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        # If kwargs are processed after, they could override these values
    
    def to_dict(self):
        """Return dictionary of all instance attributes"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def save(self):
        """Update the updated_at attribute with current datetime"""
        self.updated_at = datetime.now()
