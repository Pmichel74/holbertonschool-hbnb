# Rapport de tests HBNB API

## Résumé des tests

| Entité | Tests réussis | Tests échoués | Total |
|--------|---------------|--------------|-------|
| Users  | 6             | 0            | 6     |
| Places | 5             | 0            | 5     |
| Amenities | 3          | 0            | 3     |
| Reviews | 5            | 0            | 5     |

## Tests détaillés

### Users

#### Test 1: Création d'un utilisateur valide
**Endpoint:** POST /api/v1/users/
**Données d'entrée:**
```json
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}
```

#### Test 2: Création d'un utilisateur avec un email invalide
**Endpoint:** POST /api/v1/users/
**Données d'entrée:**
```json
{
    "first_name": "Invalid",
    "last_name": "Email",
    "email": "invalid-email"
}
```