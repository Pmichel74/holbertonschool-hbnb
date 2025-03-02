# Rapport de tests HBNB API

## Résumé des tests

| Entité     | Tests réussis | Tests échoués | Total |
|------------|--------------|--------------|------|
| Users      | 8            | 0            | 8    |
| Places     | 8            | 0            | 8    |
| Amenities  | 6            | 0            | 6    |
| Reviews    | 7            | 0            | 7    |

## Tests détaillés

### Users

#### Test 1: Création d'un utilisateur valide
**Endpoint:** `POST /api/v1/users/`
**Données d'entrée:**
```json
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}
```
**Résultat attendu:** 201 Created

#### Test 2: Création d'un utilisateur avec un email invalide
**Endpoint:** `POST /api/v1/users/`
**Données d'entrée:**
```json
{
    "first_name": "Invalid",
    "last_name": "Email",
    "email": "invalid-email"
}
```
**Résultat attendu:** 400 Bad Request

#### Test 3: Création d'un utilisateur avec un email déjà utilisé
**Endpoint:** `POST /api/v1/users/`
**Données d'entrée:**
```json
{
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "john.doe@example.com"
}
```
**Résultat attendu:** 400 Bad Request (Email already exists)

#### Test 4: Récupération de tous les utilisateurs
**Endpoint:** `GET /api/v1/users/`
**Résultat attendu:** 200 OK, liste d'utilisateurs

#### Test 5: Récupération d'un utilisateur par ID
**Endpoint:** `GET /api/v1/users/{user_id}`
**Résultat attendu:** 200 OK, informations de l'utilisateur

#### Test 6: Récupération d'un utilisateur inexistant
**Endpoint:** `GET /api/v1/users/nonexistent-id`
**Résultat attendu:** 404 Not Found

#### Test 7: Mise à jour d'un utilisateur
**Endpoint:** `PUT /api/v1/users/{user_id}`
**Données d'entrée:**
```json
{
    "first_name": "John Updated",
    "last_name": "Doe Updated",
    "email": "john.updated@example.com"
}
```
**Résultat attendu:** 200 OK, utilisateur mis à jour

#### Test 8: Suppression d'un utilisateur
**Endpoint:** `DELETE /api/v1/users/{user_id}`
**Résultat attendu:** 200 OK, utilisateur supprimé

---

### Places

#### Test 1: Création d'un lieu valide
**Endpoint:** `POST /api/v1/places/`
**Données d'entrée:**
```json
{
    "title": "Cozy Apartment",
    "description": "A nice place to stay",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "user-id",
    "amenities": []
}
```
**Résultat attendu:** 201 Created

#### Test 2: Création d'un lieu avec un prix négatif
**Endpoint:** `POST /api/v1/places/`
**Données d'entrée:**
```json
{
    "title": "Problematic Place",
    "description": "Invalid price",
    "price": -50.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "user-id"
}
```
**Résultat attendu:** 400 Bad Request

#### Test 3: Récupération de tous les lieux
**Résultat attendu:** 200 OK

#### Test 4: Récupération d'un lieu par ID
**Résultat attendu:** 200 OK

#### Test 5: Mise à jour d'un lieu
**Résultat attendu:** 200 OK

#### Test 6: Suppression d'un lieu
**Résultat attendu:** 200 OK

#### Test 7: Récupération d'un lieu inexistant
**Résultat attendu:** 404 Not Found

#### Test 8: Création d'un lieu avec des coordonnées invalides
**Endpoint:** `POST /api/v1/places/`
**Données d'entrée:**
```json
{
    "title": "Invalid Place",
    "description": "Bad coordinates",
    "price": 100.0,
    "latitude": 95.0,
    "longitude": -122.4194,
    "owner_id": "user-id"
}
```
**Résultat attendu:** 400 Bad Request

---

### Amenities

#### Test 1: Création d'une commodité valide
**Données d'entrée:**
```json
{
    "name": "High-speed WiFi"
}
```
**Résultat attendu:** 201 Created

#### Test 2: Création d'une commodité avec un nom vide
**Données d'entrée:**
```json
{
    "name": ""
}
```
**Résultat attendu:** 400 Bad Request

#### Test 3: Récupération de toutes les commodités
**Résultat attendu:** 200 OK

#### Test 4: Récupération d'une commodité par ID
**Résultat attendu:** 200 OK

#### Test 5: Mise à jour d'une commodité
**Résultat attendu:** 200 OK

#### Test 6: Suppression d'une commodité
**Résultat attendu:** 200 OK

---

### Reviews

#### Test 1: Création d'un avis valide
**Données d'entrée:**
```json
{
    "text": "Great place to stay!",
    "rating": 5,
    "place_id": "place-id",
    "user_id": "user-id"
}
```
**Résultat attendu:** 201 Created

#### Test 2: Création d'un avis avec un texte vide
**Résultat attendu:** 400 Bad Request

#### Test 3: Récupération de toutes les reviews
**Résultat attendu:** 200 OK

#### Test 4: Récupération d'un avis par ID
**Résultat attendu:** 200 OK

#### Test 5: Mise à jour d'un avis
**Données d'entrée:**
```json
{
    "text": "This place was even better!",
    "rating": 5
}
```
**Résultat attendu:** 200 OK

#### Test 6: Suppression d'un avis
**Résultat attendu:** 200 OK

#### Test 7: Création d'un avis avec une note invalide
**Données d'entrée:**
```json
{
    "text": "This place was okay",
    "rating": 6,
    "place_id": "place-id",
    "user_id": "user-id"
}
```
**Résultat attendu:** 400 Bad Request