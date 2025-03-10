#!/usr/bin/python3
"""Test d'importation"""

def test_imports():
    """Vérifie les importations clés"""
    try:
        from app import create_app
        print("✓ Import app.create_app ok")
        
        from app.models.base_model import BaseModel
        print("✓ Import app.models.base_model.BaseModel ok")
        
        from app.models.user import User
        print("✓ Import app.models.user.User ok")
        
        from app.models.place import Place
        print("✓ Import app.models.place.Place ok")

        # Testez UserService et PlaceService séparément
        try:
            from app.services.user_service import UserService
            print("✓ Import app.services.user_service.UserService ok")
        except ImportError as e:
            print(f"⚠️ Import app.services.user_service.UserService échoué: {e}")

        try:
            from app.services.place_service import PlaceService
            print("✓ Import app.services.place_service.PlaceService ok")
        except ImportError as e:
            print(f"⚠️ Import app.services.place_service.PlaceService échoué: {e}")
        
        try:
            from app.persistence.storage_engine import get_storage
            print("✓ Import app.persistence.storage_engine.get_storage ok")
        except ImportError as e:
            print(f"⚠️ Import app.persistence.storage_engine.get_storage échoué: {e}")
        
        print("\nTests d'importation terminés!")
        return True
    except Exception as e:
        print(f"❌ Erreur générale d'importation: {e}")
        return False

if __name__ == "__main__":
    test_imports()