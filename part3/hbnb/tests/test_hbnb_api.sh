#!/bin/bash
# filepath: /home/jbn/test_hbnb_api.sh

# Couleurs pour une meilleure lisibilité
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# URL de base de l'API
API_URL="http://localhost:5000/api/v1"

# Variables pour stocker les tokens et IDs
ACCESS_TOKEN=""
USER1_ID=""
USER2_ID=""
PLACE_ID=""
REVIEW_ID=""
AMENITY_ID=""

echo -e "${BLUE}=== Script de test de l'API HBnB ===${NC}\n"

# Fonction pour afficher des en-têtes de section
section() {
    echo -e "\n${YELLOW}=== $1 ===${NC}"
}

# Fonction pour exécuter une requête curl et afficher le résultat
# Usage: do_curl "Description" "méthode" "endpoint" "données"
do_curl() {
    local description=$1
    local method=$2
    local endpoint=$3
    local data=$4
    local auth_header=""
    
    echo -e "\n${BLUE}>> $description${NC}"
    
    if [ ! -z "$ACCESS_TOKEN" ]; then
        auth_header="-H \"Authorization: Bearer $ACCESS_TOKEN\""
    fi
    
    local cmd="curl -s -X $method \"$API_URL$endpoint\" \
        -H \"Content-Type: application/json\" \
        $auth_header \
        -d '$data'"
    
    echo -e "${YELLOW}Commande:${NC} $cmd"
    
    # Exécuter la commande et stocker la réponse
    local response=""
    if [ ! -z "$data" ]; then
        response=$(curl -s -X $method "$API_URL$endpoint" \
                -H "Content-Type: application/json" \
                ${ACCESS_TOKEN:+-H "Authorization: Bearer $ACCESS_TOKEN"} \
                -d "$data")
    else
        response=$(curl -s -X $method "$API_URL$endpoint" \
                -H "Content-Type: application/json" \
                ${ACCESS_TOKEN:+-H "Authorization: Bearer $ACCESS_TOKEN"})
    fi
    
    echo -e "${GREEN}Réponse:${NC} $response"
    echo "$response"  # Pour pouvoir capturer la réponse dans une variable
}

# 1. Inscription d'utilisateurs
section "Inscription des utilisateurs"

# Créer le premier utilisateur (propriétaire)
USER1=$(do_curl "Création du premier utilisateur (propriétaire)" "POST" "/users/" '{
    "email": "owner@example.com",
    "password": "password123",
    "first_name": "John",
    "last_name": "Owner"
}')

# Extraire l'ID du premier utilisateur
USER1_ID=$(echo $USER1 | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo -e "ID du premier utilisateur: $USER1_ID"

# Créer le deuxième utilisateur (client)
USER2=$(do_curl "Création du deuxième utilisateur (client)" "POST" "/users/" '{
    "email": "client@example.com",
    "password": "password456",
    "first_name": "Jane",
    "last_name": "Client"
}')

# Extraire l'ID du deuxième utilisateur
USER2_ID=$(echo $USER2 | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo -e "ID du deuxième utilisateur: $USER2_ID"

# 2. Connexion des utilisateurs
section "Connexion des utilisateurs"

# Connexion du premier utilisateur (propriétaire)
LOGIN1=$(do_curl "Connexion du propriétaire" "POST" "/auth/login" '{
    "email": "owner@example.com",
    "password": "password123"
}')

# Extraire le token du premier utilisateur
ACCESS_TOKEN=$(echo $LOGIN1 | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
echo -e "Token du propriétaire: $ACCESS_TOKEN"

# 3. Création d'une amenity
section "Création d'amenities"

AMENITY1=$(do_curl "Création d'une première amenity" "POST" "/amenities/" '{
    "name": "WiFi"
}')

# Extraire l'ID de l'amenity
AMENITY1_ID=$(echo $AMENITY1 | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo -e "ID de l'amenity WiFi: $AMENITY1_ID"

AMENITY2=$(do_curl "Création d'une deuxième amenity" "POST" "/amenities/" '{
    "name": "Swimming Pool"
}')

# Extraire l'ID de la deuxième amenity
AMENITY2_ID=$(echo $AMENITY2 | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo -e "ID de l'amenity Swimming Pool: $AMENITY2_ID"

# 4. Création d'un place par le propriétaire
section "Création d'un logement"

PLACE=$(do_curl "Création d'un logement par le propriétaire" "POST" "/places/" "{
    \"title\": \"Bel appartement\",
    \"description\": \"Un magnifique appartement avec vue\",
    \"price\": 100,
    \"latitude\": 48.8566,
    \"longitude\": 2.3522,
    \"amenities\": [\"$AMENITY1_ID\", \"$AMENITY2_ID\"]
}")

# Extraire l'ID du logement
PLACE_ID=$(echo $PLACE | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo -e "ID du logement: $PLACE_ID"

# 5. Récupération des détails du logement
section "Récupération des détails du logement"

do_curl "Récupération des détails du logement" "GET" "/places/$PLACE_ID" ""

# 6. Connexion du deuxième utilisateur (client)
section "Connexion du client"

LOGIN2=$(do_curl "Connexion du client" "POST" "/auth/login" '{
    "email": "client@example.com",
    "password": "password456"
}')

# Extraire le token du deuxième utilisateur
ACCESS_TOKEN=$(echo $LOGIN2 | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
echo -e "Token du client: $ACCESS_TOKEN"

# 7. Création d'une review par le client
section "Création d'une review"

REVIEW=$(do_curl "Création d'une review par le client" "POST" "/reviews/" "{
    \"place_id\": \"$PLACE_ID\",
    \"rating\": 4,
    \"text\": \"Très bon séjour, je recommande!\"
}")

# Extraire l'ID de la review
REVIEW_ID=$(echo $REVIEW | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo -e "ID de la review: $REVIEW_ID"

# 8. Tentative de création d'une deuxième review par le même client (doit échouer)
section "Tentative de deuxième review (même utilisateur)"

do_curl "Tentative de création d'une deuxième review (même client)" "POST" "/reviews/" "{
    \"place_id\": \"$PLACE_ID\",
    \"rating\": 5,
    \"text\": \"Deuxième commentaire qui devrait échouer\"
}"

# 9. Connexion du troisième utilisateur (autre client)
section "Création et connexion d'un troisième utilisateur"

# Créer le troisième utilisateur
USER3=$(do_curl "Création du troisième utilisateur" "POST" "/users/" '{
    "email": "client2@example.com",
    "password": "password789",
    "first_name": "Alice",
    "last_name": "Another"
}')

# Connexion du troisième utilisateur
LOGIN3=$(do_curl "Connexion du troisième utilisateur" "POST" "/auth/login" '{
    "email": "client2@example.com",
    "password": "password789"
}')

# Extraire le token du troisième utilisateur
ACCESS_TOKEN=$(echo $LOGIN3 | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
echo -e "Token du troisième utilisateur: $ACCESS_TOKEN"

# 10. Création d'une review par le troisième utilisateur (devrait réussir)
section "Création d'une review par un autre utilisateur"

REVIEW2=$(do_curl "Création d'une review par un autre client" "POST" "/reviews/" "{
    \"place_id\": \"$PLACE_ID\",
    \"rating\": 5,
    \"text\": \"Excellent logement, très propre!\"
}")

# 11. Récupération des reviews du logement
section "Récupération des reviews du logement"

do_curl "Récupération des reviews du logement" "GET" "/places/$PLACE_ID/reviews" ""

# 12. Modification d'une review
section "Modification d'une review"

do_curl "Modification de la review" "PUT" "/reviews/$REVIEW_ID" '{
    "rating": 5,
    "text": "J\'ai modifié mon avis, c\'était parfait!"
}'

# 13. Récupération de toutes les amenities
section "Récupération des amenities"

do_curl "Liste des amenities" "GET" "/amenities/" ""

# 14. Récupération des amenities d'un logement
section "Récupération des amenities du logement"

do_curl "Amenities du logement" "GET" "/places/$PLACE_ID/amenities" ""

echo -e "\n${GREEN}Tests terminés!${NC}"