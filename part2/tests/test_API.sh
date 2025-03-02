#!/bin/bash
# filepath: /home/jbn/PROJETS/Hbnb_perso/OMGpart2/hbnb/tests/test_users_api.sh
# Script de test pour les endpoints API HBnB

BASE_URL="http://localhost:5000/api/v1"
USER_ENDPOINT="$BASE_URL/users"
AMENITY_ENDPOINT="$BASE_URL/amenities"
PLACE_ENDPOINT="$BASE_URL/places"
REVIEW_ENDPOINT="$BASE_URL/reviews"

# Couleurs pour les messages
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Vérifier si jq est installé
if ! command -v jq &> /dev/null; then
    echo -e "${RED}L'outil jq n'est pas installé. Installation en cours...${NC}"
    sudo apt-get update && sudo apt-get install -y jq
    if [ $? -ne 0 ]; then
        echo -e "${RED}Impossible d'installer jq. Veuillez l'installer manuellement et réessayer.${NC}"
        exit 1
    fi
fi

# =======================================================
# SECTION 1: TESTS DES ENDPOINTS UTILISATEUR
# =======================================================
# SECTION 1: TESTS DES ENDPOINTS UTILISATEUR
# =======================================================

echo -e "${BLUE}┌────────────────────────────────────────────┐${NC}"
echo -e "${BLUE}│         TESTS DES API UTILISATEURS         │${NC}"
echo -e "${BLUE}└────────────────────────────────────────────┘${NC}\n"

# 1. Création d'un utilisateur (cas positif)
echo -e "${YELLOW}Test 1: Création d'un utilisateur valide${NC}"
CREATE_RESPONSE=$(curl -s -L -X 'POST' \
    "$USER_ENDPOINT" \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}')

echo "Réponse: $CREATE_RESPONSE"

# Extraction de l'ID avec jq
USER_ID=$(echo "$CREATE_RESPONSE" | jq -r '.id // empty')
echo "ID extrait: $USER_ID"

if [[ -n "$USER_ID" ]]; then
    echo -e "${GREEN}✓ Création d'utilisateur réussie. ID: $USER_ID${NC}\n"
else
    echo -e "${RED}✗ Échec de la création d'utilisateur${NC}\n"
fi

# 2. Création d'un utilisateur avec email déjà existant
echo -e "${YELLOW}Test 2: Création d'un utilisateur avec email déjà existant${NC}"
DUPLICATE_RESPONSE=$(curl -s -L -X 'POST' \
    "$USER_ENDPOINT" \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "john.doe@example.com"
}')

echo "Réponse: $DUPLICATE_RESPONSE"

if [[ $DUPLICATE_RESPONSE == *"Email already registered"* ]]; then
  echo -e "${GREEN}✓ Détection correcte d'email dupliqué${NC}\n"
else
  echo -e "${RED}✗ Échec de la détection d'email dupliqué${NC}\n"
fi

# 3. Création d'un utilisateur avec données invalides
echo -e "${YELLOW}Test 3: Création d'un utilisateur avec données invalides${NC}"
INVALID_RESPONSE=$(curl -s -L -X 'POST' \
  "$USER_ENDPOINT" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "last_name": "Doe",
  "email": "invalid_user@example.com"
}')

echo "Réponse: $INVALID_RESPONSE"

if [[ $INVALID_RESPONSE == *"error"* || $INVALID_RESPONSE == *"errors"* ]]; then
  echo -e "${GREEN}✓ Détection correcte de données invalides${NC}\n"
else
  echo -e "${RED}✗ Échec de la détection de données invalides${NC}\n"
fi

# 4. Récupération de tous les utilisateurs
echo -e "${YELLOW}Test 4: Récupération de tous les utilisateurs${NC}"
GET_ALL_RESPONSE=$(curl -s -L -X 'GET' \
  "$USER_ENDPOINT" \
  -H 'accept: application/json')

echo "Réponse: $GET_ALL_RESPONSE"

if [[ $(echo "$GET_ALL_RESPONSE" | jq 'length') -gt 0 ]]; then
  echo -e "${GREEN}✓ Récupération de la liste d'utilisateurs réussie${NC}\n"
else
  echo -e "${RED}✗ Échec de la récupération de la liste d'utilisateurs${NC}\n"
fi

# 5. Récupération d'un utilisateur par ID
echo -e "${YELLOW}Test 5: Récupération d'un utilisateur par ID${NC}"
if [[ -n "$USER_ID" ]]; then
  echo "Tentative de récupération pour l'ID: $USER_ID"
  GET_USER_RESPONSE=$(curl -s -L -X 'GET' \
    "$USER_ENDPOINT/$USER_ID" \
    -H 'accept: application/json')
  
  echo "Réponse: $GET_USER_RESPONSE"
  
  RETRIEVED_ID=$(echo "$GET_USER_RESPONSE" | jq -r '.id // empty')
  if [[ "$RETRIEVED_ID" == "$USER_ID" ]]; then
    echo -e "${GREEN}✓ Récupération de l'utilisateur réussie${NC}\n"
  else
    echo -e "${RED}✗ Échec de la récupération de l'utilisateur${NC}\n"
  fi
else
  echo -e "${RED}✗ ID utilisateur non disponible pour le test${NC}\n"
fi

# 6. Récupération d'un utilisateur avec ID inexistant
echo -e "${YELLOW}Test 6: Récupération d'un utilisateur avec ID inexistant${NC}"
INVALID_ID_RESPONSE=$(curl -s -L -X 'GET' \
  "$USER_ENDPOINT/invalid_id_12345" \
  -H 'accept: application/json')

echo "Réponse: $INVALID_ID_RESPONSE"

if [[ $INVALID_ID_RESPONSE == *"not found"* || $INVALID_ID_RESPONSE == *"error"* ]]; then
  echo -e "${GREEN}✓ Gestion correcte d'ID inexistant${NC}\n"
else
  echo -e "${RED}✗ Mauvaise gestion d'ID inexistant${NC}\n"
fi

# 7. Mise à jour d'un utilisateur
echo -e "${YELLOW}Test 7: Mise à jour d'un utilisateur${NC}"
if [[ -n "$USER_ID" ]]; then
  echo "Tentative de mise à jour pour l'ID: $USER_ID"
  UPDATE_RESPONSE=$(curl -s -L -X 'PUT' \
    "$USER_ENDPOINT/$USER_ID" \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "first_name": "John-Updated",
    "last_name": "Doe-Updated",
    "email": "john.updated@example.com"
  }')
  
  echo "Réponse: $UPDATE_RESPONSE"
  
  UPDATED_NAME=$(echo "$UPDATE_RESPONSE" | jq -r '.first_name // empty')
  if [[ "$UPDATED_NAME" == "John-Updated" ]]; then
    echo -e "${GREEN}✓ Mise à jour de l'utilisateur réussie${NC}\n"
  else
    echo -e "${RED}✗ Échec de la mise à jour de l'utilisateur${NC}\n"
  fi
else
  echo -e "${RED}✗ ID utilisateur non disponible pour le test${NC}\n"
fi

# 8. Mise à jour avec ID inexistant
echo -e "${YELLOW}Test 8: Mise à jour d'un utilisateur avec ID inexistant${NC}"
INVALID_UPDATE_RESPONSE=$(curl -s -L -X 'PUT' \
  "$USER_ENDPOINT/invalid_id_12345" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "first_name": "Invalid",
  "last_name": "Update",
  "email": "invalid.update@example.com"
}')

echo "Réponse: $INVALID_UPDATE_RESPONSE"

if [[ $INVALID_UPDATE_RESPONSE == *"not found"* || $INVALID_UPDATE_RESPONSE == *"error"* ]]; then
  echo -e "${GREEN}✓ Gestion correcte de mise à jour avec ID inexistant${NC}\n"
else
  echo -e "${RED}✗ Mauvaise gestion de mise à jour avec ID inexistant${NC}\n"
fi

# 9. Création d'un deuxième utilisateur (pour démontrer la liste multiple)
echo -e "${YELLOW}Test 9: Création d'un deuxième utilisateur${NC}"
CREATE_RESPONSE2=$(curl -s -L -X 'POST' \
  "$USER_ENDPOINT" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane.smith@example.com"
}')

echo "Réponse: $CREATE_RESPONSE2"

# Extraction de l'ID avec jq
USER_ID2=$(echo "$CREATE_RESPONSE2" | jq -r '.id // empty')
echo "ID extrait: $USER_ID2"

if [[ -n "$USER_ID2" ]]; then
  echo -e "${GREEN}✓ Création du deuxième utilisateur réussie. ID: $USER_ID2${NC}\n"
else
  echo -e "${RED}✗ Échec de la création du deuxième utilisateur${NC}\n"
fi

# 10. Vérification de la liste pour voir les deux utilisateurs
echo -e "${YELLOW}Test 10: Vérification de la liste avec deux utilisateurs${NC}"
GET_ALL_RESPONSE2=$(curl -s -L -X 'GET' \
  "$USER_ENDPOINT" \
  -H 'accept: application/json')

echo "Réponse: $GET_ALL_RESPONSE2"

# Vérification plus robuste avec jq
USER1_IN_LIST=$(echo "$GET_ALL_RESPONSE2" | jq --arg id "$USER_ID" 'map(.id) | contains([$id])' 2>/dev/null)
USER2_IN_LIST=$(echo "$GET_ALL_RESPONSE2" | jq --arg id "$USER_ID2" 'map(.id) | contains([$id])' 2>/dev/null)

if [[ "$USER1_IN_LIST" == "true" && "$USER2_IN_LIST" == "true" ]]; then
  echo -e "${GREEN}✓ Liste contient les deux utilisateurs${NC}\n"
else
  echo -e "${RED}✗ Liste incomplète${NC}\n"
fi

# =======================================================
# SECTION 2: TESTS DES ENDPOINTS AMENITY
# =======================================================

echo -e "${BLUE}┌────────────────────────────────────────────┐${NC}"
echo -e "${BLUE}│          TESTS DES API AMENITIES           │${NC}"
echo -e "${BLUE}└────────────────────────────────────────────┘${NC}\n"

# 1. Création d'une amenity
echo -e "${YELLOW}Test 1: Création d'une amenity valide${NC}"
AMENITY_CREATE_RESPONSE=$(curl -s -L -X 'POST' \
  "$AMENITY_ENDPOINT" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Wi-Fi"
}')

echo "Réponse: $AMENITY_CREATE_RESPONSE"

# Extraction de l'ID avec jq
AMENITY_ID=$(echo "$AMENITY_CREATE_RESPONSE" | jq -r '.id // empty')
echo "ID extrait: $AMENITY_ID"

if [[ -n "$AMENITY_ID" ]]; then
  echo -e "${GREEN}✓ Création d'amenity réussie. ID: $AMENITY_ID${NC}\n"
else
  echo -e "${RED}✗ Échec de la création d'amenity${NC}\n"
fi

# 2. Création d'une amenity avec données invalides
echo -e "${YELLOW}Test 2: Création d'une amenity avec données invalides${NC}"
AMENITY_INVALID_RESPONSE=$(curl -s -L -X 'POST' \
  "$AMENITY_ENDPOINT" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{}')

echo "Réponse: $AMENITY_INVALID_RESPONSE"

if [[ $AMENITY_INVALID_RESPONSE == *"error"* || $AMENITY_INVALID_RESPONSE == *"errors"* ]]; then
  echo -e "${GREEN}✓ Détection correcte de données invalides${NC}\n"
else
  echo -e "${RED}✗ Échec de la détection de données invalides${NC}\n"
fi

# 3. Récupération de toutes les amenities
echo -e "${YELLOW}Test 3: Récupération de toutes les amenities${NC}"
AMENITY_GET_ALL_RESPONSE=$(curl -s -L -X 'GET' \
  "$AMENITY_ENDPOINT" \
  -H 'accept: application/json')

echo "Réponse: $AMENITY_GET_ALL_RESPONSE"

if [[ $(echo "$AMENITY_GET_ALL_RESPONSE" | jq 'length') -gt 0 ]]; then
  echo -e "${GREEN}✓ Récupération de la liste d'amenities réussie${NC}\n"
else
  echo -e "${RED}✗ Échec de la récupération de la liste d'amenities${NC}\n"
fi

# 4. Récupération d'une amenity par ID
echo -e "${YELLOW}Test 4: Récupération d'une amenity par ID${NC}"
if [[ -n "$AMENITY_ID" ]]; then
  echo "Tentative de récupération pour l'ID: $AMENITY_ID"
  AMENITY_GET_RESPONSE=$(curl -s -L -X 'GET' \
    "$AMENITY_ENDPOINT/$AMENITY_ID" \
    -H 'accept: application/json')
  
  echo "Réponse: $AMENITY_GET_RESPONSE"
  
  AMENITY_RETRIEVED_ID=$(echo "$AMENITY_GET_RESPONSE" | jq -r '.id // empty')
  if [[ "$AMENITY_RETRIEVED_ID" == "$AMENITY_ID" ]]; then
    echo -e "${GREEN}✓ Récupération de l'amenity réussie${NC}\n"
  else
    echo -e "${RED}✗ Échec de la récupération de l'amenity${NC}\n"
  fi
else
  echo -e "${RED}✗ ID amenity non disponible pour le test${NC}\n"
fi

# 5. Récupération d'une amenity avec ID inexistant
echo -e "${YELLOW}Test 5: Récupération d'une amenity avec ID inexistant${NC}"
AMENITY_INVALID_ID_RESPONSE=$(curl -s -L -X 'GET' \
  "$AMENITY_ENDPOINT/invalid_id_12345" \
  -H 'accept: application/json')

echo "Réponse: $AMENITY_INVALID_ID_RESPONSE"

if [[ $AMENITY_INVALID_ID_RESPONSE == *"not found"* || $AMENITY_INVALID_ID_RESPONSE == *"error"* ]]; then
  echo -e "${GREEN}✓ Gestion correcte d'ID inexistant${NC}\n"
else
  echo -e "${RED}✗ Mauvaise gestion d'ID inexistant${NC}\n"
fi

# 6. Mise à jour d'une amenity
echo -e "${YELLOW}Test 6: Mise à jour d'une amenity${NC}"
if [[ -n "$AMENITY_ID" ]]; then
  echo "Tentative de mise à jour pour l'ID: $AMENITY_ID"
  AMENITY_UPDATE_RESPONSE=$(curl -s -L -X 'PUT' \
    "$AMENITY_ENDPOINT/$AMENITY_ID" \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "name": "Air Conditioning"
  }')
  
  echo "Réponse: $AMENITY_UPDATE_RESPONSE"
  
  AMENITY_UPDATED_NAME=$(echo "$AMENITY_UPDATE_RESPONSE" | jq -r '.name // empty')
  if [[ "$AMENITY_UPDATED_NAME" == "Air Conditioning" ]]; then
    echo -e "${GREEN}✓ Mise à jour de l'amenity réussie${NC}\n"
  else
    echo -e "${RED}✗ Échec de la mise à jour de l'amenity${NC}\n"
  fi
else
  echo -e "${RED}✗ ID amenity non disponible pour le test${NC}\n"
fi

# 7. Mise à jour avec ID inexistant
echo -e "${YELLOW}Test 7: Mise à jour d'une amenity avec ID inexistant${NC}"
AMENITY_INVALID_UPDATE_RESPONSE=$(curl -s -L -X 'PUT' \
  "$AMENITY_ENDPOINT/invalid_id_12345" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Invalid Update"
}')

echo "Réponse: $AMENITY_INVALID_UPDATE_RESPONSE"

if [[ $AMENITY_INVALID_UPDATE_RESPONSE == *"not found"* || $AMENITY_INVALID_UPDATE_RESPONSE == *"error"* ]]; then
  echo -e "${GREEN}✓ Gestion correcte de mise à jour avec ID inexistant${NC}\n"
else
  echo -e "${RED}✗ Mauvaise gestion de mise à jour avec ID inexistant${NC}\n"
fi

# 8. Création d'une deuxième amenity (pour démontrer la liste multiple)
echo -e "${YELLOW}Test 8: Création d'une deuxième amenity${NC}"
AMENITY_CREATE_RESPONSE2=$(curl -s -L -X 'POST' \
  "$AMENITY_ENDPOINT" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Swimming Pool"
}')

echo "Réponse: $AMENITY_CREATE_RESPONSE2"

# Extraction de l'ID avec jq
AMENITY_ID2=$(echo "$AMENITY_CREATE_RESPONSE2" | jq -r '.id // empty')
echo "ID extrait: $AMENITY_ID2"

if [[ -n "$AMENITY_ID2" ]]; then
  echo -e "${GREEN}✓ Création de la deuxième amenity réussie. ID: $AMENITY_ID2${NC}\n"
else
  echo -e "${RED}✗ Échec de la création de la deuxième amenity${NC}\n"
fi

# 9. Vérification de la liste pour voir les deux amenities
echo -e "${YELLOW}Test 9: Vérification de la liste avec deux amenities${NC}"
AMENITY_GET_ALL_RESPONSE2=$(curl -s -L -X 'GET' \
  "$AMENITY_ENDPOINT" \
  -H 'accept: application/json')

echo "Réponse: $AMENITY_GET_ALL_RESPONSE2"

# Vérification plus robuste avec jq
AMENITY1_IN_LIST=$(echo "$AMENITY_GET_ALL_RESPONSE2" | jq --arg id "$AMENITY_ID" 'map(.id) | contains([$id])' 2>/dev/null)
AMENITY2_IN_LIST=$(echo "$AMENITY_GET_ALL_RESPONSE2" | jq --arg id "$AMENITY_ID2" 'map(.id) | contains([$id])' 2>/dev/null)

if [[ "$AMENITY1_IN_LIST" == "true" && "$AMENITY2_IN_LIST" == "true" ]]; then
  echo -e "${GREEN}✓ Liste contient les deux amenities${NC}\n"
else
  echo -e "${RED}✗ Liste incomplète${NC}\n"
fi

# =======================================================
# SECTION 3: TESTS DES ENDPOINTS PLACE
# =======================================================

echo -e "${BLUE}┌────────────────────────────────────────────┐${NC}"
echo -e "${BLUE}│             TESTS DES API PLACES           │${NC}"
echo -e "${BLUE}└────────────────────────────────────────────┘${NC}\n"

# 0. Create test user and amenities first
echo -e "${YELLOW}Test préliminaire: Création d'un utilisateur pour les tests${NC}"
USER_RESPONSE=$(curl -s -L -X 'POST' \
  "$USER_ENDPOINT" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "first_name": "Place",
  "last_name": "Owner",
  "email": "place.owner'$(date +%s)'@example.com"
}')

USER_ID=$(echo "$USER_RESPONSE" | jq -r '.id // empty')
echo "ID utilisateur extrait: $USER_ID"

if [[ -z "$USER_ID" ]]; then
  echo -e "${RED}✗ Échec de la création d'utilisateur pour les tests de place. Arrêt des tests.${NC}\n"
  echo "Réponse complète: $USER_RESPONSE"
  exit 1
fi

echo -e "${YELLOW}Test préliminaire: Création d'amenities pour les tests${NC}"
AMENITY1_RESPONSE=$(curl -s -L -X 'POST' \
  "$AMENITY_ENDPOINT" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Wi-Fi"
}')

AMENITY1_ID=$(echo "$AMENITY1_RESPONSE" | jq -r '.id // empty')
echo "ID amenity 1 extrait: $AMENITY1_ID"

AMENITY2_RESPONSE=$(curl -s -L -X 'POST' \
  "$AMENITY_ENDPOINT" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Swimming Pool"
}')

AMENITY2_ID=$(echo "$AMENITY2_RESPONSE" | jq -r '.id // empty')
echo "ID amenity 2 extrait: $AMENITY2_ID"

# 1. Création d'un place valide
echo -e "${YELLOW}Test 1: Création d'un place valide${NC}"
CREATE_RESPONSE=$(curl -s -L -X 'POST' \
  "$PLACE_ENDPOINT" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Cozy Apartment",
  "description": "A nice place to stay",
  "price": 100.0,
  "latitude": 37.7749,
  "longitude": -122.4194,
  "owner_id": "'"$USER_ID"'",
  "amenities": ["'"$AMENITY1_ID"'", "'"$AMENITY2_ID"'"]
}')

echo "Réponse: $CREATE_RESPONSE"

# Extraction de l'ID 
PLACE_ID=$(echo "$CREATE_RESPONSE" | jq -r '.id // empty')
echo "ID place extrait: $PLACE_ID"

if [[ -n "$PLACE_ID" ]]; then
  echo -e "${GREEN}✓ Création de place réussie. ID: $PLACE_ID${NC}\n"
else
  echo -e "${RED}✗ Échec de la création de place${NC}\n"
fi

# 2. Création avec propriétaire invalide
echo -e "${YELLOW}Test 2: Création d'un place avec propriétaire invalide${NC}"
INVALID_OWNER_RESPONSE=$(curl -s -L -X 'POST' \
  "$PLACE_ENDPOINT" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Invalid Owner Apartment",
  "description": "A place with invalid owner",
  "price": 120.0,
  "latitude": 38.7749,
  "longitude": -121.4194,
  "owner_id": "invalid_owner_id",
  "amenities": []
}')

echo "Réponse: $INVALID_OWNER_RESPONSE"

if [[ $INVALID_OWNER_RESPONSE == *"error"* ]]; then
  echo -e "${GREEN}✓ Détection correcte de propriétaire invalide${NC}\n"
else
  echo -e "${RED}✗ Échec de la détection de propriétaire invalide${NC}\n"
fi

# 3. Création avec prix négatif
echo -e "${YELLOW}Test 3: Création d'un place avec prix négatif${NC}"
NEGATIVE_PRICE_RESPONSE=$(curl -s -L -X 'POST' \
  "$PLACE_ENDPOINT" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Negative Price Place",
  "description": "A place with negative price",
  "price": -50.0,
  "latitude": 39.7749,
  "longitude": -120.4194,
  "owner_id": "'"$USER_ID"'",
  "amenities": []
}')

echo "Réponse: $NEGATIVE_PRICE_RESPONSE"

if [[ $NEGATIVE_PRICE_RESPONSE == *"error"* ]]; then
  echo -e "${GREEN}✓ Détection correcte de prix négatif${NC}\n"
else
  echo -e "${RED}✗ Échec de la détection de prix négatif${NC}\n"
fi

# 4. Création avec latitude invalide
echo -e "${YELLOW}Test 4: Création d'un place avec latitude invalide${NC}"
INVALID_LAT_RESPONSE=$(curl -s -L -X 'POST' \
  "$PLACE_ENDPOINT" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Invalid Latitude Place",
  "description": "A place with invalid latitude",
  "price": 150.0,
  "latitude": 95.0,
  "longitude": -120.4194,
  "owner_id": "'"$USER_ID"'",
  "amenities": []
}')

echo "Réponse: $INVALID_LAT_RESPONSE"

if [[ $INVALID_LAT_RESPONSE == *"error"* ]]; then
  echo -e "${GREEN}✓ Détection correcte de latitude invalide${NC}\n"
else
  echo -e "${RED}✗ Échec de la détection de latitude invalide${NC}\n"
fi

# 5. Liste de tous les places
echo -e "${YELLOW}Test 5: Récupération de tous les places${NC}"
GET_ALL_RESPONSE=$(curl -s -L -X 'GET' \
  "$PLACE_ENDPOINT" \
  -H 'accept: application/json')

echo "Réponse: $GET_ALL_RESPONSE"

if [[ $(echo "$GET_ALL_RESPONSE" | jq 'length') -gt 0 ]]; then
  echo -e "${GREEN}✓ Récupération de la liste de places réussie${NC}\n"
else
  echo -e "${RED}✗ Échec de la récupération de la liste de places${NC}\n"
fi

# 6. Détail d'un place par ID
echo -e "${YELLOW}Test 6: Récupération d'un place par ID${NC}"
if [[ -n "$PLACE_ID" ]]; then
  echo "Tentative de récupération pour l'ID: $PLACE_ID"
  GET_PLACE_RESPONSE=$(curl -s -L -X 'GET' \
    "$PLACE_ENDPOINT/$PLACE_ID" \
    -H 'accept: application/json')
  
  echo "Réponse: $GET_PLACE_RESPONSE"
  
  RETRIEVED_ID=$(echo "$GET_PLACE_RESPONSE" | jq -r '.id // empty')
  RETRIEVED_OWNER=$(echo "$GET_PLACE_RESPONSE" | jq -r '.owner.id // empty')
  RETRIEVED_AMENITIES=$(echo "$GET_PLACE_RESPONSE" | jq -r '.amenities | length')
  
  if [[ "$RETRIEVED_ID" == "$PLACE_ID" && "$RETRIEVED_OWNER" == "$USER_ID" && "$RETRIEVED_AMENITIES" -eq 2 ]]; then
    echo -e "${GREEN}✓ Récupération du place avec détails complets réussie${NC}\n"
  else
    echo -e "${RED}✗ Échec de la récupération complète du place${NC}\n"
  fi
else
  echo -e "${RED}✗ ID place non disponible pour le test${NC}\n"
fi

# 7. Récupération avec ID inexistant
echo -e "${YELLOW}Test 7: Récupération d'un place avec ID inexistant${NC}"
INVALID_ID_RESPONSE=$(curl -s -L -X 'GET' \
  "$PLACE_ENDPOINT/invalid_id_12345" \
  -H 'accept: application/json')

echo "Réponse: $INVALID_ID_RESPONSE"

if [[ $INVALID_ID_RESPONSE == *"not found"* || $INVALID_ID_RESPONSE == *"error"* ]]; then
  echo -e "${GREEN}✓ Gestion correcte d'ID inexistant${NC}\n"
else
  echo -e "${RED}✗ Mauvaise gestion d'ID inexistant${NC}\n"
fi

# 8. Mise à jour d'un place
echo -e "${YELLOW}Test 8: Mise à jour d'un place${NC}"
if [[ -n "$PLACE_ID" ]]; then
  echo "Tentative de mise à jour pour l'ID: $PLACE_ID"
  UPDATE_RESPONSE=$(curl -s -L -X 'PUT' \
    "$PLACE_ENDPOINT/$PLACE_ID" \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "title": "Updated Apartment",
    "description": "An updated description",
    "price": 150.0
  }')
  
  echo "Réponse: $UPDATE_RESPONSE"
  
  UPDATED_TITLE=$(echo "$UPDATE_RESPONSE" | jq -r '.title // empty')
  if [[ "$UPDATED_TITLE" == "Updated Apartment" ]]; then
    echo -e "${GREEN}✓ Mise à jour du place réussie${NC}\n"
  else
    echo -e "${RED}✗ Échec de la mise à jour du place${NC}\n"
  fi
else
  echo -e "${RED}✗ ID place non disponible pour le test${NC}\n"
fi

# 9. Mise à jour avec ID inexistant
echo -e "${YELLOW}Test 9: Mise à jour d'un place avec ID inexistant${NC}"
INVALID_UPDATE_RESPONSE=$(curl -s -L -X 'PUT' \
  "$PLACE_ENDPOINT/invalid_id_12345" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Invalid Update",
  "price": 200.0
}')

echo "Réponse: $INVALID_UPDATE_RESPONSE"

if [[ $INVALID_UPDATE_RESPONSE == *"not found"* || $INVALID_UPDATE_RESPONSE == *"error"* ]]; then
  echo -e "${GREEN}✓ Gestion correcte de mise à jour avec ID inexistant${NC}\n"
else
  echo -e "${RED}✗ Mauvaise gestion de mise à jour avec ID inexistant${NC}\n"
fi

echo -e "${BLUE}┌────────────────────────────────────────────┐${NC}"
echo -e "${BLUE}│             TESTS DES API REVIEWS           │${NC}"
echo -e "${BLUE}└────────────────────────────────────────────┘${NC}\n"

# 0. Tests préliminaires : création d'un utilisateur et d'un place pour les tests
echo -e "${YELLOW}Test préliminaire: Création d'un utilisateur pour les tests${NC}"
USER_RESPONSE=$(curl -s -L -X 'POST' \
  "$USER_ENDPOINT" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "first_name": "Review",
  "last_name": "Tester",
  "email": "review.tester'$(date +%s)'@example.com"
}')

USER_ID=$(echo "$USER_RESPONSE" | jq -r '.id // empty')
echo "ID utilisateur extrait: $USER_ID"

if [[ -z "$USER_ID" ]]; then
  echo -e "${RED}✗ Échec de la création d'utilisateur pour les tests. Arrêt des tests.${NC}\n"
  echo "Réponse complète: $USER_RESPONSE"
  exit 1
fi

echo -e "${YELLOW}Test préliminaire: Création d'un place pour les tests${NC}"
PLACE_RESPONSE=$(curl -s -L -X 'POST' \
  "$PLACE_ENDPOINT" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Place for Reviews",
  "description": "A place to test reviews",
  "price": 100.0,
  "latitude": 37.7749,
  "longitude": -122.4194,
  "owner_id": "'"$USER_ID"'",
  "amenities": []
}')

PLACE_ID=$(echo "$PLACE_RESPONSE" | jq -r '.id // empty')
echo "ID place extrait: $PLACE_ID"

if [[ -z "$PLACE_ID" ]]; then
  echo -e "${RED}✗ Échec de la création de place pour les tests. Arrêt des tests.${NC}\n"
  echo "Réponse complète: $PLACE_RESPONSE"
  exit 1
fi

# 1. Création d'une review valide
echo -e "${YELLOW}Test 1: Création d'une review valide${NC}"
CREATE_RESPONSE=$(curl -s -L -X 'POST' \
  "$REVIEW_ENDPOINT" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "Great place to stay!",
  "rating": 5,
  "user_id": "'"$USER_ID"'",
  "place_id": "'"$PLACE_ID"'"
}')

echo "Réponse: $CREATE_RESPONSE"

# Extraction de l'ID
REVIEW_ID=$(echo "$CREATE_RESPONSE" | jq -r '.id // empty')
echo "ID review extrait: $REVIEW_ID"

if [[ -n "$REVIEW_ID" ]]; then
  echo -e "${GREEN}✓ Création de review réussie. ID: $REVIEW_ID${NC}\n"
else
  echo -e "${RED}✗ Échec de la création de review${NC}\n"
fi

# 2. Création d'une review avec un utilisateur inexistant
echo -e "${YELLOW}Test 2: Création d'une review avec utilisateur inexistant${NC}"
INVALID_USER_RESPONSE=$(curl -s -L -X 'POST' \
  "$REVIEW_ENDPOINT" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "Invalid user review",
  "rating": 4,
  "user_id": "invalid_user_id",
  "place_id": "'"$PLACE_ID"'"
}')

echo "Réponse: $INVALID_USER_RESPONSE"

if [[ $INVALID_USER_RESPONSE == *"error"* ]]; then
  echo -e "${GREEN}✓ Détection correcte d'utilisateur invalide${NC}\n"
else
  echo -e "${RED}✗ Échec de la détection d'utilisateur invalide${NC}\n"
fi

# 3. Création d'une review avec un place inexistant
echo -e "${YELLOW}Test 3: Création d'une review avec place inexistant${NC}"
INVALID_PLACE_RESPONSE=$(curl -s -L -X 'POST' \
  "$REVIEW_ENDPOINT" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "Invalid place review",
  "rating": 3,
  "user_id": "'"$USER_ID"'",
  "place_id": "invalid_place_id"
}')

echo "Réponse: $INVALID_PLACE_RESPONSE"

if [[ $INVALID_PLACE_RESPONSE == *"error"* ]]; then
  echo -e "${GREEN}✓ Détection correcte de place invalide${NC}\n"
else
  echo -e "${RED}✗ Échec de la détection de place invalide${NC}\n"
fi

# 4. Création d'une review avec une note invalide
echo -e "${YELLOW}Test 4: Création d'une review avec note invalide${NC}"
INVALID_RATING_RESPONSE=$(curl -s -L -X 'POST' \
  "$REVIEW_ENDPOINT" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "Invalid rating review",
  "rating": 10,
  "user_id": "'"$USER_ID"'",
  "place_id": "'"$PLACE_ID"'"
}')

echo "Réponse: $INVALID_RATING_RESPONSE"

if [[ $INVALID_RATING_RESPONSE == *"error"* ]]; then
  echo -e "${GREEN}✓ Détection correcte de note invalide${NC}\n"
else
  echo -e "${RED}✗ Échec de la détection de note invalide${NC}\n"
fi

# 5. Récupération de toutes les reviews
echo -e "${YELLOW}Test 5: Récupération de toutes les reviews${NC}"
GET_ALL_RESPONSE=$(curl -s -L -X 'GET' \
  "$REVIEW_ENDPOINT" \
  -H 'accept: application/json')

echo "Réponse: $GET_ALL_RESPONSE"

if [[ $(echo "$GET_ALL_RESPONSE" | jq 'length') -gt 0 ]]; then
  echo -e "${GREEN}✓ Récupération de la liste des reviews réussie${NC}\n"
else
  echo -e "${RED}✗ Échec de la récupération de la liste des reviews${NC}\n"
fi

# 6. Récupération d'une review par ID
echo -e "${YELLOW}Test 6: Récupération d'une review par ID${NC}"
if [[ -n "$REVIEW_ID" ]]; then
  echo "Tentative de récupération pour l'ID: $REVIEW_ID"
  GET_REVIEW_RESPONSE=$(curl -s -L -X 'GET' \
    "$REVIEW_ENDPOINT/$REVIEW_ID" \
    -H 'accept: application/json')
  
  echo "Réponse: $GET_REVIEW_RESPONSE"
  
  RETRIEVED_ID=$(echo "$GET_REVIEW_RESPONSE" | jq -r '.id // empty')
  RETRIEVED_TEXT=$(echo "$GET_REVIEW_RESPONSE" | jq -r '.text // empty')
  RETRIEVED_RATING=$(echo "$GET_REVIEW_RESPONSE" | jq -r '.rating // empty')
  
  if [[ "$RETRIEVED_ID" == "$REVIEW_ID" && "$RETRIEVED_TEXT" == "Great place to stay!" && "$RETRIEVED_RATING" -eq 5 ]]; then
    echo -e "${GREEN}✓ Récupération de la review réussie${NC}\n"
  else
    echo -e "${RED}✗ Échec de la récupération de la review${NC}\n"
  fi
else
  echo -e "${RED}✗ ID review non disponible pour le test${NC}\n"
fi

# 7. Récupération de toutes les reviews d'un place par son ID
echo -e "${YELLOW}Test 7: Récupération des reviews par place ID${NC}"
REVIEWS_BY_PLACE_RESPONSE=$(curl -s -L -X 'GET' \
  "$PLACE_ENDPOINT/$PLACE_ID/reviews" \
  -H 'accept: application/json')

echo "Réponse: $REVIEWS_BY_PLACE_RESPONSE"

if [[ $(echo "$REVIEWS_BY_PLACE_RESPONSE" | jq 'length') -gt 0 ]]; then
  REVIEW_IN_PLACE=$(echo "$REVIEWS_BY_PLACE_RESPONSE" | jq --arg id "$REVIEW_ID" 'map(.id) | contains([$id])' 2>/dev/null)
  
  if [[ "$REVIEW_IN_PLACE" == "true" ]]; then
    echo -e "${GREEN}✓ Récupération des reviews par place ID réussie${NC}\n"
  else
    echo -e "${RED}✗ La review n'est pas trouvée dans les reviews du place${NC}\n"
  fi
else
  echo -e "${RED}✗ Aucune review trouvée pour ce place${NC}\n"
fi

# 8. Mise à jour d'une review
echo -e "${YELLOW}Test 8: Mise à jour d'une review${NC}"
if [[ -n "$REVIEW_ID" ]]; then
  echo "Tentative de mise à jour pour l'ID: $REVIEW_ID"
  UPDATE_RESPONSE=$(curl -s -L -X 'PUT' \
    "$REVIEW_ENDPOINT/$REVIEW_ID" \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "text": "Updated review text",
    "rating": 4
  }')
  
  echo "Réponse: $UPDATE_RESPONSE"
  
  UPDATED_TEXT=$(echo "$UPDATE_RESPONSE" | jq -r '.text // empty')
  UPDATED_RATING=$(echo "$UPDATE_RESPONSE" | jq -r '.rating // empty')
  
  if [[ "$UPDATED_TEXT" == "Updated review text" && "$UPDATED_RATING" -eq 4 ]]; then
    echo -e "${GREEN}✓ Mise à jour de la review réussie${NC}\n"
  else
    echo -e "${RED}✗ Échec de la mise à jour de la review${NC}\n"
  fi
else
  echo -e "${RED}✗ ID review non disponible pour le test${NC}\n"
fi

# 9. Mise à jour avec note invalide
echo -e "${YELLOW}Test 9: Mise à jour avec note invalide${NC}"
if [[ -n "$REVIEW_ID" ]]; then
  INVALID_UPDATE_RESPONSE=$(curl -s -L -X 'PUT' \
    "$REVIEW_ENDPOINT/$REVIEW_ID" \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "rating": 0
  }')
  
  echo "Réponse: $INVALID_UPDATE_RESPONSE"
  
  if [[ $INVALID_UPDATE_RESPONSE == *"error"* ]]; then
    echo -e "${GREEN}✓ Détection correcte de note invalide lors de la mise à jour${NC}\n"
  else
    echo -e "${RED}✗ Échec de la détection de note invalide lors de la mise à jour${NC}\n"
  fi
else
  echo -e "${RED}✗ ID review non disponible pour le test${NC}\n"
fi

# 10. Mise à jour avec ID inexistant
echo -e "${YELLOW}Test 10: Mise à jour avec ID inexistant${NC}"
INVALID_ID_UPDATE_RESPONSE=$(curl -s -L -X 'PUT' \
  "$REVIEW_ENDPOINT/invalid_id_12345" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "This should not work",
  "rating": 2
}')

echo "Réponse: $INVALID_ID_UPDATE_RESPONSE"

if [[ $INVALID_ID_UPDATE_RESPONSE == *"not found"* || $INVALID_ID_UPDATE_RESPONSE == *"error"* ]]; then
  echo -e "${GREEN}✓ Gestion correcte de mise à jour avec ID inexistant${NC}\n"
else
  echo -e "${RED}✗ Mauvaise gestion de mise à jour avec ID inexistant${NC}\n"
fi

# 11. Suppression d'une review
echo -e "${YELLOW}Test 11: Suppression d'une review${NC}"
if [[ -n "$REVIEW_ID" ]]; then
  echo "Tentative de suppression pour l'ID: $REVIEW_ID"
  DELETE_RESPONSE=$(curl -s -L -X 'DELETE' \
    "$REVIEW_ENDPOINT/$REVIEW_ID" \
    -H 'accept: application/json')
  
  echo "Réponse: $DELETE_RESPONSE"
  
  if [[ $DELETE_RESPONSE == *"successfully"* || $DELETE_RESPONSE == *"success"* ]]; then
    echo -e "${GREEN}✓ Suppression de la review réussie${NC}\n"
  else
    echo -e "${RED}✗ Échec de la suppression de la review${NC}\n"
  fi
else
  echo -e "${RED}✗ ID review non disponible pour le test${NC}\n"
fi

# 12. Suppression avec ID inexistant
echo -e "${YELLOW}Test 12: Suppression avec ID inexistant${NC}"
INVALID_DELETE_RESPONSE=$(curl -s -L -X 'DELETE' \
  "$REVIEW_ENDPOINT/invalid_id_12345" \
  -H 'accept: application/json')

echo "Réponse: $INVALID_DELETE_RESPONSE"

if [[ $INVALID_DELETE_RESPONSE == *"not found"* || $INVALID_DELETE_RESPONSE == *"error"* ]]; then
  echo -e "${GREEN}✓ Gestion correcte de suppression avec ID inexistant${NC}\n"
else
  echo -e "${RED}✗ Mauvaise gestion de suppression avec ID inexistant${NC}\n"
fi

# 13. Vérification que la review a bien été supprimée
echo -e "${YELLOW}Test 13: Vérification que la review a bien été supprimée${NC}"
if [[ -n "$REVIEW_ID" ]]; then
  VERIFY_DELETE_RESPONSE=$(curl -s -L -X 'GET' \
    "$REVIEW_ENDPOINT/$REVIEW_ID" \
    -H 'accept: application/json')
  
  echo "Réponse: $VERIFY_DELETE_RESPONSE"
  
  if [[ $VERIFY_DELETE_RESPONSE == *"not found"* || $VERIFY_DELETE_RESPONSE == *"error"* ]]; then
    echo -e "${GREEN}✓ La review a bien été supprimée${NC}\n"
  else
    echo -e "${RED}✗ La review existe toujours après suppression${NC}\n"
  fi
else
  echo -e "${RED}✗ ID review non disponible pour le test${NC}\n"
fi

# 14. Création d'une nouvelle review pour vérifier la mise à jour de place_detail
echo -e "${YELLOW}Test 14: Création d'une nouvelle review et vérification dans les détails du place${NC}"
NEW_REVIEW_RESPONSE=$(curl -s -L -X 'POST' \
  "$REVIEW_ENDPOINT" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "Another great review",
  "rating": 5,
  "user_id": "'"$USER_ID"'",
  "place_id": "'"$PLACE_ID"'"
}')

NEW_REVIEW_ID=$(echo "$NEW_REVIEW_RESPONSE" | jq -r '.id // empty')
echo "ID nouvelle review: $NEW_REVIEW_ID"

if [[ -n "$NEW_REVIEW_ID" ]]; then
  # Vérifier si la review apparaît dans les détails du place
  PLACE_DETAILS_RESPONSE=$(curl -s -L -X 'GET' \
    "$PLACE_ENDPOINT/$PLACE_ID" \
    -H 'accept: application/json')
  
  echo "Réponse détails place: $PLACE_DETAILS_RESPONSE"
  
  # Vérifier si la structure du JSON contient des reviews
  HAS_REVIEWS=$(echo "$PLACE_DETAILS_RESPONSE" | jq 'has("reviews")' 2>/dev/null)
  
  if [[ "$HAS_REVIEWS" == "true" ]]; then
    # Vérifier si notre nouvelle review est présente
    REVIEW_IN_PLACE=$(echo "$PLACE_DETAILS_RESPONSE" | jq --arg id "$NEW_REVIEW_ID" '.reviews | map(.id) | contains([$id])' 2>/dev/null)
    
    if [[ "$REVIEW_IN_PLACE" == "true" ]]; then
      echo -e "${GREEN}✓ La nouvelle review apparaît dans les détails du place${NC}\n"
    else
      echo -e "${RED}✗ La nouvelle review n'apparaît pas dans les détails du place${NC}\n"
    fi
  else
    echo -e "${RED}✗ Les détails du place ne contiennent pas de champ 'reviews'${NC}\n"
  fi
else
  echo -e "${RED}✗ Échec de la création d'une nouvelle review pour le test${NC}\n"
fi

echo -e "${BLUE}┌────────────────────────────────────────────┐${NC}"
echo -e "${BLUE}│              TESTS TERMINÉS                │${NC}"
echo -e "${BLUE}└────────────────────────────────────────────┘${NC}"
