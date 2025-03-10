#!/usr/bin/python3
"""Test des importations pour les services utilisateur"""

def test_user_imports():
    """Test les importations utilisateur sans interaction"""
    try:
        # Test de l'import direct du service
        from app.services.user_service import UserService
        print("✓ Import direct de UserService OK")
        
        # Test de création d'une instance
        user_service = UserService(None)
        print("✓ Création d'instance UserService OK")
        
        print("\nTOUS LES TESTS RÉUSSIS!")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    test_user_imports()
