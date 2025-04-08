#!/bin/bash

# Couleurs pour une meilleure lisibilité
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Lancement des tests curl pour l'API HBnB ===${NC}\n"

# Emplacement des scripts de test
SCRIPT_DIR="$(dirname "$0")"
TEST_DIR="${SCRIPT_DIR}/../tests_part3"

# Rendre les scripts exécutables
chmod +x $TEST_DIR/*.sh

# Exécuter les tests dans l'ordre
echo -e "${GREEN}Exécution des tests d'authentification${NC}"
$TEST_DIR/test_auth.sh

echo -e "\n${GREEN}Exécution des tests d'utilisateurs${NC}"
$TEST_DIR/test_users.sh

echo -e "\n${GREEN}Exécution des tests d'amenities${NC}"
$TEST_DIR/test_amenities.sh

echo -e "\n${GREEN}Exécution des tests de places${NC}"
$TEST_DIR/test_places.sh

echo -e "\n${GREEN}Exécution des tests de reviews${NC}"
$TEST_DIR/test_reviews.sh

echo -e "\n${YELLOW}=== Fin des tests curl ===${NC}"