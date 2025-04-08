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

# Mode interactif - 0 pour automatique, 1 pour interactif
INTERACTIVE_MODE=0

# Mode debug - affiche les commandes curl complètes (1=oui, 0=non)
DEBUG_MODE=0

# Générer des valeurs uniques pour éviter les erreurs de duplication
TIMESTAMP=$(date +%s)
USER_EMAIL="test_user_${TIMESTAMP}@example.com"
USER_PASSWORD="password123"
ADMIN2_EMAIL="admin2_${TIMESTAMP}@example.com"
ADMIN2_PASSWORD="admin456"

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
            echo -e "${YELLOW}⚠️ L'utilisateur existe déjà. Utilisez un autre email.${NC}"
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

# Une nouvelle fonction d'extraction très simple qui prend le token directement
extract_token_simple() {
    local json_response="$1"
    # Enregistrer la réponse dans un fichier temporaire
    echo "$json_response" > /tmp/token_response.json
    
    # Extraire avec une expression régulière très simple
    # Cette méthode est plus robuste car elle recherche simplement la partie 
    # entre "access_token" : "..." sans se préoccuper du formatage exact
    if grep -q "access_token" /tmp/token_response.json; then
        # Extraire la ligne contenant access_token
        local token_line=$(grep "access_token" /tmp/token_response.json)
        # Extraire juste le token de cette ligne
        local token=$(echo "$token_line" | sed -E 's/.*"access_token"[^"]*"([^"]+)".*/\1/')
        echo "$token"
    else
        echo ""
    fi
}

# Fonction pour extraire l'ID simple
extract_id_simple() {
    local json_response="$1"
    # Enregistrer la réponse dans un fichier temporaire
    echo "$json_response" > /tmp/id_response.json
    
    # Extraire avec une expression régulière très simple
    if grep -q "\"id\"" /tmp/id_response.json; then
        # Extraire la ligne contenant id
        local id_line=$(grep "\"id\"" /tmp/id_response.json)
        # Extraire juste l'ID de cette ligne
        local id=$(echo "$id_line" | sed -E 's/.*"id"[^"]*"([^"]+)".*/\1/')
        echo "$id"
    else
        echo ""
    fi
}

echo -e "${YELLOW}=== Test de l'API utilisateurs ===${NC}\n"

# 1. Connexion avec l'admin préexistant
echo -e "\n${YELLOW}1. Connexion avec l'admin préexistant${NC}"
ADMIN_LOGIN_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/auth/login\" -H \"Content-Type: application/json\" -d '{\"email\": \"admin@hbnb.io\", \"password\": \"admin1234\"}'"
ADMIN_LOGIN_RESPONSE=$(debug_curl "$ADMIN_LOGIN_CMD")
ADMIN_LOGIN_STATUS=${ADMIN_LOGIN_RESPONSE: -3}
ADMIN_LOGIN=${ADMIN_LOGIN_RESPONSE:0:${#ADMIN_LOGIN_RESPONSE}-3}
validate_test "Connexion admin" "$ADMIN_LOGIN_STATUS" "$ADMIN_LOGIN" 200

# Extraction du token de manière simplifiée
ADMIN_TOKEN=$(extract_token_simple "$ADMIN_LOGIN")
echo -e "\n${GREEN}Token JWT admin extrait:${NC} $ADMIN_TOKEN"

# Vérifier si le token est vide
if [ -z "$ADMIN_TOKEN" ]; then
    echo -e "\n${RED}Échec d'extraction du token admin. Tentative de secours...${NC}"
    
    # Solution de secours - extraire directement avec une méthode encore plus simple
    ADMIN_TOKEN=$(echo "$ADMIN_LOGIN" | grep -o 'eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*')
    
    if [ -n "$ADMIN_TOKEN" ]; then
        echo -e "${GREEN}Token JWT récupéré par méthode alternative:${NC} $ADMIN_TOKEN"
    else
        echo -e "${RED}Échec critique de récupération du token. Impossible de continuer.${NC}"
        exit 1
    fi
fi

# 2. Création d'un utilisateur normal avec le token admin
echo -e "\n${YELLOW}2. Création d'un utilisateur normal avec le token admin${NC}"
USER_RESPONSE_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/users/\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $ADMIN_TOKEN\" -d '{\"email\": \"$USER_EMAIL\", \"password\": \"$USER_PASSWORD\", \"first_name\": \"Test\", \"last_name\": \"User\"}'"
USER_RESPONSE_FULL=$(debug_curl "$USER_RESPONSE_CMD")
USER_RESPONSE_STATUS=${USER_RESPONSE_FULL: -3}
USER_RESPONSE=${USER_RESPONSE_FULL:0:${#USER_RESPONSE_FULL}-3}
validate_test "Création utilisateur normal" "$USER_RESPONSE_STATUS" "$USER_RESPONSE" 201

# Extraction de l'ID utilisateur avec la fonction simplifiée
USER_ID=$(extract_id_simple "$USER_RESPONSE")
echo -e "\n${GREEN}ID utilisateur extrait:${NC} $USER_ID"

if [ -z "$USER_ID" ]; then
    echo -e "\n${RED}Échec d'extraction de l'ID utilisateur. Tentative de secours...${NC}"
    
    # Solution de secours - extraire l'UUID directement 
    USER_ID=$(echo "$USER_RESPONSE" | grep -o '[0-9a-f]\{8\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{12\}')
    
    if [ -n "$USER_ID" ]; then
        echo -e "${GREEN}ID utilisateur récupéré par méthode alternative:${NC} $USER_ID"
    else
        echo -e "${RED}Impossible de récupérer l'ID utilisateur.${NC}"
        # Continuer quand même car les tests suivants pourraient fonctionner
    fi
fi

# 3. Connexion avec cet utilisateur normal
echo -e "\n${YELLOW}3. Connexion avec l'utilisateur normal${NC}"
USER_LOGIN_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/auth/login\" -H \"Content-Type: application/json\" -d '{\"email\": \"$USER_EMAIL\", \"password\": \"$USER_PASSWORD\"}'"
USER_LOGIN_FULL=$(debug_curl "$USER_LOGIN_CMD")
USER_LOGIN_STATUS=${USER_LOGIN_FULL: -3}
USER_LOGIN=${USER_LOGIN_FULL:0:${#USER_LOGIN_FULL}-3}
validate_test "Connexion utilisateur" "$USER_LOGIN_STATUS" "$USER_LOGIN" 200

# Extraction du token avec la nouvelle méthode fiable
USER_TOKEN=$(extract_token_simple "$USER_LOGIN")
if [ -z "$USER_TOKEN" ]; then
    USER_TOKEN=$(echo "$USER_LOGIN" | grep -o 'eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*')
fi
echo -e "\n${GREEN}Token JWT utilisateur extrait:${NC} $USER_TOKEN"

# 4. Création d'un deuxième utilisateur administrateur
echo -e "\n${YELLOW}4. Création d'un deuxième utilisateur administrateur${NC}"
ADMIN2_RESPONSE_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/users/\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $ADMIN_TOKEN\" -d '{\"email\": \"$ADMIN2_EMAIL\", \"password\": \"$ADMIN2_PASSWORD\", \"first_name\": \"Admin2\", \"last_name\": \"User\", \"is_admin\": true}'"
ADMIN2_RESPONSE_FULL=$(debug_curl "$ADMIN2_RESPONSE_CMD")
ADMIN2_RESPONSE_STATUS=${ADMIN2_RESPONSE_FULL: -3}
ADMIN2_RESPONSE=${ADMIN2_RESPONSE_FULL:0:${#ADMIN2_RESPONSE_FULL}-3}
validate_test "Création administrateur" "$ADMIN2_RESPONSE_STATUS" "$ADMIN2_RESPONSE" 201

# Extraction de l'ID avec la nouvelle méthode fiable
ADMIN2_ID=$(extract_id_simple "$ADMIN2_RESPONSE")
if [ -z "$ADMIN2_ID" ]; then
    ADMIN2_ID=$(echo "$ADMIN2_RESPONSE" | grep -o '[0-9a-f]\{8\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{12\}')
fi
echo -e "\n${GREEN}ID du deuxième admin extrait:${NC} $ADMIN2_ID"

# 5. Connexion avec le deuxième administrateur
echo -e "\n${YELLOW}5. Connexion avec le deuxième administrateur${NC}"
ADMIN2_LOGIN_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/auth/login\" -H \"Content-Type: application/json\" -d '{\"email\": \"$ADMIN2_EMAIL\", \"password\": \"$ADMIN2_PASSWORD\"}'"
ADMIN2_LOGIN_FULL=$(debug_curl "$ADMIN2_LOGIN_CMD")
ADMIN2_LOGIN_STATUS=${ADMIN2_LOGIN_FULL: -3}
ADMIN2_LOGIN=${ADMIN2_LOGIN_FULL:0:${#ADMIN2_LOGIN_FULL}-3}
validate_test "Connexion deuxième admin" "$ADMIN2_LOGIN_STATUS" "$ADMIN2_LOGIN" 200

# Extraction du token avec la nouvelle méthode fiable
ADMIN2_TOKEN=$(extract_token_simple "$ADMIN2_LOGIN")
if [ -z "$ADMIN2_TOKEN" ]; then
    ADMIN2_TOKEN=$(echo "$ADMIN2_LOGIN" | grep -o 'eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*')
fi
echo -e "\n${GREEN}Token JWT du deuxième admin extrait:${NC} $ADMIN2_TOKEN"

# 6. Tentative d'un utilisateur normal de créer un administrateur (doit échouer)
echo -e "\n${YELLOW}6. Tentative d'un utilisateur normal de créer un administrateur (doit échouer)${NC}"
FAILED_EMAIL="should_fail_${TIMESTAMP}@example.com"
FAILED_ADMIN_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/users/\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $USER_TOKEN\" -d '{\"email\": \"$FAILED_EMAIL\", \"password\": \"fail123\", \"first_name\": \"Should\", \"last_name\": \"Fail\", \"is_admin\": true}'"
FAILED_ADMIN_RESPONSE_FULL=$(debug_curl "$FAILED_ADMIN_CMD")
FAILED_ADMIN_RESPONSE_STATUS=${FAILED_ADMIN_RESPONSE_FULL: -3}
FAILED_ADMIN_RESPONSE=${FAILED_ADMIN_RESPONSE_FULL:0:${#FAILED_ADMIN_RESPONSE_FULL}-3}
validate_test "Tentative création admin par utilisateur normal" "$FAILED_ADMIN_RESPONSE_STATUS" "$FAILED_ADMIN_RESPONSE" 403

# 7. Récupérer tous les utilisateurs en tant qu'admin
echo -e "\n${YELLOW}7. Récupération de tous les utilisateurs (admin)${NC}"
ALL_USERS_CMD="curl -s -w \"%{http_code}\" -X GET \"$API_URL/users/\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $ADMIN_TOKEN\""
ALL_USERS_RESPONSE_FULL=$(debug_curl "$ALL_USERS_CMD")
ALL_USERS_RESPONSE_STATUS=${ALL_USERS_RESPONSE_FULL: -3}
ALL_USERS_RESPONSE=${ALL_USERS_RESPONSE_FULL:0:${#ALL_USERS_RESPONSE_FULL}-3}
validate_test "Liste tous utilisateurs (admin)" "$ALL_USERS_RESPONSE_STATUS" "$ALL_USERS_RESPONSE" 200

# 8. Récupération de tous les utilisateurs en tant qu'utilisateur normal (autorisé)
echo -e "\n${YELLOW}8. Récupération de tous les utilisateurs (utilisateur normal)${NC}"
USER_ALL_USERS_CMD="curl -s -w \"%{http_code}\" -X GET \"$API_URL/users/\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $USER_TOKEN\""
USER_ALL_USERS_FULL=$(debug_curl "$USER_ALL_USERS_CMD")
USER_ALL_USERS_STATUS=${USER_ALL_USERS_FULL: -3}
USER_ALL_USERS=${USER_ALL_USERS_FULL:0:${#USER_ALL_USERS_FULL}-3}
validate_test "Liste tous utilisateurs (utilisateur normal)" "$USER_ALL_USERS_STATUS" "$USER_ALL_USERS" 200

# 9. Récupérer un utilisateur spécifique en tant qu'admin
echo -e "\n${YELLOW}9. Récupération d'un utilisateur spécifique (admin)${NC}"
SPECIFIC_USER_CMD="curl -s -w \"%{http_code}\" -X GET \"$API_URL/users/$USER_ID\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $ADMIN_TOKEN\""
SPECIFIC_USER_FULL=$(debug_curl "$SPECIFIC_USER_CMD")
SPECIFIC_USER_STATUS=${SPECIFIC_USER_FULL: -3}
SPECIFIC_USER=${SPECIFIC_USER_FULL:0:${#SPECIFIC_USER_FULL}-3}
validate_test "Récupération utilisateur spécifique (admin)" "$SPECIFIC_USER_STATUS" "$SPECIFIC_USER" 200

# 10. Récupération d'un autre utilisateur en tant qu'utilisateur normal (autorisé)
echo -e "\n${YELLOW}10. Récupération d'un autre utilisateur (utilisateur normal)${NC}"
USER_SPECIFIC_USER_CMD="curl -s -w \"%{http_code}\" -X GET \"$API_URL/users/$ADMIN2_ID\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $USER_TOKEN\""
USER_SPECIFIC_USER_FULL=$(debug_curl "$USER_SPECIFIC_USER_CMD")
USER_SPECIFIC_USER_STATUS=${USER_SPECIFIC_USER_FULL: -3}
USER_SPECIFIC_USER=${USER_SPECIFIC_USER_FULL:0:${#USER_SPECIFIC_USER_FULL}-3}
validate_test "Récupération autre utilisateur (utilisateur normal)" "$USER_SPECIFIC_USER_STATUS" "$USER_SPECIFIC_USER" 200

# 11. Modifier un utilisateur en tant qu'admin
echo -e "\n${YELLOW}11. Modification d'un utilisateur (admin)${NC}"
MODIFIED_USER_CMD="curl -s -w \"%{http_code}\" -X PUT \"$API_URL/users/$USER_ID\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $ADMIN_TOKEN\" -d '{\"first_name\": \"Modified\", \"last_name\": \"ByAdmin\"}'"
MODIFIED_USER_FULL=$(debug_curl "$MODIFIED_USER_CMD")
MODIFIED_USER_STATUS=${MODIFIED_USER_FULL: -3}
MODIFIED_USER=${MODIFIED_USER_FULL:0:${#MODIFIED_USER_FULL}-3}
validate_test "Modification utilisateur par admin" "$MODIFIED_USER_STATUS" "$MODIFIED_USER" 200

# 12. Modification de son propre profil (non-admin)
echo -e "\n${YELLOW}12. Modification de son propre profil (non-admin)${NC}"
SELF_MODIFIED_CMD="curl -s -w \"%{http_code}\" -X PUT \"$API_URL/users/$USER_ID\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $USER_TOKEN\" -d '{\"first_name\": \"Self\", \"last_name\": \"Modified\"}'"
SELF_MODIFIED_FULL=$(debug_curl "$SELF_MODIFIED_CMD")
SELF_MODIFIED_STATUS=${SELF_MODIFIED_FULL: -3}
SELF_MODIFIED=${SELF_MODIFIED_FULL:0:${#SELF_MODIFIED_FULL}-3}
validate_test "Modification de son profil (utilisateur normal)" "$SELF_MODIFIED_STATUS" "$SELF_MODIFIED" 200

# 13. Récupérer l'utilisateur modifié pour vérifier les changements
echo -e "\n${YELLOW}13. Vérification des modifications de l'utilisateur${NC}"
VERIFY_MODIFIED_CMD="curl -s -w \"%{http_code}\" -X GET \"$API_URL/users/$USER_ID\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $ADMIN_TOKEN\""
VERIFY_MODIFIED_FULL=$(debug_curl "$VERIFY_MODIFIED_CMD")
VERIFY_MODIFIED_STATUS=${VERIFY_MODIFIED_FULL: -3}
VERIFY_MODIFIED=${VERIFY_MODIFIED_FULL:0:${#VERIFY_MODIFIED_FULL}-3}
validate_test "Vérification modifications" "$VERIFY_MODIFIED_STATUS" "$VERIFY_MODIFIED" 200

# 14. Tentative de modification d'un autre utilisateur par un non-admin (doit échouer)
echo -e "\n${YELLOW}14. Tentative de modification d'un autre utilisateur par un non-admin (doit échouer)${NC}"
FAILED_MODIFICATION_CMD="curl -s -w \"%{http_code}\" -X PUT \"$API_URL/users/$ADMIN2_ID\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $USER_TOKEN\" -d '{\"first_name\": \"Should\", \"last_name\": \"Fail\"}'"
FAILED_MODIFICATION_FULL=$(debug_curl "$FAILED_MODIFICATION_CMD")
FAILED_MODIFICATION_STATUS=${FAILED_MODIFICATION_FULL: -3}
FAILED_MODIFICATION=${FAILED_MODIFICATION_FULL:0:${#FAILED_MODIFICATION_FULL}-3}
validate_test "Tentative modification autre utilisateur par non-admin" "$FAILED_MODIFICATION_STATUS" "$FAILED_MODIFICATION" 403

# 15. Modification de l'email d'un utilisateur par un admin
echo -e "\n${YELLOW}15. Modification de l'email d'un utilisateur par un admin${NC}"
NEW_EMAIL="updated_email_${TIMESTAMP}@example.com"
ADMIN_MODIFY_EMAIL_CMD="curl -s -w \"%{http_code}\" -X PUT \"$API_URL/users/$USER_ID\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $ADMIN_TOKEN\" -d '{\"email\": \"$NEW_EMAIL\"}'"
ADMIN_MODIFY_EMAIL_FULL=$(debug_curl "$ADMIN_MODIFY_EMAIL_CMD")
ADMIN_MODIFY_EMAIL_STATUS=${ADMIN_MODIFY_EMAIL_FULL: -3}
ADMIN_MODIFY_EMAIL=${ADMIN_MODIFY_EMAIL_FULL:0:${#ADMIN_MODIFY_EMAIL_FULL}-3}
validate_test "Modification email par admin" "$ADMIN_MODIFY_EMAIL_STATUS" "$ADMIN_MODIFY_EMAIL" 200

# 16. Vérification de la modification d'email par admin
echo -e "\n${YELLOW}16. Vérification de la modification d'email par admin${NC}"
VERIFY_EMAIL_CMD="curl -s -w \"%{http_code}\" -X GET \"$API_URL/users/$USER_ID\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $ADMIN_TOKEN\""
VERIFY_EMAIL_FULL=$(debug_curl "$VERIFY_EMAIL_CMD")
VERIFY_EMAIL_STATUS=${VERIFY_EMAIL_FULL: -3}
VERIFY_EMAIL=${VERIFY_EMAIL_FULL:0:${#VERIFY_EMAIL_FULL}-3}
validate_test "Vérification email modifié" "$VERIFY_EMAIL_STATUS" "$VERIFY_EMAIL" 200
# Vérifier si l'email a bien été modifié
if [[ "$VERIFY_EMAIL" == *"$NEW_EMAIL"* ]]; then
    echo -e "${GREEN}✓ Email correctement modifié par l'admin${NC}"
else
    echo -e "${RED}✗ La modification d'email par l'admin n'a pas été appliquée${NC}"
fi

# 17. Tentative d'un utilisateur normal de modifier son propre email (devrait échouer)
echo -e "\n${YELLOW}17. Tentative d'un utilisateur normal de modifier son propre email${NC}"
USER_NEW_EMAIL="user_attempt_${TIMESTAMP}@example.com"
USER_MODIFY_EMAIL_CMD="curl -s -w \"%{http_code}\" -X PUT \"$API_URL/users/$USER_ID\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $USER_TOKEN\" -d '{\"email\": \"$USER_NEW_EMAIL\"}'"
USER_MODIFY_EMAIL_FULL=$(debug_curl "$USER_MODIFY_EMAIL_CMD")
USER_MODIFY_EMAIL_STATUS=${USER_MODIFY_EMAIL_FULL: -3}
USER_MODIFY_EMAIL=${USER_MODIFY_EMAIL_FULL:0:${#USER_MODIFY_EMAIL_FULL}-3}
validate_test "Tentative modification email par utilisateur" "$USER_MODIFY_EMAIL_STATUS" "$USER_MODIFY_EMAIL" 400

# 18. Modification du mot de passe d'un utilisateur par admin
echo -e "\n${YELLOW}18. Modification du mot de passe d'un utilisateur par admin${NC}"
NEW_PASSWORD="newpassword123"
ADMIN_MODIFY_PASSWORD_CMD="curl -s -w \"%{http_code}\" -X PUT \"$API_URL/users/$USER_ID\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $ADMIN_TOKEN\" -d '{\"password\": \"$NEW_PASSWORD\"}'"
ADMIN_MODIFY_PASSWORD_FULL=$(debug_curl "$ADMIN_MODIFY_PASSWORD_CMD")
ADMIN_MODIFY_PASSWORD_STATUS=${ADMIN_MODIFY_PASSWORD_FULL: -3}
ADMIN_MODIFY_PASSWORD=${ADMIN_MODIFY_PASSWORD_FULL:0:${#ADMIN_MODIFY_PASSWORD_FULL}-3}
validate_test "Modification mot de passe par admin" "$ADMIN_MODIFY_PASSWORD_STATUS" "$ADMIN_MODIFY_PASSWORD" 200

# 19. Vérification du nouveau mot de passe en essayant de se connecter
echo -e "\n${YELLOW}19. Vérification du nouveau mot de passe${NC}"
LOGIN_NEW_PASSWORD_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/auth/login\" -H \"Content-Type: application/json\" -d '{\"email\": \"$NEW_EMAIL\", \"password\": \"$NEW_PASSWORD\"}'"
LOGIN_NEW_PASSWORD_FULL=$(debug_curl "$LOGIN_NEW_PASSWORD_CMD")
LOGIN_NEW_PASSWORD_STATUS=${LOGIN_NEW_PASSWORD_FULL: -3}
LOGIN_NEW_PASSWORD=${LOGIN_NEW_PASSWORD_FULL:0:${#LOGIN_NEW_PASSWORD_FULL}-3}
validate_test "Connexion avec nouveau mot de passe" "$LOGIN_NEW_PASSWORD_STATUS" "$LOGIN_NEW_PASSWORD" 200

# Extraction du nouveau token
NEW_USER_TOKEN=$(extract_token_simple "$LOGIN_NEW_PASSWORD")
if [ -z "$NEW_USER_TOKEN" ]; then
    NEW_USER_TOKEN=$(echo "$LOGIN_NEW_PASSWORD" | grep -o 'eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*')
fi
echo -e "\n${GREEN}Nouveau token JWT utilisateur extrait:${NC} $NEW_USER_TOKEN"

# 20. Tentative d'un utilisateur normal de modifier son propre mot de passe (devrait échouer)
echo -e "\n${YELLOW}20. Tentative d'un utilisateur normal de modifier son propre mot de passe${NC}"
USER_NEW_PASSWORD="userpassword456"
USER_MODIFY_PASSWORD_CMD="curl -s -w \"%{http_code}\" -X PUT \"$API_URL/users/$USER_ID\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $NEW_USER_TOKEN\" -d '{\"password\": \"$USER_NEW_PASSWORD\"}'"
USER_MODIFY_PASSWORD_FULL=$(debug_curl "$USER_MODIFY_PASSWORD_CMD")
USER_MODIFY_PASSWORD_STATUS=${USER_MODIFY_PASSWORD_FULL: -3}
USER_MODIFY_PASSWORD=${USER_MODIFY_PASSWORD_FULL:0:${#USER_MODIFY_PASSWORD_FULL}-3}
validate_test "Tentative modification mot de passe par utilisateur" "$USER_MODIFY_PASSWORD_STATUS" "$USER_MODIFY_PASSWORD" 400

# 21. Tentative de modification simultanée email et mot de passe par admin
echo -e "\n${YELLOW}21. Modification simultanée email et mot de passe par admin${NC}"
FINAL_EMAIL="final_email_${TIMESTAMP}@example.com"
FINAL_PASSWORD="finalpassword789"
ADMIN_FULL_MODIFY_CMD="curl -s -w \"%{http_code}\" -X PUT \"$API_URL/users/$USER_ID\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $ADMIN_TOKEN\" -d '{\"email\": \"$FINAL_EMAIL\", \"password\": \"$FINAL_PASSWORD\", \"first_name\": \"Final\", \"last_name\": \"Version\"}'"
ADMIN_FULL_MODIFY_FULL=$(debug_curl "$ADMIN_FULL_MODIFY_CMD")
ADMIN_FULL_MODIFY_STATUS=${ADMIN_FULL_MODIFY_FULL: -3}
ADMIN_FULL_MODIFY=${ADMIN_FULL_MODIFY_FULL:0:${#ADMIN_FULL_MODIFY_FULL}-3}
validate_test "Modification complète par admin" "$ADMIN_FULL_MODIFY_STATUS" "$ADMIN_FULL_MODIFY" 200

# 22. Vérification finale en se connectant avec les nouvelles informations
echo -e "\n${YELLOW}22. Vérification finale avec nouvelles informations${NC}"
FINAL_LOGIN_CMD="curl -s -w \"%{http_code}\" -X POST \"$API_URL/auth/login\" -H \"Content-Type: application/json\" -d '{\"email\": \"$FINAL_EMAIL\", \"password\": \"$FINAL_PASSWORD\"}'"
FINAL_LOGIN_FULL=$(debug_curl "$FINAL_LOGIN_CMD")
FINAL_LOGIN_STATUS=${FINAL_LOGIN_FULL: -3}
FINAL_LOGIN=${FINAL_LOGIN_FULL:0:${#FINAL_LOGIN_FULL}-3}
validate_test "Connexion finale avec nouvelles informations" "$FINAL_LOGIN_STATUS" "$FINAL_LOGIN" 200

# 23. Tentative de modification de ses propres informations non-sensibles (nom, prénom) par l'utilisateur
echo -e "\n${YELLOW}23. Modification d'informations non-sensibles par l'utilisateur${NC}"
FINAL_TOKEN=$(extract_token_simple "$FINAL_LOGIN")
if [ -z "$FINAL_TOKEN" ]; then
    FINAL_TOKEN=$(echo "$FINAL_LOGIN" | grep -o 'eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*')
fi
USER_NONSENSITIVE_CMD="curl -s -w \"%{http_code}\" -X PUT \"$API_URL/users/$USER_ID\" -H \"Content-Type: application/json\" -H \"Authorization: Bearer $FINAL_TOKEN\" -d '{\"first_name\": \"Changed\", \"last_name\": \"ByUser\"}'"
USER_NONSENSITIVE_FULL=$(debug_curl "$USER_NONSENSITIVE_CMD")
USER_NONSENSITIVE_STATUS=${USER_NONSENSITIVE_FULL: -3}
USER_NONSENSITIVE=${USER_NONSENSITIVE_FULL:0:${#USER_NONSENSITIVE_FULL}-3}
validate_test "Modification informations non-sensibles par utilisateur" "$USER_NONSENSITIVE_STATUS" "$USER_NONSENSITIVE" 200

echo -e "\n${GREEN}Tests de modifications de mots de passe et emails terminés.${NC}"