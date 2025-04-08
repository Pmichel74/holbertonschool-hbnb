from app import db, bcrypt
from .base_model import BaseModel
import re
from sqlalchemy.orm import validates, relationship

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationships
    places = relationship("Place", back_populates="owner", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")

    @validates('first_name', 'last_name')
    def validate_string(self, key, value):
        field_name = key.replace('_', ' ').title()
        max_length = 50
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError(f"{field_name} is required and must be a non-empty string")
        if len(value) > max_length:
            raise ValueError(f"{field_name} must be at most {max_length} characters long")
        return value.strip()

    @validates('email')
    def validate_email(self, key, value):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Email is required and must be a non-empty string")
        email = value.strip().lower()
        email_regex = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        if not email_regex.match(email):
            raise ValueError("Invalid email format")
        return email
        
    @validates('password')
    def validate_password(self, key, value):
        """Valide le mot de passe sans le hacher"""
        if not isinstance(value, str) or len(value) < 8:
            raise ValueError("Password must be a string with at least 8 characters")
        return value  # Retourne le mot de passe non haché
    
    def hash_password(self, password):
        """Hache et stocke le mot de passe après validation"""
        # La validation est déjà faite par le validateur si on passe par self.password = password
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def verify_password(self, password):
        """Vérifie si le mot de passe fourni correspond au mot de passe haché"""
        return bcrypt.check_password_hash(self.password, password)
    
    def update(self, data):
        """Met à jour les attributs de l'utilisateur"""
        # Traitement spécial pour le mot de passe
        password = data.pop('password', None)
        
        # Mise à jour des autres attributs
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
                
        # Hachage du mot de passe si fourni
        if password is not None:
            self.hash_password(password)
