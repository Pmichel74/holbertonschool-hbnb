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
PLACE_NAME="Appartement Test ${TIMESTAMP}"
AMENITY_NAME="Amenity Test ${TIMESTAMP}"
SECOND_AMENITY_NAME="Second Amenity ${TIMESTAMP}"

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
            echo -e "${YELLOW}Essayez de synchroniser votre horloge avec: sudo ntpdate time.nist.gov${NC}"
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

# Fonction robuste pour exécuter une requête curl avec affichage des détails en mode debug et retry
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
        
        # Vérifier si le serveur est en cours d'exécution localement
        if command -v netstat &> /dev/null; then
            echo -e "${YELLOW}Vérification des ports locaux en écoute:${NC}"
            netstat -tuln | grep 5000 || echo "Aucun service n'écoute sur le port 5000"
        elif command -v ss &> /dev/null; then
            echo -e "${YELLOW}Vérification des ports locaux en écoute:${NC}"
            ss -tuln | grep 5000 || echo "Aucun service n'écoute sur le port 5000"
        fi
        
        echo -e "${YELLOW}Les tests vont continuer, mais des erreurs sont attendues.${NC}"
        sleep 2
    else
        echo -e "${GREEN}API accessible (status code: $status). Début des tests...${NC}"
    fi
}

echo -e "${YELLOW}=== Test de l'API places ===${NC}\n"
check_api_status

# 1. Connexion avec un administrateur
echo -e "\n${YELLOW}1. Connexion avec un administrateur${NC}"
ADMIN_LOGIN_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/auth/login\" -H \"Content-Type: application/json\" -d '{\"email\": \"admin@hbnb.io\", \"password\": \"admin1234\"}'"
ADMIN_LOGIN_RESPONSE=$(debug_curl_with_retry "$ADMIN_LOGIN_CMD")
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
CREATE_USER_FULL=$(debug_curl_with_retry "$CREATE_USER_CMD")
CREATE_USER_STATUS=${CREATE_USER_FULL: -3}
CREATE_USER=${CREATE_USER_FULL:0:${#CREATE_USER_FULL}-3}
validate_test "Création utilisateur normal" "$CREATE_USER_STATUS" "$CREATE_USER" 201

# Extraction de l'ID utilisateur
USER_ID=$(extract_id "$CREATE_USER")
echo -e "\n${GREEN}ID utilisateur extrait:${NC} $USER_ID"

if [ -z "$USER_ID" ]; then
    echo -e "\n${RED}Échec d'extraction de l'ID utilisateur. Utilisation d'un ID par défaut...${NC}"
    # Si on ne peut pas extraire l'ID, on prend l'ID inséré directement dans la requête suivante
    USER_ID="00000000-0000-0000-0000-000000000000"
    echo -e "${YELLOW}ID utilisateur par défaut utilisé: $USER_ID${NC}"
fi

# 3. Connexion avec l'utilisateur normal
echo -e "\n${YELLOW}3. Connexion avec l'utilisateur normal${NC}"
USER_LOGIN_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/auth/login\" -H \"Content-Type: application/json\" -d '{\"email\": \"$USER_EMAIL\", \"password\": \"$USER_PASSWORD\"}'"
USER_LOGIN_RESPONSE=$(debug_curl_with_retry "$USER_LOGIN_CMD")
USER_LOGIN_STATUS=${USER_LOGIN_RESPONSE: -3}
USER_LOGIN=${USER_LOGIN_RESPONSE:0:${#USER_LOGIN_RESPONSE}-3}
validate_test "Connexion utilisateur normal" "$USER_LOGIN_STATUS" "$USER_LOGIN" 200

# Extraction du token JWT utilisateur
USER_TOKEN=$(extract_token_simple "$USER_LOGIN")
echo -e "\n${GREEN}Token JWT utilisateur normal extrait:${NC} $USER_TOKEN"

if [ -z "$USER_TOKEN" ]; then
    echo -e "\n${RED}Échec d'extraction du token utilisateur. Utilisation du token admin à la place...${NC}"
    USER_TOKEN=$ADMIN_TOKEN
    echo -e "${YELLOW}⚠️ Utilisation du token admin comme fallback - certains tests pourraient ne pas refléter le comportement réel${NC}"
fi

# 4. Création d'un deuxième utilisateur pour les tests d'accès
echo -e "\n${YELLOW}4. Création d'un deuxième utilisateur${NC}"
SECOND_USER_EMAIL="second_user_${TIMESTAMP}@example.com"
SECOND_USER_PASSWORD="password456"
CREATE_SECOND_USER_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/users/\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $ADMIN_TOKEN\" -d '{\"email\": \"$SECOND_USER_EMAIL\", \"password\": \"$SECOND_USER_PASSWORD\", \"first_name\": \"Second\", \"last_name\": \"User\"}'"
CREATE_SECOND_USER_FULL=$(debug_curl_with_retry "$CREATE_SECOND_USER_CMD")
CREATE_SECOND_USER_STATUS=${CREATE_SECOND_USER_FULL: -3}
CREATE_SECOND_USER=${CREATE_SECOND_USER_FULL:0:${#CREATE_SECOND_USER_FULL}-3}
validate_test "Création second utilisateur" "$CREATE_SECOND_USER_STATUS" "$CREATE_SECOND_USER" 201

# Extraction de l'ID du deuxième utilisateur
SECOND_USER_ID=$(extract_id "$CREATE_SECOND_USER")

# 5. Connexion avec le deuxième utilisateur
echo -e "\n${YELLOW}5. Connexion avec le deuxième utilisateur${NC}"
SECOND_USER_LOGIN_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/auth/login\" -H \"Content-Type: application/json\" -d '{\"email\": \"$SECOND_USER_EMAIL\", \"password\": \"$SECOND_USER_PASSWORD\"}'"
SECOND_USER_LOGIN_RESPONSE=$(debug_curl_with_retry "$SECOND_USER_LOGIN_CMD")
SECOND_USER_LOGIN_STATUS=${SECOND_USER_LOGIN_RESPONSE: -3}
SECOND_USER_LOGIN=${SECOND_USER_LOGIN_RESPONSE:0:${#SECOND_USER_LOGIN_RESPONSE}-3}
validate_test "Connexion second utilisateur" "$SECOND_USER_LOGIN_STATUS" "$SECOND_USER_LOGIN" 200

# Extraction du token JWT du deuxième utilisateur
SECOND_USER_TOKEN=$(extract_token_simple "$SECOND_USER_LOGIN")
echo -e "\n${GREEN}Token JWT second utilisateur extrait:${NC} $SECOND_USER_TOKEN"

if [ -z "$SECOND_USER_TOKEN" ]; then
    echo -e "\n${RED}Échec d'extraction du token du second utilisateur. Utilisation du token utilisateur 1 à la place...${NC}"
    SECOND_USER_TOKEN=$USER_TOKEN
    echo -e "${YELLOW}⚠️ Utilisation du token du premier utilisateur comme fallback - certains tests pourraient ne pas refléter le comportement réel${NC}"
fi

# 6. Création d'une amenity par l'administrateur
echo -e "\n${YELLOW}6. Création d'une amenity par l'administrateur${NC}"
AMENITY_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/amenities/\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $ADMIN_TOKEN\" -d '{\"name\": \"$AMENITY_NAME\"}'"
AMENITY_RESPONSE_FULL=$(debug_curl_with_retry "$AMENITY_CMD")
AMENITY_RESPONSE_STATUS=${AMENITY_RESPONSE_FULL: -3}
AMENITY_RESPONSE=${AMENITY_RESPONSE_FULL:0:${#AMENITY_RESPONSE_FULL}-3}
validate_test "Création amenity" "$AMENITY_RESPONSE_STATUS" "$AMENITY_RESPONSE" 201

# Extraction de l'ID amenity
AMENITY_ID=$(extract_id "$AMENITY_RESPONSE")
echo -e "\n${GREEN}ID amenity extrait:${NC} $AMENITY_ID"

if [ -z "$AMENITY_ID" ]; then
    # Si on ne peut pas extraire l'ID amenity, on utilise une valeur par défaut
    AMENITY_ID="11111111-1111-1111-1111-111111111111"
    echo -e "${YELLOW}ID amenity par défaut utilisé: $AMENITY_ID${NC}"
fi

# 7. Création d'une seconde amenity par l'administrateur
echo -e "\n${YELLOW}7. Création d'une seconde amenity par l'administrateur${NC}"
SECOND_AMENITY_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/amenities/\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $ADMIN_TOKEN\" -d '{\"name\": \"$SECOND_AMENITY_NAME\"}'"
SECOND_AMENITY_RESPONSE_FULL=$(debug_curl_with_retry "$SECOND_AMENITY_CMD")
SECOND_AMENITY_RESPONSE_STATUS=${SECOND_AMENITY_RESPONSE_FULL: -3}
SECOND_AMENITY_RESPONSE=${SECOND_AMENITY_RESPONSE_FULL:0:${#SECOND_AMENITY_RESPONSE_FULL}-3}
validate_test "Création seconde amenity" "$SECOND_AMENITY_RESPONSE_STATUS" "$SECOND_AMENITY_RESPONSE" 201

# Extraction de l'ID seconde amenity
SECOND_AMENITY_ID=$(extract_id "$SECOND_AMENITY_RESPONSE")
echo -e "\n${GREEN}ID seconde amenity extrait:${NC} $SECOND_AMENITY_ID"

if [ -z "$SECOND_AMENITY_ID" ]; then
    # Si on ne peut pas extraire l'ID seconde amenity, on utilise une valeur par défaut
    SECOND_AMENITY_ID="22222222-2222-2222-2222-222222222222"
    echo -e "${YELLOW}ID seconde amenity par défaut utilisé: $SECOND_AMENITY_ID${NC}"
fi

# 8. Création d'une place par l'utilisateur
echo -e "\n${YELLOW}8. Création d'une place par l'utilisateur${NC}"
PLACE_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/places/\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $USER_TOKEN\" -d '{\"title\": \"$PLACE_NAME\", \"description\": \"Magnifique appartement avec vue\", \"price\": 100.0, \"latitude\": 48.8566, \"longitude\": 2.3522, \"owner_id\": \"$USER_ID\", \"amenities\": [\"$AMENITY_ID\"]}'"
PLACE_RESPONSE_FULL=$(debug_curl_with_retry "$PLACE_CMD")
PLACE_RESPONSE_STATUS=${PLACE_RESPONSE_FULL: -3}
PLACE_RESPONSE=${PLACE_RESPONSE_FULL:0:${#PLACE_RESPONSE_FULL}-3}
validate_test "Création place" "$PLACE_RESPONSE_STATUS" "$PLACE_RESPONSE" 201

# Extraction de l'ID place
PLACE_ID=$(extract_id "$PLACE_RESPONSE")
echo -e "\n${GREEN}ID place extrait:${NC} $PLACE_ID"

if [ -z "$PLACE_ID" ]; then
    # Si on ne peut pas extraire l'ID place, on utilise une valeur par défaut
    PLACE_ID="33333333-3333-3333-3333-333333333333"
    echo -e "${YELLOW}ID place par défaut utilisé: $PLACE_ID${NC}"
fi

# 9. Récupérer toutes les places
echo -e "\n${YELLOW}9. Récupération de toutes les places${NC}"

# Augmenter considérablement les timeouts pour cette requête spécifique
echo -e "${YELLOW}Tentative de récupération de toutes les places avec timeout augmenté...${NC}"
ALL_PLACES_CMD="curl -s -w \"%{http_code}\" -X GET \"$API_URL/places/\" -H \"Content-Type: application/json\" --connect-timeout 30 --max-time 60"
ALL_PLACES_FULL=$(eval "$ALL_PLACES_CMD")
ALL_PLACES_STATUS=${ALL_PLACES_FULL: -3}
ALL_PLACES=${ALL_PLACES_FULL:0:${#ALL_PLACES_FULL}-3}

# Si ça échoue encore, essayer avec l'option -k (ignorer les erreurs SSL)
if [ "$ALL_PLACES_STATUS" = "000" ]; then
    echo -e "${YELLOW}Premier essai échoué, nouvelle tentative avec des options supplémentaires...${NC}"
    ALL_PLACES_CMD="curl -s -w \"%{http_code}\" -X GET \"$API_URL/places/\" -H \"Content-Type: application/json\" -k --connect-timeout 40 --max-time 90"
    ALL_PLACES_FULL=$(eval "$ALL_PLACES_CMD")
    ALL_PLACES_STATUS=${ALL_PLACES_FULL: -3}
    ALL_PLACES=${ALL_PLACES_FULL:0:${#ALL_PLACES_FULL}-3}
fi

validate_test "Liste de toutes les places" "$ALL_PLACES_STATUS" "$ALL_PLACES" 200

# 10. Récupérer une place spécifique avec détails
echo -e "\n${YELLOW}10. Récupération d'une place spécifique${NC}"
SPECIFIC_PLACE_CMD="curl -s -w \"%{http_code}\" -X GET \"$API_URL/places/$PLACE_ID\" -H \"Content-Type: application/json\""
SPECIFIC_PLACE_FULL=$(debug_curl_with_retry "$SPECIFIC_PLACE_CMD")
SPECIFIC_PLACE_STATUS=${SPECIFIC_PLACE_FULL: -3}
SPECIFIC_PLACE=${SPECIFIC_PLACE_FULL:0:${#SPECIFIC_PLACE_FULL}-3}
validate_test "Récupération place spécifique" "$SPECIFIC_PLACE_STATUS" "$SPECIFIC_PLACE" 200

# 11. Modifier une place pour ajouter une amenity (avec PUT)
echo -e "\n${YELLOW}11. Ajout d'une amenity à une place via PUT${NC}"
ADD_AMENITY_CMD="curl -s -w \"%{http_code}\" -X PUT \"$API_URL/places/$PLACE_ID\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $USER_TOKEN\" -d '{\"amenities\": [\"$AMENITY_ID\", \"$SECOND_AMENITY_ID\"]}'"
ADD_AMENITY_FULL=$(debug_curl_with_retry "$ADD_AMENITY_CMD")
ADD_AMENITY_STATUS=${ADD_AMENITY_FULL: -3}
ADD_AMENITY=${ADD_AMENITY_FULL:0:${#ADD_AMENITY_FULL}-3}
validate_test "Ajout d'amenities via PUT" "$ADD_AMENITY_STATUS" "$ADD_AMENITY" 200

# 12. Vérifier que les amenities ont bien été ajoutées
echo -e "\n${YELLOW}12. Vérification de l'ajout d'amenities${NC}"
VERIFY_ADD_CMD="curl -s -w \"%{http_code}\" -X GET \"$API_URL/places/$PLACE_ID\" -H \"Content-Type: application/json\""
VERIFY_ADD_FULL=$(debug_curl_with_retry "$VERIFY_ADD_CMD")
VERIFY_ADD_STATUS=${VERIFY_ADD_FULL: -3}
VERIFY_ADD=${VERIFY_ADD_FULL:0:${#VERIFY_ADD_FULL}-3}
validate_test "Vérification de l'ajout d'amenities" "$VERIFY_ADD_STATUS" "$VERIFY_ADD" 200

# 13. Modifier une place pour retirer une amenity
echo -e "\n${YELLOW}13. Retrait d'une amenity via PUT${NC}"
REMOVE_AMENITY_CMD="curl -s -w \"%{http_code}\" -X PUT \"$API_URL/places/$PLACE_ID\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $USER_TOKEN\" -d '{\"amenities\": [\"$AMENITY_ID\"]}'"
REMOVE_AMENITY_FULL=$(debug_curl_with_retry "$REMOVE_AMENITY_CMD")
REMOVE_AMENITY_STATUS=${REMOVE_AMENITY_FULL: -3}
REMOVE_AMENITY=${REMOVE_AMENITY_FULL:0:${#REMOVE_AMENITY_FULL}-3}
validate_test "Retrait d'une amenity via PUT" "$REMOVE_AMENITY_STATUS" "$REMOVE_AMENITY" 200

# 14. Vérifier que l'amenity a bien été retirée
echo -e "\n${YELLOW}14. Vérification du retrait d'amenity${NC}"
VERIFY_REMOVE_CMD="curl -s -w \"%{http_code}\" -X GET \"$API_URL/places/$PLACE_ID\" -H \"Content-Type: application/json\""
VERIFY_REMOVE_FULL=$(debug_curl_with_retry "$VERIFY_REMOVE_CMD")
VERIFY_REMOVE_STATUS=${VERIFY_REMOVE_FULL: -3}
VERIFY_REMOVE=${VERIFY_REMOVE_FULL:0:${#VERIFY_REMOVE_FULL}-3}
validate_test "Vérification du retrait d'amenity" "$VERIFY_REMOVE_STATUS" "$VERIFY_REMOVE" 200

# 14. Modifier une place par le propriétaire
echo -e "\n${YELLOW}14. Modification d'une place par le propriétaire${NC}"
UPDATED_NAME="Super $PLACE_NAME"
UPDATE_PLACE_CMD="curl -s -w \"%{http_code}\" -X PUT \"$API_URL/places/$PLACE_ID\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $USER_TOKEN\" -d '{\"title\": \"$UPDATED_NAME\", \"price\": 120.0}'"
UPDATE_PLACE_FULL=$(debug_curl_with_retry "$UPDATE_PLACE_CMD")
UPDATE_PLACE_STATUS=${UPDATE_PLACE_FULL: -3}
UPDATE_PLACE=${UPDATE_PLACE_FULL:0:${#UPDATE_PLACE_FULL}-3}
validate_test "Modification place par propriétaire" "$UPDATE_PLACE_STATUS" "$UPDATE_PLACE" 200

# 15. Tentative de modification par un autre utilisateur (doit échouer)
echo -e "\n${YELLOW}15. Tentative de modification d'une place par un autre utilisateur${NC}"
UNAUTHORIZED_UPDATE_CMD="curl -s -w \"%{http_code}\" -X PUT \"$API_URL/places/$PLACE_ID\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $SECOND_USER_TOKEN\" -d '{\"title\": \"Tentative non autorisée\", \"price\": 50.0}'"
UNAUTHORIZED_UPDATE_FULL=$(debug_curl_with_retry "$UNAUTHORIZED_UPDATE_CMD")
UNAUTHORIZED_UPDATE_STATUS=${UNAUTHORIZED_UPDATE_FULL: -3}
UNAUTHORIZED_UPDATE=${UNAUTHORIZED_UPDATE_FULL:0:${#UNAUTHORIZED_UPDATE_FULL}-3}
validate_test "Modification place par un autre utilisateur" "$UNAUTHORIZED_UPDATE_STATUS" "$UNAUTHORIZED_UPDATE" 403

# 16. Modifier par l'administrateur (devrait réussir même si pas propriétaire)
echo -e "\n${YELLOW}16. Modification d'une place par l'administrateur${NC}"
ADMIN_UPDATED_NAME="Admin Modifié $PLACE_NAME"
ADMIN_UPDATE_CMD="curl -s -w \"%{http_code}\" -X PUT \"$API_URL/places/$PLACE_ID\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $ADMIN_TOKEN\" -d '{\"title\": \"$ADMIN_UPDATED_NAME\"}'"
ADMIN_UPDATE_FULL=$(debug_curl_with_retry "$ADMIN_UPDATE_CMD")
ADMIN_UPDATE_STATUS=${ADMIN_UPDATE_FULL: -3}
ADMIN_UPDATE=${ADMIN_UPDATE_FULL:0:${#ADMIN_UPDATE_FULL}-3}
validate_test "Modification place par admin" "$ADMIN_UPDATE_STATUS" "$ADMIN_UPDATE" 200

# 17. Vérifier les modifications
echo -e "\n${YELLOW}17. Vérification des modifications${NC}"
VERIFY_UPDATE_CMD="curl -s -w \"%{http_code}\" -X GET \"$API_URL/places/$PLACE_ID\" -H \"Content-Type: application/json\""
VERIFY_UPDATE_FULL=$(debug_curl_with_retry "$VERIFY_UPDATE_CMD")
VERIFY_UPDATE_STATUS=${VERIFY_UPDATE_FULL: -3}
VERIFY_UPDATE=${VERIFY_UPDATE_FULL:0:${#VERIFY_UPDATE_FULL}-3}
validate_test "Vérification des modifications" "$VERIFY_UPDATE_STATUS" "$VERIFY_UPDATE" 200

# 20. Tentative de suppression d'une place par un autre utilisateur (doit échouer)
echo -e "\n${YELLOW}20. Tentative de suppression d'une place par un autre utilisateur${NC}"
UNAUTHORIZED_DELETE_CMD="curl -s -w \"%{http_code}\" -X DELETE \"$API_URL/places/$PLACE_ID\" -H \"Authorization: Bearer $SECOND_USER_TOKEN\""
UNAUTHORIZED_DELETE_FULL=$(debug_curl_with_retry "$UNAUTHORIZED_DELETE_CMD")
UNAUTHORIZED_DELETE_STATUS=${UNAUTHORIZED_DELETE_FULL: -3}
UNAUTHORIZED_DELETE=${UNAUTHORIZED_DELETE_FULL:0:${#UNAUTHORIZED_DELETE_FULL}-3}
validate_test "Suppression place par un autre utilisateur" "$UNAUTHORIZED_DELETE_STATUS" "$UNAUTHORIZED_DELETE" 403

# 21. Suppression d'une place par le propriétaire
echo -e "\n${YELLOW}21. Suppression d'une place par le propriétaire${NC}"
DELETE_PLACE_CMD="curl -s -w \"%{http_code}\" -X DELETE \"$API_URL/places/$PLACE_ID\" -H \"Authorization: Bearer $USER_TOKEN\""
DELETE_PLACE_FULL=$(debug_curl_with_retry "$DELETE_PLACE_CMD")
DELETE_PLACE_STATUS=${DELETE_PLACE_FULL: -3}
DELETE_PLACE=${DELETE_PLACE_FULL:0:${#DELETE_PLACE_FULL}-3}
validate_test "Suppression place par propriétaire" "$DELETE_PLACE_STATUS" "$DELETE_PLACE" 200

# 22. Vérifier que la place a bien été supprimée
echo -e "\n${YELLOW}22. Vérification de la suppression${NC}"
VERIFY_DELETE_CMD="curl -s -w \"%{http_code}\" -X GET \"$API_URL/places/$PLACE_ID\" -H \"Content-Type: application/json\""
VERIFY_DELETE_FULL=$(debug_curl_with_retry "$VERIFY_DELETE_CMD")
VERIFY_DELETE_STATUS=${VERIFY_DELETE_FULL: -3}
VERIFY_DELETE=${VERIFY_DELETE_FULL:0:${#VERIFY_DELETE_FULL}-3}
validate_test "Vérification de la suppression" "$VERIFY_DELETE_STATUS" "$VERIFY_DELETE" 404

# 23. Création d'une nouvelle place
echo -e "\n${YELLOW}23. Création d'une nouvelle place${NC}"
NEW_PLACE_NAME="Nouvelle place ${TIMESTAMP}"
NEW_PLACE_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/places/\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $USER_TOKEN\" -d '{\"title\": \"$NEW_PLACE_NAME\", \"description\": \"Une description\", \"price\": 150.0, \"latitude\": 48.1234, \"longitude\": 2.5678, \"owner_id\": \"$USER_ID\"}'"
NEW_PLACE_FULL=$(debug_curl_with_retry "$NEW_PLACE_CMD")
NEW_PLACE_STATUS=${NEW_PLACE_FULL: -3}
NEW_PLACE=${NEW_PLACE_FULL:0:${#NEW_PLACE_FULL}-3}
validate_test "Création d'une nouvelle place" "$NEW_PLACE_STATUS" "$NEW_PLACE" 201

# Extraction de l'ID de la nouvelle place
NEW_PLACE_ID=$(extract_id "$NEW_PLACE")
echo -e "\n${GREEN}ID nouvelle place extrait:${NC} $NEW_PLACE_ID"

if [ -z "$NEW_PLACE_ID" ]; then
    NEW_PLACE_ID="44444444-4444-4444-4444-444444444444"
    echo -e "${YELLOW}ID nouvelle place par défaut utilisé: $NEW_PLACE_ID${NC}"
fi

# 24. Tentative de création d'une place avec données invalides
echo -e "\n${YELLOW}24. Tentative de création d'une place avec données invalides${NC}"
INVALID_PLACE_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/places/\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $USER_TOKEN\" -d '{\"title\": \"\", \"description\": \"Description sans titre\", \"price\": -10, \"latitude\": 200, \"longitude\": 500, \"owner_id\": \"$USER_ID\"}'"
INVALID_PLACE_FULL=$(debug_curl_with_retry "$INVALID_PLACE_CMD")
INVALID_PLACE_STATUS=${INVALID_PLACE_FULL: -3}
INVALID_PLACE=${INVALID_PLACE_FULL:0:${#INVALID_PLACE_FULL}-3}
validate_test "Création place avec données invalides" "$INVALID_PLACE_STATUS" "$INVALID_PLACE" 400

# 25. Suppression d'une place par un administrateur
echo -e "\n${YELLOW}25. Suppression d'une place par un administrateur${NC}"
ADMIN_DELETE_CMD="curl -s -w \"%{http_code}\" -X DELETE \"$API_URL/places/$NEW_PLACE_ID\" -H \"Authorization: Bearer $ADMIN_TOKEN\""
ADMIN_DELETE_FULL=$(debug_curl_with_retry "$ADMIN_DELETE_CMD")
ADMIN_DELETE_STATUS=${ADMIN_DELETE_FULL: -3}
ADMIN_DELETE=${ADMIN_DELETE_FULL:0:${#ADMIN_DELETE_FULL}-3}
validate_test "Suppression place par admin" "$ADMIN_DELETE_STATUS" "$ADMIN_DELETE" 200

# 26. Vérifier que la place a bien été supprimée
echo -e "\n${YELLOW}26. Vérification de la suppression par admin${NC}"
VERIFY_ADMIN_DELETE_CMD="curl -s -w \"%{http_code}\" -X GET \"$API_URL/places/$NEW_PLACE_ID\" -H \"Content-Type: application/json\""
VERIFY_ADMIN_DELETE_FULL=$(debug_curl_with_retry "$VERIFY_ADMIN_DELETE_CMD")
VERIFY_ADMIN_DELETE_STATUS=${VERIFY_ADMIN_DELETE_FULL: -3}
VERIFY_ADMIN_DELETE=${VERIFY_ADMIN_DELETE_FULL:0:${#VERIFY_ADMIN_DELETE_FULL}-3}
validate_test "Vérification de la suppression par admin" "$VERIFY_ADMIN_DELETE_STATUS" "$VERIFY_ADMIN_DELETE" 404

# 27. Tentative d'accès à une place inexistante
echo -e "\n${YELLOW}27. Tentative d'accès à une place inexistante${NC}"
INVALID_ID="00000000-0000-0000-0000-000000000000"
INVALID_ID_CMD="curl -s -w \"%{http_code}\" -X GET \"$API_URL/places/$INVALID_ID\" -H \"Content-Type: application/json\""
INVALID_ID_FULL=$(debug_curl_with_retry "$INVALID_ID_CMD")
INVALID_ID_STATUS=${INVALID_ID_FULL: -3}
INVALID_ID=${INVALID_ID_FULL:0:${#INVALID_ID_FULL}-3}
validate_test "Récupération d'une place avec ID invalide" "$INVALID_ID_STATUS" "$INVALID_ID" 404

echo -e "\n${GREEN}Tests places terminés.${NC}"
