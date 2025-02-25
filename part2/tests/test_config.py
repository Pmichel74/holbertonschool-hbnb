def test_app_config(app):
    """Test de la configuration de base de l'application"""
    assert app.config['TESTING'] == True
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'
    assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] == False

def test_api_configuration(client):
    """Test de la configuration de l'API"""
    response = client.get('/swagger.json')
    assert response.status_code == 200
    assert b'User Management API' in response.data
