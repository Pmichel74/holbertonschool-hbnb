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

# Nombre maximum de tentatives pour les requêtes curl
MAX_RETRIES=5
# Délai entre les tentatives (en secondes)
RETRY_DELAY=3

# Générer des valeurs uniques pour éviter les erreurs de duplication
TIMESTAMP=$(date +%s)
PLACE_NAME="Maison Test ${TIMESTAMP}"
CLIENT_EMAIL="client_${TIMESTAMP}@example.com"
CLIENT_PASSWORD="password456"
OWNER_EMAIL="owner_${TIMESTAMP}@example.com"
OWNER_PASSWORD="password123"

# Fonction pour valider et afficher le résultat
validate_test() {
    local test_name="$1"
    local status="$2"
    local response="$3"
    local expected_status="$4"
    
    if [ "$status" -eq "$expected_status" ]; then
        local result="${GREEN}${CHECK_MARK} Test réussi: ${test_name}${NC}"
        echo -e "$result"
    elif [ "$status" -eq 000 ]; then
        local result="${RED}${CROSS_MARK} Erreur de connexion: ${test_name} (Code: ${status})${NC}"
        echo -e "$result"
        echo -e "${YELLOW}⚠️ Problème de connexion au serveur. Vérifiez que l'API est en cours d'exécution.${NC}"
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
        elif [[ "$response" == *"no token"* || "$response" == *"missing"* || "$response" == *"Missing Authorization"* ]]; then
            echo -e "${YELLOW}⚠️ Token manquant dans la requête.${NC}"
        elif [[ "$response" == *"invalid token"* || "$response" == *"expired"* ]]; then
            echo -e "${YELLOW}⚠️ Token invalide ou expiré.${NC}"
        elif [[ "$response" == *"not found"* ]]; then
            echo -e "${YELLOW}⚠️ La ressource demandée n'existe pas.${NC}"
        elif [[ "$response" == *"privileges required"* || "$response" == *"Admin privileges"* ]]; then
            echo -e "${YELLOW}⚠️ Privilèges insuffisants pour effectuer cette action.${NC}"
        elif [[ "$response" == *"you are not the owner"* ]]; then
            echo -e "${YELLOW}⚠️ Vous n'êtes pas le propriétaire de cette ressource.${NC}"
        elif [[ "$response" == *"required property"* ]]; then
            echo -e "${YELLOW}⚠️ Un champ requis est manquant dans la requête.${NC}"
        fi
    fi
    
    # Afficher la réponse avec une couleur correspondant au statut
    if [ "$status" -ge 200 ] && [ "$status" -lt 300 ]; then
        echo -e "${CYAN}$response${NC}"
    elif [ "$status" -ge 400 ]; then
        echo -e "${PURPLE}$response${NC}"
    elif [ "$status" -ne 000 ]; then
        echo "$response"
    fi
}

# Fonction pour exécuter une requête curl avec affichage des détails en mode debug et retry
debug_curl_with_retry() {
    local curl_cmd="$1"
    local attempt=1
    local result=""
    local success=false
    
    if [ "$DEBUG_MODE" -eq 1 ]; then
        echo -e "${BLUE}Exécution de: $curl_cmd${NC}"
    fi
    
    while [ $attempt -le $MAX_RETRIES ]; do
        if [ $attempt -gt 1 ]; then
            echo -e "${YELLOW}Tentative $attempt de $MAX_RETRIES (délai: ${RETRY_DELAY}s)...${NC}"
            sleep $RETRY_DELAY
        fi
        
        # Augmenter le timeout de curl pour les connexions lentes
        result=$(eval "$curl_cmd --connect-timeout 10 --max-time 30") || true
        
        # Vérifier le résultat
        if [[ "$result" != *"000"* && -n "$result" ]]; then
            success=true
            break
        else
            echo -e "${YELLOW}Problème de connexion détecté, nouvelle tentative...${NC}"
            attempt=$((attempt + 1))
            # Augmenter le délai entre les tentatives
            RETRY_DELAY=$((RETRY_DELAY + 1))
        fi
    done
    
    if [ "$success" = false ]; then
        echo "000"
    else
        echo "$result"
    fi
}

# Fonction pour extraire le token JWT
extract_token_simple() {
    local json_response="$1"
    
    if [[ "$json_response" == *"access_token"* ]]; then
        local token=$(echo "$json_response" | grep -o '"access_token"[^"]*"[^"]*"' | sed 's/"access_token"[^"]*"\([^"]*\)"/\1/')
        echo "$token"
    else
        echo ""
    fi
}

# Fonction améliorée pour extraire l'ID
extract_id() {
    local json_response="$1"
    
    # Méthode 1: chercher le format standard "id": "uuid"
    if [[ "$json_response" == *"\"id\""* ]]; then
        local id=$(echo "$json_response" | grep -o '"id"[^"]*"[^"]*"' | head -1 | sed 's/"id"[^"]*"\([^"]*\)"/\1/')
        echo "$id"
        return
    fi
    
    # Méthode 2: chercher un UUID dans la réponse
    local uuid_pattern='[0-9a-f]\{8\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{12\}'
    local uuid=$(echo "$json_response" | grep -o "$uuid_pattern" | head -1)
    if [ -n "$uuid" ]; then
        echo "$uuid"
        return
    fi
    
    # Aucun ID trouvé
    echo ""
}

# Fonction pour vérifier l'API avant de commencer les tests
check_api_status() {
    echo -e "${YELLOW}Vérification de l'état de l'API...${NC}"
    local status_cmd="curl -s -o /dev/null -w \"%{http_code}\" --connect-timeout 5 $API_URL/status"
    local status=$(eval "$status_cmd" || echo "000")
    
    if [ "$status" = "000" ]; then
        echo -e "${RED}⚠️ L'API ne semble pas accessible. Vérifiez que le serveur est en cours d'exécution.${NC}"
        echo -e "${YELLOW}Tentative de connexion à: $API_URL/status${NC}"
        sleep 2
    else
        echo -e "${GREEN}API accessible (status code: $status). Début des tests...${NC}"
    fi
}

echo -e "${YELLOW}=== Test de l'API reviews ===${NC}\n"
check_api_status

# Étape préalable: Connexion avec un administrateur pour obtenir un token admin
echo -e "\n${YELLOW}Étape préalable: Connexion avec un administrateur${NC}"
ADMIN_LOGIN_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/auth/login\" -H \"Content-Type: application/json\" -d '{\"email\": \"admin@hbnb.io\", \"password\": \"admin1234\"}'"
ADMIN_LOGIN_FULL=$(debug_curl_with_retry "$ADMIN_LOGIN_CMD")
ADMIN_LOGIN_STATUS=${ADMIN_LOGIN_FULL: -3}
ADMIN_LOGIN=${ADMIN_LOGIN_FULL:0:${#ADMIN_LOGIN_FULL}-3}
validate_test "Connexion administrateur" "$ADMIN_LOGIN_STATUS" "$ADMIN_LOGIN" 200

# Extraction du token JWT admin
ADMIN_TOKEN=$(extract_token_simple "$ADMIN_LOGIN")
echo -e "\n${GREEN}Token JWT admin extrait:${NC} $ADMIN_TOKEN"

if [ -z "$ADMIN_TOKEN" ]; then
    echo -e "${RED}Échec d'extraction du token admin. Tentative de secours...${NC}"
    ADMIN_TOKEN=$(echo "$ADMIN_LOGIN" | grep -o 'eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*')
    if [ -n "$ADMIN_TOKEN" ]; then
        echo -e "${GREEN}Token JWT admin récupéré par méthode alternative:${NC} $ADMIN_TOKEN"
    else
        echo -e "${RED}Échec critique de récupération du token admin. Impossible de continuer.${NC}"
        exit 1
    fi
fi

# 1. Création d'un utilisateur propriétaire avec le token admin
echo -e "\n${YELLOW}1. Création d'un utilisateur propriétaire${NC}"
CREATE_OWNER_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/users/\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $ADMIN_TOKEN\" -d '{\"email\": \"$OWNER_EMAIL\", \"password\": \"$OWNER_PASSWORD\", \"first_name\": \"Owner\", \"last_name\": \"User\"}'"
CREATE_OWNER_FULL=$(debug_curl_with_retry "$CREATE_OWNER_CMD")
CREATE_OWNER_STATUS=${CREATE_OWNER_FULL: -3}
CREATE_OWNER=${CREATE_OWNER_FULL:0:${#CREATE_OWNER_FULL}-3}
validate_test "Création utilisateur propriétaire" "$CREATE_OWNER_STATUS" "$CREATE_OWNER" 201

# Extraction de l'ID propriétaire
OWNER_ID=$(extract_id "$CREATE_OWNER")
echo -e "\n${GREEN}ID propriétaire extrait:${NC} $OWNER_ID"

if [ -z "$OWNER_ID" ]; then
    echo -e "${RED}Échec d'extraction de l'ID propriétaire. Utilisation d'un ID par défaut...${NC}"
    OWNER_ID="00000000-0000-0000-0000-000000000001"
    echo -e "${YELLOW}ID propriétaire par défaut utilisé: $OWNER_ID${NC}"
fi

# 2. Connexion avec le propriétaire
echo -e "\n${YELLOW}2. Connexion avec le propriétaire${NC}"
OWNER_LOGIN_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/auth/login\" -H \"Content-Type: application/json\" -d '{\"email\": \"$OWNER_EMAIL\", \"password\": \"$OWNER_PASSWORD\"}'"
OWNER_LOGIN_FULL=$(debug_curl_with_retry "$OWNER_LOGIN_CMD")
OWNER_LOGIN_STATUS=${OWNER_LOGIN_FULL: -3}
OWNER_LOGIN=${OWNER_LOGIN_FULL:0:${#OWNER_LOGIN_FULL}-3}
validate_test "Connexion propriétaire" "$OWNER_LOGIN_STATUS" "$OWNER_LOGIN" 200

# Extraction du token JWT propriétaire
OWNER_TOKEN=$(extract_token_simple "$OWNER_LOGIN")
echo -e "\n${GREEN}Token JWT propriétaire extrait:${NC} $OWNER_TOKEN"

if [ -z "$OWNER_TOKEN" ]; then
    echo -e "${RED}Échec d'extraction du token propriétaire. Tentative de secours...${NC}"
    OWNER_TOKEN=$(echo "$OWNER_LOGIN" | grep -o 'eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*')
    if [ -n "$OWNER_TOKEN" ]; then
        echo -e "${GREEN}Token JWT propriétaire récupéré par méthode alternative:${NC} $OWNER_TOKEN"
    else
        echo -e "${RED}Échec critique de récupération du token propriétaire. Impossible de continuer.${NC}"
        exit 1
    fi
fi

# 3. Création d'un utilisateur client avec le token admin
echo -e "\n${YELLOW}3. Création d'un utilisateur client${NC}"
CREATE_CLIENT_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/users/\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $ADMIN_TOKEN\" -d '{\"email\": \"$CLIENT_EMAIL\", \"password\": \"$CLIENT_PASSWORD\", \"first_name\": \"Client\", \"last_name\": \"User\"}'"
CREATE_CLIENT_FULL=$(debug_curl_with_retry "$CREATE_CLIENT_CMD")
CREATE_CLIENT_STATUS=${CREATE_CLIENT_FULL: -3}
CREATE_CLIENT=${CREATE_CLIENT_FULL:0:${#CREATE_CLIENT_FULL}-3}
validate_test "Création utilisateur client" "$CREATE_CLIENT_STATUS" "$CREATE_CLIENT" 201

# Extraction de l'ID client
CLIENT_ID=$(extract_id "$CREATE_CLIENT")
echo -e "\n${GREEN}ID client extrait:${NC} $CLIENT_ID"

if [ -z "$CLIENT_ID" ]; then
    echo -e "${RED}Échec d'extraction de l'ID client. Utilisation d'un ID par défaut...${NC}"
    CLIENT_ID="00000000-0000-0000-0000-000000000002"
    echo -e "${YELLOW}ID client par défaut utilisé: $CLIENT_ID${NC}"
fi

# 4. Connexion avec le client
echo -e "\n${YELLOW}4. Connexion avec le client${NC}"
CLIENT_LOGIN_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/auth/login\" -H \"Content-Type: application/json\" -d '{\"email\": \"$CLIENT_EMAIL\", \"password\": \"$CLIENT_PASSWORD\"}'"
CLIENT_LOGIN_FULL=$(debug_curl_with_retry "$CLIENT_LOGIN_CMD")
CLIENT_LOGIN_STATUS=${CLIENT_LOGIN_FULL: -3}
CLIENT_LOGIN=${CLIENT_LOGIN_FULL:0:${#CLIENT_LOGIN_FULL}-3}
validate_test "Connexion client" "$CLIENT_LOGIN_STATUS" "$CLIENT_LOGIN" 200

# Extraction du token JWT client
CLIENT_TOKEN=$(extract_token_simple "$CLIENT_LOGIN")
echo -e "\n${GREEN}Token JWT client extrait:${NC} $CLIENT_TOKEN"

if [ -z "$CLIENT_TOKEN" ]; then
    echo -e "${RED}Échec d'extraction du token client. Tentative de secours...${NC}"
    CLIENT_TOKEN=$(echo "$CLIENT_LOGIN" | grep -o 'eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*')
    if [ -n "$CLIENT_TOKEN" ]; then
        echo -e "${GREEN}Token JWT client récupéré par méthode alternative:${NC} $CLIENT_TOKEN"
    else
        echo -e "${RED}Échec critique de récupération du token client. Impossible de continuer.${NC}"
        exit 1
    fi
fi

# 5. Connexion avec un administrateur
echo -e "\n${YELLOW}5. Connexion avec un administrateur${NC}"
ADMIN_LOGIN_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/auth/login\" -H \"Content-Type: application/json\" -d '{\"email\": \"admin@hbnb.io\", \"password\": \"admin1234\"}'"
ADMIN_LOGIN_FULL=$(debug_curl_with_retry "$ADMIN_LOGIN_CMD")
ADMIN_LOGIN_STATUS=${ADMIN_LOGIN_FULL: -3}
ADMIN_LOGIN=${ADMIN_LOGIN_FULL:0:${#ADMIN_LOGIN_FULL}-3}
validate_test "Connexion administrateur" "$ADMIN_LOGIN_STATUS" "$ADMIN_LOGIN" 200

# Extraction du token JWT admin
ADMIN_TOKEN=$(extract_token_simple "$ADMIN_LOGIN")
echo -e "\n${GREEN}Token JWT admin extrait:${NC} $ADMIN_TOKEN"

if [ -z "$ADMIN_TOKEN" ]; then
    echo -e "${RED}Échec d'extraction du token admin. Tentative de secours...${NC}"
    ADMIN_TOKEN=$(echo "$ADMIN_LOGIN" | grep -o 'eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*')
    if [ -n "$ADMIN_TOKEN" ]; then
        echo -e "${GREEN}Token JWT admin récupéré par méthode alternative:${NC} $ADMIN_TOKEN"
    else
        echo -e "${RED}Échec critique de récupération du token admin. Impossible de continuer.${NC}"
        exit 1
    fi
fi

# 6. Création d'une place par le propriétaire
echo -e "\n${YELLOW}6. Création d'une place par le propriétaire${NC}"
PLACE_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/places/\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $OWNER_TOKEN\" -d '{\"title\": \"$PLACE_NAME\", \"description\": \"Belle maison avec jardin\", \"price\": 150.0, \"latitude\": 43.6047, \"longitude\": 1.4442, \"owner_id\": \"$OWNER_ID\"}'"
PLACE_FULL=$(debug_curl_with_retry "$PLACE_CMD")
PLACE_STATUS=${PLACE_FULL: -3}
PLACE=${PLACE_FULL:0:${#PLACE_FULL}-3}
validate_test "Création place" "$PLACE_STATUS" "$PLACE" 201

# Extraction de l'ID place
PLACE_ID=$(extract_id "$PLACE")
echo -e "\n${GREEN}ID place extrait:${NC} $PLACE_ID"

if [ -z "$PLACE_ID" ]; then
    echo -e "${RED}Échec d'extraction de l'ID place. Utilisation d'un ID par défaut...${NC}"
    PLACE_ID="00000000-0000-0000-0000-000000000003"
    echo -e "${YELLOW}ID place par défaut utilisé: $PLACE_ID${NC}"
fi

# 7. Création d'une review par le client
echo -e "\n${YELLOW}7. Création d'une review par le client${NC}"
REVIEW_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/reviews/\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $CLIENT_TOKEN\" -d '{\"place_id\": \"$PLACE_ID\", \"user_id\": \"$CLIENT_ID\", \"rating\": 4, \"text\": \"Très bon séjour, propriétaire accueillant\"}'"
REVIEW_FULL=$(debug_curl_with_retry "$REVIEW_CMD")
REVIEW_STATUS=${REVIEW_FULL: -3}
REVIEW=${REVIEW_FULL:0:${#REVIEW_FULL}-3}
validate_test "Création review" "$REVIEW_STATUS" "$REVIEW" 201

# Extraction de l'ID review
REVIEW_ID=$(extract_id "$REVIEW")
echo -e "\n${GREEN}ID review extrait:${NC} $REVIEW_ID"

if [ -z "$REVIEW_ID" ]; then
    echo -e "${RED}Échec d'extraction de l'ID review. Utilisation d'un ID par défaut...${NC}"
    REVIEW_ID="00000000-0000-0000-0000-000000000004"
    echo -e "${YELLOW}ID review par défaut utilisé: $REVIEW_ID${NC}"
fi

# 8. Tentative de création d'une seconde review par le même client (doit échouer)
echo -e "\n${YELLOW}8. Tentative de création d'une seconde review par le même client${NC}"
SECOND_REVIEW_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/reviews/\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $CLIENT_TOKEN\" -d '{\"place_id\": \"$PLACE_ID\", \"user_id\": \"$CLIENT_ID\", \"rating\": 5, \"text\": \"Je tente de poster une seconde review\"}'"
SECOND_REVIEW_FULL=$(debug_curl_with_retry "$SECOND_REVIEW_CMD")
SECOND_REVIEW_STATUS=${SECOND_REVIEW_FULL: -3}
SECOND_REVIEW=${SECOND_REVIEW_FULL:0:${#SECOND_REVIEW_FULL}-3}
validate_test "Tentative de double review" "$SECOND_REVIEW_STATUS" "$SECOND_REVIEW" 400

# 9. Récupérer les reviews d'une place
echo -e "\n${YELLOW}9. Récupération des reviews d'une place${NC}"
PLACE_REVIEWS_CMD="curl -s -w \"%{http_code}\" -X GET \"$API_URL/places/$PLACE_ID/reviews\" -H \"Content-Type: application/json\""
PLACE_REVIEWS_FULL=$(debug_curl_with_retry "$PLACE_REVIEWS_CMD")
PLACE_REVIEWS_STATUS=${PLACE_REVIEWS_FULL: -3}
PLACE_REVIEWS=${PLACE_REVIEWS_FULL:0:${#PLACE_REVIEWS_FULL}-3}
validate_test "Récupération reviews d'une place" "$PLACE_REVIEWS_STATUS" "$PLACE_REVIEWS" 200

# 10. Récupérer une review spécifique
echo -e "\n${YELLOW}10. Récupération d'une review spécifique${NC}"
SPECIFIC_REVIEW_CMD="curl -s -w \"%{http_code}\" -X GET \"$API_URL/reviews/$REVIEW_ID\" -H \"Content-Type: application/json\""
SPECIFIC_REVIEW_FULL=$(debug_curl_with_retry "$SPECIFIC_REVIEW_CMD")
SPECIFIC_REVIEW_STATUS=${SPECIFIC_REVIEW_FULL: -3}
SPECIFIC_REVIEW=${SPECIFIC_REVIEW_FULL:0:${#SPECIFIC_REVIEW_FULL}-3}
validate_test "Récupération review spécifique" "$SPECIFIC_REVIEW_STATUS" "$SPECIFIC_REVIEW" 200

# 11. Tentative de modification d'une review par un autre utilisateur (doit échouer)
echo -e "\n${YELLOW}11. Tentative de modification d'une review par un autre utilisateur${NC}"
UNAUTH_MODIFY_CMD="curl -s -w \"%{http_code}\" -X PUT \"$API_URL/reviews/$REVIEW_ID\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $OWNER_TOKEN\" -d '{\"rating\": 1, \"text\": \"Je tente de falsifier cette review\"}'"
UNAUTH_MODIFY_FULL=$(debug_curl_with_retry "$UNAUTH_MODIFY_CMD")
UNAUTH_MODIFY_STATUS=${UNAUTH_MODIFY_FULL: -3}
UNAUTH_MODIFY=${UNAUTH_MODIFY_FULL:0:${#UNAUTH_MODIFY_FULL}-3}
validate_test "Modification par non-auteur" "$UNAUTH_MODIFY_STATUS" "$UNAUTH_MODIFY" 403

# 12. Modification d'une review par le client qui l'a créée
echo -e "\n${YELLOW}12. Modification d'une review par son auteur${NC}"
MODIFY_REVIEW_CMD="curl -s -w \"%{http_code}\" -X PUT \"$API_URL/reviews/$REVIEW_ID\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $CLIENT_TOKEN\" -d '{\"rating\": 5, \"text\": \"Finalement, c était super !\"}'"
MODIFY_REVIEW_FULL=$(debug_curl_with_retry "$MODIFY_REVIEW_CMD")
MODIFY_REVIEW_STATUS=${MODIFY_REVIEW_FULL: -3}
MODIFY_REVIEW=${MODIFY_REVIEW_FULL:0:${#MODIFY_REVIEW_FULL}-3}
validate_test "Modification review par auteur" "$MODIFY_REVIEW_STATUS" "$MODIFY_REVIEW" 200

# 13. Vérifier que la modification a bien été prise en compte
echo -e "\n${YELLOW}13. Vérification de la modification${NC}"
VERIFY_MODIFY_CMD="curl -s -w \"%{http_code}\" -X GET \"$API_URL/reviews/$REVIEW_ID\" -H \"Content-Type: application/json\""
VERIFY_MODIFY_FULL=$(debug_curl_with_retry "$VERIFY_MODIFY_CMD")
VERIFY_MODIFY_STATUS=${VERIFY_MODIFY_FULL: -3}
VERIFY_MODIFY=${VERIFY_MODIFY_FULL:0:${#VERIFY_MODIFY_FULL}-3}
validate_test "Vérification modification" "$VERIFY_MODIFY_STATUS" "$VERIFY_MODIFY" 200

# 14. Modification d'une review par un administrateur
echo -e "\n${YELLOW}14. Modification d'une review par un administrateur${NC}"
ADMIN_MODIFY_CMD="curl -s -w \"%{http_code}\" -X PUT \"$API_URL/reviews/$REVIEW_ID\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $ADMIN_TOKEN\" -d '{\"rating\": 3, \"text\": \"Review modérée par un administrateur\"}'"
ADMIN_MODIFY_FULL=$(debug_curl_with_retry "$ADMIN_MODIFY_CMD")
ADMIN_MODIFY_STATUS=${ADMIN_MODIFY_FULL: -3}
ADMIN_MODIFY=${ADMIN_MODIFY_FULL:0:${#ADMIN_MODIFY_FULL}-3}
validate_test "Modification review par admin" "$ADMIN_MODIFY_STATUS" "$ADMIN_MODIFY" 200

# 15. Suppression d'une review par un administrateur
echo -e "\n${YELLOW}15. Suppression d'une review par un administrateur${NC}"
ADMIN_DELETE_CMD="curl -s -w \"%{http_code}\" -X DELETE \"$API_URL/reviews/$REVIEW_ID\" -H \"Authorization: Bearer $ADMIN_TOKEN\""
ADMIN_DELETE_FULL=$(debug_curl_with_retry "$ADMIN_DELETE_CMD")
ADMIN_DELETE_STATUS=${ADMIN_DELETE_FULL: -3}
ADMIN_DELETE=${ADMIN_DELETE_FULL:0:${#ADMIN_DELETE_FULL}-3}
validate_test "Suppression review par admin" "$ADMIN_DELETE_STATUS" "$ADMIN_DELETE" 200

# 16. Vérifier que la review a bien été supprimée
echo -e "\n${YELLOW}16. Vérification de la suppression${NC}"
VERIFY_DELETE_CMD="curl -s -w \"%{http_code}\" -X GET \"$API_URL/reviews/$REVIEW_ID\" -H \"Content-Type: application/json\""
VERIFY_DELETE_FULL=$(debug_curl_with_retry "$VERIFY_DELETE_CMD")
VERIFY_DELETE_STATUS=${VERIFY_DELETE_FULL: -3}
VERIFY_DELETE=${VERIFY_DELETE_FULL:0:${#VERIFY_DELETE_FULL}-3}
validate_test "Vérification de la suppression" "$VERIFY_DELETE_STATUS" "$VERIFY_DELETE" 404

# 17. Création d'une nouvelle review pour tester la suppression par l'auteur
echo -e "\n${YELLOW}17. Création d'une nouvelle review par le client${NC}"
NEW_REVIEW_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/reviews/\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $CLIENT_TOKEN\" -d '{\"place_id\": \"$PLACE_ID\", \"user_id\": \"$CLIENT_ID\", \"rating\": 3, \"text\": \"Review pour tester la suppression\"}'"
NEW_REVIEW_FULL=$(debug_curl_with_retry "$NEW_REVIEW_CMD")
NEW_REVIEW_STATUS=${NEW_REVIEW_FULL: -3}
NEW_REVIEW=${NEW_REVIEW_FULL:0:${#NEW_REVIEW_FULL}-3}
validate_test "Création nouvelle review" "$NEW_REVIEW_STATUS" "$NEW_REVIEW" 201

# Extraction de l'ID de la nouvelle review
NEW_REVIEW_ID=$(extract_id "$NEW_REVIEW")
echo -e "\n${GREEN}ID nouvelle review extrait:${NC} $NEW_REVIEW_ID"

if [ -z "$NEW_REVIEW_ID" ]; then
    echo -e "${RED}Échec d'extraction de l'ID nouvelle review. Utilisation d'un ID par défaut...${NC}"
    NEW_REVIEW_ID="00000000-0000-0000-0000-000000000005"
    echo -e "${YELLOW}ID nouvelle review par défaut utilisé: $NEW_REVIEW_ID${NC}"
fi

# 18. Suppression d'une review par son auteur
echo -e "\n${YELLOW}18. Suppression d'une review par son auteur${NC}"
AUTHOR_DELETE_CMD="curl -s -w \"%{http_code}\" -X DELETE \"$API_URL/reviews/$NEW_REVIEW_ID\" -H \"Authorization: Bearer $CLIENT_TOKEN\""
AUTHOR_DELETE_FULL=$(debug_curl_with_retry "$AUTHOR_DELETE_CMD")
AUTHOR_DELETE_STATUS=${AUTHOR_DELETE_FULL: -3}
AUTHOR_DELETE=${AUTHOR_DELETE_FULL:0:${#AUTHOR_DELETE_FULL}-3}
validate_test "Suppression review par auteur" "$AUTHOR_DELETE_STATUS" "$AUTHOR_DELETE" 200

# 19. Vérifier que la review a bien été supprimée
echo -e "\n${YELLOW}19. Vérification de la suppression par auteur${NC}"
VERIFY_AUTHOR_DELETE_CMD="curl -s -w \"%{http_code}\" -X GET \"$API_URL/reviews/$NEW_REVIEW_ID\" -H \"Content-Type: application/json\""
VERIFY_AUTHOR_DELETE_FULL=$(debug_curl_with_retry "$VERIFY_AUTHOR_DELETE_CMD")
VERIFY_AUTHOR_DELETE_STATUS=${VERIFY_AUTHOR_DELETE_FULL: -3}
VERIFY_AUTHOR_DELETE=${VERIFY_AUTHOR_DELETE_FULL:0:${#VERIFY_AUTHOR_DELETE_FULL}-3}
validate_test "Vérification de la suppression par auteur" "$VERIFY_AUTHOR_DELETE_STATUS" "$VERIFY_AUTHOR_DELETE" 404

# 20. Tentative de création d'une review sans être connecté
echo -e "\n${YELLOW}20. Tentative de création d'une review sans être connecté${NC}"
UNAUTH_REVIEW_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/reviews/\" -H \"Content-Type: application/json\" -d '{\"place_id\": \"$PLACE_ID\", \"user_id\": \"$CLIENT_ID\", \"rating\": 2, \"text\": \"Tentative sans authentification\"}'"
UNAUTH_REVIEW_FULL=$(debug_curl_with_retry "$UNAUTH_REVIEW_CMD")
UNAUTH_REVIEW_STATUS=${UNAUTH_REVIEW_FULL: -3}
UNAUTH_REVIEW=${UNAUTH_REVIEW_FULL:0:${#UNAUTH_REVIEW_FULL}-3}
validate_test "Création review sans authentification" "$UNAUTH_REVIEW_STATUS" "$UNAUTH_REVIEW" 401

# 21. Tentative de création d'une review avec un rating invalide
echo -e "\n${YELLOW}21. Tentative de création d'une review avec un rating invalide${NC}"
INVALID_RATING_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/reviews/\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $CLIENT_TOKEN\" -d '{\"place_id\": \"$PLACE_ID\", \"user_id\": \"$CLIENT_ID\", \"rating\": 6, \"text\": \"Rating invalide\"}'"
INVALID_RATING_FULL=$(debug_curl_with_retry "$INVALID_RATING_CMD")
INVALID_RATING_STATUS=${INVALID_RATING_FULL: -3}
INVALID_RATING=${INVALID_RATING_FULL:0:${#INVALID_RATING_FULL}-3}
validate_test "Création review avec rating invalide" "$INVALID_RATING_STATUS" "$INVALID_RATING" 400

# 22. Tentative de création d'une review avec un texte vide
echo -e "\n${YELLOW}22. Tentative de création d'une review avec un texte vide${NC}"
EMPTY_TEXT_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/reviews/\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $CLIENT_TOKEN\" -d '{\"place_id\": \"$PLACE_ID\", \"user_id\": \"$CLIENT_ID\", \"rating\": 3, \"text\": \"\"}'"
EMPTY_TEXT_FULL=$(debug_curl_with_retry "$EMPTY_TEXT_CMD")
EMPTY_TEXT_STATUS=${EMPTY_TEXT_FULL: -3}
EMPTY_TEXT=${EMPTY_TEXT_FULL:0:${#EMPTY_TEXT_FULL}-3}
validate_test "Création review avec texte vide" "$EMPTY_TEXT_STATUS" "$EMPTY_TEXT" 400

# 23. Tentative de récupération d'une review inexistante
echo -e "\n${YELLOW}23. Tentative de récupération d'une review inexistante${NC}"
INVALID_ID="00000000-0000-0000-0000-000000000000"
INVALID_ID_CMD="curl -s -w \"%{http_code}\" -X GET \"$API_URL/reviews/$INVALID_ID\" -H \"Content-Type: application/json\""
INVALID_ID_FULL=$(debug_curl_with_retry "$INVALID_ID_CMD")
INVALID_ID_STATUS=${INVALID_ID_FULL: -3}
INVALID_ID=${INVALID_ID_FULL:0:${#INVALID_ID_FULL}-3}
validate_test "Récupération d'une review avec ID invalide" "$INVALID_ID_STATUS" "$INVALID_ID" 404

# 24. Création d'une nouvelle review par le propriétaire (devrait échouer car un propriétaire ne peut pas reviewer sa propre place)
echo -e "\n${YELLOW}24. Création d'une nouvelle review par le propriétaire${NC}"
OWNER_REVIEW_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/reviews/\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $OWNER_TOKEN\" -d '{\"place_id\": \"$PLACE_ID\", \"user_id\": \"$OWNER_ID\", \"rating\": 4, \"text\": \"Review par le propriétaire\"}'"
OWNER_REVIEW_FULL=$(debug_curl_with_retry "$OWNER_REVIEW_CMD")
OWNER_REVIEW_STATUS=${OWNER_REVIEW_FULL: -3}
OWNER_REVIEW=${OWNER_REVIEW_FULL:0:${#OWNER_REVIEW_FULL}-3}
validate_test "Création review par propriétaire" "$OWNER_REVIEW_STATUS" "$OWNER_REVIEW" 400

# 25. Récupération de toutes les reviews
echo -e "\n${YELLOW}25. Récupération de toutes les reviews${NC}"
ALL_REVIEWS_CMD="curl -s -w \"%{http_code}\" -X GET \"$API_URL/reviews/\" -H \"Content-Type: application/json\""
ALL_REVIEWS_FULL=$(debug_curl_with_retry "$ALL_REVIEWS_CMD")
ALL_REVIEWS_STATUS=${ALL_REVIEWS_FULL: -3}
ALL_REVIEWS=${ALL_REVIEWS_FULL:0:${#ALL_REVIEWS_FULL}-3}
validate_test "Récupération de toutes les reviews" "$ALL_REVIEWS_STATUS" "$ALL_REVIEWS" 200

# 26. Création d'une seconde place pour tester la récupération des reviews par place
echo -e "\n${YELLOW}26. Création d'une seconde place${NC}"
SECOND_PLACE_NAME="Appartement Test ${TIMESTAMP}"
SECOND_PLACE_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/places/\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $OWNER_TOKEN\" -d '{\"title\": \"$SECOND_PLACE_NAME\", \"description\": \"Petit appartement en centre-ville\", \"price\": 80.0, \"latitude\": 44.8378, \"longitude\": -0.5792, \"owner_id\": \"$OWNER_ID\"}'"
SECOND_PLACE_FULL=$(debug_curl_with_retry "$SECOND_PLACE_CMD")
SECOND_PLACE_STATUS=${SECOND_PLACE_FULL: -3}
SECOND_PLACE=${SECOND_PLACE_FULL:0:${#SECOND_PLACE_FULL}-3}
validate_test "Création seconde place" "$SECOND_PLACE_STATUS" "$SECOND_PLACE" 201

# Extraction de l'ID seconde place
SECOND_PLACE_ID=$(extract_id "$SECOND_PLACE")
echo -e "\n${GREEN}ID seconde place extrait:${NC} $SECOND_PLACE_ID"

if [ -z "$SECOND_PLACE_ID" ]; then
    SECOND_PLACE_ID="00000000-0000-0000-0000-000000000006"
    echo -e "${YELLOW}ID seconde place par défaut utilisé: $SECOND_PLACE_ID${NC}"
fi

# 27. Création d'une review pour la seconde place
echo -e "\n${YELLOW}27. Création d'une review pour la seconde place${NC}"
SECOND_REVIEW_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/reviews/\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $CLIENT_TOKEN\" -d '{\"place_id\": \"$SECOND_PLACE_ID\", \"user_id\": \"$CLIENT_ID\", \"rating\": 2, \"text\": \"Appartement correct mais bruyant\"}'"
SECOND_REVIEW_FULL=$(debug_curl_with_retry "$SECOND_REVIEW_CMD")
SECOND_REVIEW_STATUS=${SECOND_REVIEW_FULL: -3}
SECOND_REVIEW=${SECOND_REVIEW_FULL:0:${#SECOND_REVIEW_FULL}-3}
validate_test "Création review pour seconde place" "$SECOND_REVIEW_STATUS" "$SECOND_REVIEW" 201

# 28. Récupération des reviews de la seconde place
echo -e "\n${YELLOW}28. Récupération des reviews de la seconde place${NC}"
SECOND_PLACE_REVIEWS_CMD="curl -s -w \"%{http_code}\" -X GET \"$API_URL/places/$SECOND_PLACE_ID/reviews\" -H \"Content-Type: application/json\""
SECOND_PLACE_REVIEWS_FULL=$(debug_curl_with_retry "$SECOND_PLACE_REVIEWS_CMD")
SECOND_PLACE_REVIEWS_STATUS=${SECOND_PLACE_REVIEWS_FULL: -3}
SECOND_PLACE_REVIEWS=${SECOND_PLACE_REVIEWS_FULL:0:${#SECOND_PLACE_REVIEWS_FULL}-3}
validate_test "Récupération reviews de la seconde place" "$SECOND_PLACE_REVIEWS_STATUS" "$SECOND_PLACE_REVIEWS" 200

# 29. Vérification que le propriétaire ne peut pas reviewer sa propre place 
# (note: test 24 est suffisant pour vérifier cela, mais nous pourrions ajouter un test explicite ici)

# 30. Récupération des reviews d'une place inexistante
echo -e "\n${YELLOW}30. Récupération des reviews d'une place inexistante${NC}"
INVALID_PLACE_ID="00000000-0000-0000-0000-000000000999"
INVALID_PLACE_REVIEWS_CMD="curl -s -w \"%{http_code}\" -X GET \"$API_URL/places/$INVALID_PLACE_ID/reviews\" -H \"Content-Type: application/json\""
INVALID_PLACE_REVIEWS_FULL=$(debug_curl_with_retry "$INVALID_PLACE_REVIEWS_CMD")
INVALID_PLACE_REVIEWS_STATUS=${INVALID_PLACE_REVIEWS_FULL: -3}
INVALID_PLACE_REVIEWS=${INVALID_PLACE_REVIEWS_FULL:0:${#INVALID_PLACE_REVIEWS_FULL}-3}
validate_test "Récupération reviews d'une place inexistante" "$INVALID_PLACE_REVIEWS_STATUS" "$INVALID_PLACE_REVIEWS" 404

# 31. Tentative de modification d'une review avec un rating invalide
echo -e "\n${YELLOW}31. Tentative de modification d'une review avec un rating invalide${NC}"
# Extraire l'ID de la review créée pour la seconde place
SECOND_REVIEW_ID=$(extract_id "$SECOND_REVIEW")
echo -e "\n${GREEN}ID second review extrait:${NC} $SECOND_REVIEW_ID"

if [ -z "$SECOND_REVIEW_ID" ]; then
    SECOND_REVIEW_ID="00000000-0000-0000-0000-000000000007"
    echo -e "${YELLOW}ID seconde review par défaut utilisé: $SECOND_REVIEW_ID${NC}"
fi

INVALID_UPDATE_CMD="curl -s -w \"%{http_code}\" -X PUT \"$API_URL/reviews/$SECOND_REVIEW_ID\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $CLIENT_TOKEN\" -d '{\"rating\": 0, \"text\": \"Rating invalide update\"}'"
INVALID_UPDATE_FULL=$(debug_curl_with_retry "$INVALID_UPDATE_CMD")
INVALID_UPDATE_STATUS=${INVALID_UPDATE_FULL: -3}
INVALID_UPDATE=${INVALID_UPDATE_FULL:0:${#INVALID_UPDATE_FULL}-3}
validate_test "Modification review avec rating invalide" "$INVALID_UPDATE_STATUS" "$INVALID_UPDATE" 400

echo -e "\n${GREEN}Tests de l'API reviews terminés.${NC}"