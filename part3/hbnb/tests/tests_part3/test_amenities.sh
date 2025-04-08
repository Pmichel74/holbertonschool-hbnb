#!/bin/bash

# Couleurs pour une meilleure lisibilité
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Symboles pour les résultats
CHECK_MARK="\xE2\x9C\x94"
CROSS_MARK="\xE2\x9C\x96"

# URL de base de l'API
API_URL="http://localhost:5000/api/v1"

# Mode debug - affiche les commandes curl complètes (1=oui, 0=non)
DEBUG_MODE=0

# Générer des valeurs uniques pour éviter les erreurs de duplication
TIMESTAMP=$(date +%s)
WIFI_NAME="WiFi_${TIMESTAMP}"
POOL_NAME="Swimming Pool_${TIMESTAMP}"

# Fonction pour valider et afficher le résultat
validate_test() {
    local test_name="$1"
    local status="$2"
    local response="$3"
    local expected_status="$4"
    
    if [ "$status" -eq "$expected_status" ]; then
        local result="${GREEN}${CHECK_MARK} Test réussi: ${test_name}${NC}"
        echo -e "$result"
    else
        local result="${RED}${CROSS_MARK} Test échoué: ${test_name} (Code: ${status}, Attendu: ${expected_status})${NC}"
        echo -e "$result"
        
        # Afficher des messages d'aide selon le type d'erreur
        if [[ "$response" == *"token"* && "$response" == *"not yet valid"* ]]; then
            echo -e "${YELLOW}⚠️ Problème de synchronisation d'horloge détecté!${NC}"
        elif [[ "$response" == *"Invalid credentials"* ]]; then
            echo -e "${YELLOW}⚠️ Identifiants incorrects. L'utilisateur existe-t-il et le mot de passe est-il correct?${NC}"
        elif [[ "$response" == *"already exists"* ]]; then
            echo -e "${YELLOW}⚠️ L'entité existe déjà. Utilisez un nom différent.${NC}"
        elif [[ "$response" == *"no token"* || "$response" == *"missing"* ]]; then
            echo -e "${YELLOW}⚠️ Token manquant dans la requête.${NC}"
        elif [[ "$response" == *"invalid token"* || "$response" == *"expired"* ]]; then
            echo -e "${YELLOW}⚠️ Token invalide ou expiré.${NC}"
        elif [[ "$response" == *"not found"* ]]; then
            echo -e "${YELLOW}⚠️ La ressource demandée n'existe pas.${NC}"
        elif [[ "$response" == *"privileges required"* || "$response" == *"Admin privileges"* ]]; then
            echo -e "${YELLOW}⚠️ Privilèges insuffisants pour effectuer cette action.${NC}"
        fi
    fi
    
    # Afficher la réponse avec une couleur correspondant au statut
    if [ "$status" -ge 200 ] && [ "$status" -lt 300 ]; then
        echo -e "${CYAN}$response${NC}"
    elif [ "$status" -ge 400 ]; then
        echo -e "${PURPLE}$response${NC}"
    else
        echo "$response"
    fi
}

# Fonction pour exécuter une requête curl avec affichage des détails en mode debug
debug_curl() {
    local curl_cmd="$1"
    
    if [ "$DEBUG_MODE" -eq 1 ]; then
        echo -e "${BLUE}Exécution de: $curl_cmd${NC}"
    fi
    
    # Exécute la commande curl et retourne le résultat
    eval "$curl_cmd"
}

# Fonction pour extraire le token JWT
extract_token_simple() {
    local json_response="$1"
    echo "$json_response" > /tmp/token_response.json
    
    if grep -q "access_token" /tmp/token_response.json; then
        local token_line=$(grep "access_token" /tmp/token_response.json)
        local token=$(echo "$token_line" | sed -E 's/.*"access_token"[^"]*"([^"]+)".*/\1/')
        echo "$token"
    else
        echo ""
    fi
}

# Fonction pour extraire l'ID
extract_id_simple() {
    local json_response="$1"
    echo "$json_response" > /tmp/id_response.json
    
    if grep -q "\"id\"" /tmp/id_response.json; then
        local id_line=$(grep "\"id\"" /tmp/id_response.json)
        local id=$(echo "$id_line" | sed -E 's/.*"id"[^"]*"([^"]+)".*/\1/')
        echo "$id"
    else
        echo ""
    fi
}

echo -e "${YELLOW}=== Test de l'API amenities ===${NC}\n"

# 1. Connexion avec un administrateur
echo -e "\n${YELLOW}1. Connexion avec un administrateur${NC}"
ADMIN_LOGIN_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/auth/login\" -H \"Content-Type: application/json\" -d '{\"email\": \"admin@hbnb.io\", \"password\": \"admin1234\"}'"
ADMIN_LOGIN_RESPONSE=$(debug_curl "$ADMIN_LOGIN_CMD")
ADMIN_LOGIN_STATUS=${ADMIN_LOGIN_RESPONSE: -3}
ADMIN_LOGIN=${ADMIN_LOGIN_RESPONSE:0:${#ADMIN_LOGIN_RESPONSE}-3}
validate_test "Connexion administrateur" "$ADMIN_LOGIN_STATUS" "$ADMIN_LOGIN" 200

# Extraction du token JWT admin
ADMIN_TOKEN=$(extract_token_simple "$ADMIN_LOGIN")
echo -e "\n${GREEN}Token JWT admin extrait:${NC} $ADMIN_TOKEN"

if [ -z "$ADMIN_TOKEN" ]; then
    echo -e "\n${RED}Échec d'extraction du token admin. Tentative de secours...${NC}"
    ADMIN_TOKEN=$(echo "$ADMIN_LOGIN" | grep -o 'eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*')
    
    if [ -n "$ADMIN_TOKEN" ]; then
        echo -e "${GREEN}Token JWT admin récupéré par méthode alternative:${NC} $ADMIN_TOKEN"
    else
        echo -e "${RED}Échec critique de récupération du token. Impossible de continuer.${NC}"
        exit 1
    fi
fi

# 2. Création d'un utilisateur normal
echo -e "\n${YELLOW}2. Création d'un utilisateur normal${NC}"
USER_EMAIL="user_test_${TIMESTAMP}@example.com" 
USER_PASSWORD="password123"
CREATE_USER_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/users/\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $ADMIN_TOKEN\" -d '{\"email\": \"$USER_EMAIL\", \"password\": \"$USER_PASSWORD\", \"first_name\": \"Test\", \"last_name\": \"User\"}'"
CREATE_USER_FULL=$(debug_curl "$CREATE_USER_CMD")
CREATE_USER_STATUS=${CREATE_USER_FULL: -3}
CREATE_USER=${CREATE_USER_FULL:0:${#CREATE_USER_FULL}-3}
validate_test "Création utilisateur normal" "$CREATE_USER_STATUS" "$CREATE_USER" 201

# 3. Connexion avec l'utilisateur normal
echo -e "\n${YELLOW}3. Connexion avec l'utilisateur normal${NC}"
USER_LOGIN_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/auth/login\" -H \"Content-Type: application/json\" -d '{\"email\": \"$USER_EMAIL\", \"password\": \"$USER_PASSWORD\"}'"
USER_LOGIN_RESPONSE=$(debug_curl "$USER_LOGIN_CMD")
USER_LOGIN_STATUS=${USER_LOGIN_RESPONSE: -3}
USER_LOGIN=${USER_LOGIN_RESPONSE:0:${#USER_LOGIN_RESPONSE}-3}
validate_test "Connexion utilisateur normal" "$USER_LOGIN_STATUS" "$USER_LOGIN" 200

# Extraction du token JWT utilisateur
USER_TOKEN=$(extract_token_simple "$USER_LOGIN")
echo -e "\n${GREEN}Token JWT utilisateur normal extrait:${NC} $USER_TOKEN"

if [ -z "$USER_TOKEN" ]; then
    echo -e "\n${RED}Échec d'extraction du token utilisateur. Tentative de secours...${NC}"
    USER_TOKEN=$(echo "$USER_LOGIN" | grep -o 'eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*')
    
    if [ -n "$USER_TOKEN" ]; then
        echo -e "${GREEN}Token JWT utilisateur récupéré par méthode alternative:${NC} $USER_TOKEN"
    else
        echo -e "${RED}Échec critique de récupération du token. Impossible de continuer.${NC}"
        exit 1
    fi
fi

# 4. Tentative de création d'une amenity par un utilisateur normal (doit échouer)
echo -e "\n${YELLOW}4. Tentative de création d'une amenity par un utilisateur normal${NC}"
USER_AMENITY_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/amenities/\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $USER_TOKEN\" -d '{\"name\": \"$POOL_NAME\"}'"
USER_AMENITY_FULL=$(debug_curl "$USER_AMENITY_CMD")
USER_AMENITY_STATUS=${USER_AMENITY_FULL: -3}
USER_AMENITY=${USER_AMENITY_FULL:0:${#USER_AMENITY_FULL}-3}
validate_test "Création amenity par utilisateur normal" "$USER_AMENITY_STATUS" "$USER_AMENITY" 403

# 5. Création d'une amenity par l'administrateur
echo -e "\n${YELLOW}5. Création d'une amenity par l'administrateur${NC}"
AMENITY_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/amenities/\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $ADMIN_TOKEN\" -d '{\"name\": \"$WIFI_NAME\"}'"
AMENITY_RESPONSE_FULL=$(debug_curl "$AMENITY_CMD")
AMENITY_RESPONSE_STATUS=${AMENITY_RESPONSE_FULL: -3}
AMENITY_RESPONSE=${AMENITY_RESPONSE_FULL:0:${#AMENITY_RESPONSE_FULL}-3}
validate_test "Création amenity par admin" "$AMENITY_RESPONSE_STATUS" "$AMENITY_RESPONSE" 201

# Extraction de l'ID amenity
AMENITY_ID=$(extract_id_simple "$AMENITY_RESPONSE")
echo -e "\n${GREEN}ID amenity extrait:${NC} $AMENITY_ID"

if [ -z "$AMENITY_ID" ]; then
    echo -e "\n${RED}Échec d'extraction de l'ID amenity. Tentative de secours...${NC}"
    AMENITY_ID=$(echo "$AMENITY_RESPONSE" | grep -o '[0-9a-f]\{8\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{12\}')
    
    if [ -n "$AMENITY_ID" ]; then
        echo -e "${GREEN}ID amenity récupéré par méthode alternative:${NC} $AMENITY_ID"
    else
        echo -e "${RED}Échec critique de récupération de l'ID. Impossible de continuer.${NC}"
        exit 1
    fi
fi

# 6. Récupérer toutes les amenities (accessible à tous)
echo -e "\n${YELLOW}6. Récupération de toutes les amenities${NC}"
ALL_AMENITIES_CMD="curl -s -w \"%{http_code}\" -X GET \"$API_URL/amenities/\" -H \"Content-Type: application/json\""
ALL_AMENITIES_FULL=$(debug_curl "$ALL_AMENITIES_CMD")
ALL_AMENITIES_STATUS=${ALL_AMENITIES_FULL: -3}
ALL_AMENITIES=${ALL_AMENITIES_FULL:0:${#ALL_AMENITIES_FULL}-3}
validate_test "Liste de toutes les amenities" "$ALL_AMENITIES_STATUS" "$ALL_AMENITIES" 200

# 7. Récupérer une amenity spécifique (accessible à tous)
echo -e "\n${YELLOW}7. Récupération d'une amenity spécifique${NC}"
SPECIFIC_AMENITY_CMD="curl -s -w \"%{http_code}\" -X GET \"$API_URL/amenities/$AMENITY_ID\" -H \"Content-Type: application/json\""
SPECIFIC_AMENITY_FULL=$(debug_curl "$SPECIFIC_AMENITY_CMD")
SPECIFIC_AMENITY_STATUS=${SPECIFIC_AMENITY_FULL: -3}
SPECIFIC_AMENITY=${SPECIFIC_AMENITY_FULL:0:${#SPECIFIC_AMENITY_FULL}-3}
validate_test "Récupération amenity spécifique" "$SPECIFIC_AMENITY_STATUS" "$SPECIFIC_AMENITY" 200

# 8. Tentative de modification d'une amenity par un utilisateur normal (doit échouer)
echo -e "\n${YELLOW}8. Tentative de modification d'une amenity par un utilisateur normal${NC}"
USER_UPDATE_CMD="curl -s -w \"%{http_code}\" -X PUT \"$API_URL/amenities/$AMENITY_ID\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $USER_TOKEN\" -d '{\"name\": \"User Modified Amenity\"}'"
USER_UPDATE_FULL=$(debug_curl "$USER_UPDATE_CMD")
USER_UPDATE_STATUS=${USER_UPDATE_FULL: -3}
USER_UPDATE=${USER_UPDATE_FULL:0:${#USER_UPDATE_FULL}-3}
validate_test "Modification amenity par utilisateur normal" "$USER_UPDATE_STATUS" "$USER_UPDATE" 403

# 9. Modifier une amenity par l'administrateur (devrait réussir)
echo -e "\n${YELLOW}9. Modification d'une amenity par l'administrateur${NC}"
MODIFIED_NAME="Admin Modified ${WIFI_NAME}"
ADMIN_UPDATE_CMD="curl -s -w \"%{http_code}\" -X PUT \"$API_URL/amenities/$AMENITY_ID\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $ADMIN_TOKEN\" -d '{\"name\": \"$MODIFIED_NAME\"}'"
ADMIN_UPDATE_FULL=$(debug_curl "$ADMIN_UPDATE_CMD")
ADMIN_UPDATE_STATUS=${ADMIN_UPDATE_FULL: -3}
ADMIN_UPDATE=${ADMIN_UPDATE_FULL:0:${#ADMIN_UPDATE_FULL}-3}
validate_test "Modification amenity par admin" "$ADMIN_UPDATE_STATUS" "$ADMIN_UPDATE" 200

# 10. Vérifier la modification
echo -e "\n${YELLOW}10. Vérification de la modification${NC}"
VERIFY_UPDATE_CMD="curl -s -w \"%{http_code}\" -X GET \"$API_URL/amenities/$AMENITY_ID\" -H \"Content-Type: application/json\""
VERIFY_UPDATE_FULL=$(debug_curl "$VERIFY_UPDATE_CMD")
VERIFY_UPDATE_STATUS=${VERIFY_UPDATE_FULL: -3}
VERIFY_UPDATE=${VERIFY_UPDATE_FULL:0:${#VERIFY_UPDATE_FULL}-3}
validate_test "Vérification modification" "$VERIFY_UPDATE_STATUS" "$VERIFY_UPDATE" 200

# 11. Tentative de modification d'une amenity sans nom par l'admin (doit échouer)
echo -e "\n${YELLOW}11. Tentative de modification d'une amenity sans nom${NC}"
EMPTY_NAME_CMD="curl -s -w \"%{http_code}\" -X PUT \"$API_URL/amenities/$AMENITY_ID\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $ADMIN_TOKEN\" -d '{\"name\": \"\"}'"
EMPTY_NAME_FULL=$(debug_curl "$EMPTY_NAME_CMD")
EMPTY_NAME_STATUS=${EMPTY_NAME_FULL: -3}
EMPTY_NAME=${EMPTY_NAME_FULL:0:${#EMPTY_NAME_FULL}-3}
validate_test "Modification d'une amenity sans nom" "$EMPTY_NAME_STATUS" "$EMPTY_NAME" 400

# 12. Tentative de récupération d'une amenity avec un ID invalide
echo -e "\n${YELLOW}12. Récupération d'une amenity avec un ID invalide${NC}"
INVALID_ID="00000000-0000-0000-0000-000000000000"
INVALID_ID_CMD="curl -s -w \"%{http_code}\" -X GET \"$API_URL/amenities/$INVALID_ID\" -H \"Content-Type: application/json\""
INVALID_ID_FULL=$(debug_curl "$INVALID_ID_CMD")
INVALID_ID_STATUS=${INVALID_ID_FULL: -3}
INVALID_ID=${INVALID_ID_FULL:0:${#INVALID_ID_FULL}-3}
validate_test "Récupération d'une amenity avec ID invalide" "$INVALID_ID_STATUS" "$INVALID_ID" 404

echo -e "\n${GREEN}Tests amenities terminés.${NC}"