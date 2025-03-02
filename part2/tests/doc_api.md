Mise en œuvre des tests et validation des points de terminaison
1. Implémentation de la validation de base dans la couche logique métier
Validation du modèle User
Copier
class User(BaseModel):
    def validate(self):
        # Validation first_name
        if not self.first_name or not self.first_name.strip():
            raise ValidationError("first_name ne peut pas être vide")
            
        # Validation last_name
        if not self.last_name or not self.last_name.strip():
            raise ValidationError("last_name ne peut pas être vide")
            
        # Validation email
        if not self.email or not self.email.strip():
            raise ValidationError("email ne peut pas être vide")
            
        # Validation format email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.email):
            raise ValidationError("format email invalide")
Validation du modèle Place
Copier
class Place(BaseModel):
    def validate(self):
        # Validation title
        if not self.title or not self.title.strip():
            raise ValidationError("title ne peut pas être vide")
            
        # Validation price
        if not isinstance(self.price, (int, float)) or self.price <= 0:
            raise ValidationError("price doit être un nombre positif")
            
        # Validation latitude
        if not -90 <= self.latitude <= 90:
            raise ValidationError("latitude doit être entre -90 et 90")
            
        # Validation longitude
        if not -180 <= self.longitude <= 180:
            raise ValidationError("longitude doit être entre -180 et 180")
Validation du modèle Review
Copier
class Review(BaseModel):
    def validate(self):
        # Validation text
        if not self.text or not self.text.strip():
            raise ValidationError("text ne peut pas être vide")
            
        # Validation user_id et place_id
        if not User.get(self.user_id):
            raise ValidationError("user_id invalide")
        if not Place.get(self.place_id):
            raise ValidationError("place_id invalide")
2. Tests des points de terminaison avec cURL
Test création utilisateur valide
Copier
curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
-H "Content-Type: application/json" \
-d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}'

# Réponse attendue (200 OK):
{
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}
Test données invalides utilisateur
Copier
curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
-H "Content-Type: application/json" \
-d '{
    "first_name": "",
    "last_name": "",
    "email": "invalid-email"
}'

# Réponse attendue (400 Bad Request):
{
    "error": "Invalid input data"
}
Tests des limites (Place)
Copier
curl -X POST "http://127.0.0.1:5000/api/v1/places/" \
-H "Content-Type: application/json" \
-d '{
    "title": "Test Place",
    "price": -100,
    "latitude": 91,
    "longitude": 181
}'

# Réponse attendue (400 Bad Request):
{
    "error": "Validation error: latitude must be between -90 and 90"
}
3. Documentation Swagger
La documentation Swagger est accessible à:

Copier
http://127.0.0.1:5000/api/v1/
Elle décrit tous les endpoints avec:

Les méthodes HTTP supportées
Les paramètres attendus
Les réponses possibles
Les modèles de données
4. Tests unitaires
Copier
import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)
5. Documentation du processus de test
Points de terminaison testés
POST /api/v1/users/
POST /api/v1/places/
POST /api/v1/reviews/
GET /api/v1/users/{id}
GET /api/v1/places/{id}
Données d'entrée utilisées
Données valides pour chaque modèle
Données invalides (champs vides, formats incorrects)
Valeurs limites (latitude/longitude)
Résultats des tests
Endpoint	Test	Résultat attendu	Résultat obtenu
POST /users	Données valides	201 Created	201 Created
POST /users	Email invalide	400 Bad Request	400 Bad Request
POST /places	Latitude > 90	400 Bad Request	400 Bad Request
GET /users/999	ID inexistant	404 Not Found	404 Not Found
Problèmes rencontrés
Gestion des espaces dans les champs texte
Validation des références entre entités
Format des messages d'erreur
6. Résultat final
✅ Validation de base implémentée pour tous les modèles
✅ Tests cURL effectués et documentés
✅ Documentation Swagger générée et vérifiée
✅ Tests unitaires créés et exécutés
✅ Documentation complète du processus de test