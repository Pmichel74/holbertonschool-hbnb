"""Module de validation des données"""
from email_validator import validate_email, EmailNotValidError
import re

class DataValidator:
    """Classe pour la validation des données"""

    @staticmethod
    def validate_email(email):
        """Valide un email"""
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False

    @staticmethod
    def validate_password(password):
        """
        Valide un mot de passe
        - Au moins 8 caractères
        - Au moins une lettre majuscule
        - Au moins une lettre minuscule
        - Au moins un chiffre
        """
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        return True

    @staticmethod
    def validate_string_field(value, min_length=1, max_length=255):
        """Valide un champ texte"""
        if not isinstance(value, str):
            return False
        if len(value) < min_length or len(value) > max_length:
            return False
        return True

    @staticmethod
    def validate_number_field(value, min_value=0, max_value=None):
        """Valide un champ numérique"""
        if not isinstance(value, (int, float)):
            return False
        if value < min_value:
            return False
        if max_value is not None and value > max_value:
            return False
        return True
