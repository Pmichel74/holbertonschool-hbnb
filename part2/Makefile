# Définition des variables
PYTHON = python3
PYTEST = pytest
COVERAGE = coverage
PIP = pip
FLASK = flask
APP_NAME = app

# Couleurs pour les messages
CYAN = \033[96m
GREEN = \033[92m
RED = \033[91m
RESET = \033[0m

.PHONY: help install test test-verbose coverage clean run lint format db-init db-migrate db-upgrade

# Affiche l'aide avec toutes les commandes disponibles
help:
	@echo "$(CYAN)Commandes disponibles :$(RESET)"
	@echo "$(GREEN)make install$(RESET)      - Installe les dépendances"
	@echo "$(GREEN)make test$(RESET)         - Lance les tests unitaires"
	@echo "$(GREEN)make test-verbose$(RESET) - Lance les tests avec plus de détails"
	@echo "$(GREEN)make coverage$(RESET)     - Lance les tests avec rapport de couverture"
	@echo "$(GREEN)make clean$(RESET)        - Nettoie les fichiers temporaires"
	@echo "$(GREEN)make run$(RESET)          - Lance l'application en mode développement"
	@echo "$(GREEN)make lint$(RESET)         - Vérifie le style du code"
	@echo "$(GREEN)make format$(RESET)       - Formate le code automatiquement"
	@echo "$(GREEN)make db-init$(RESET)      - Initialise la base de données"
	@echo "$(GREEN)make db-migrate$(RESET)   - Crée une nouvelle migration"
	@echo "$(GREEN)make db-upgrade$(RESET)   - Applique les migrations"

# Installation des dépendances
install:
	@echo "$(CYAN)Installation des dépendances...$(RESET)"
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)Installation terminée !$(RESET)"

# Tests simples
test:
	@echo "$(CYAN)Lancement des tests...$(RESET)"
	$(PYTHON) -m unittest discover tests
	@echo "$(GREEN)Tests terminés !$(RESET)"

# Tests détaillés
test-verbose:
	@echo "$(CYAN)Lancement des tests détaillés...$(RESET)"
	$(PYTHON) -m unittest discover tests -v
	@echo "$(GREEN)Tests terminés !$(RESET)"

# Tests avec couverture
coverage:
	@echo "$(CYAN)Lancement des tests avec couverture...$(RESET)"
	$(COVERAGE) run -m unittest discover tests
	$(COVERAGE) report
	$(COVERAGE) html
	@echo "$(GREEN)Rapport de couverture généré dans htmlcov/index.html$(RESET)"

# Nettoyage des fichiers temporaires
clean:
	@echo "$(CYAN)Nettoyage des fichiers temporaires...$(RESET)"
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	@echo "$(GREEN)Nettoyage terminé !$(RESET)"

# Lancement de l'application
run:
	@echo "$(CYAN)Lancement de l'application...$(RESET)"
	$(FLASK) run --debug

# Vérification du style de code avec flake8
lint:
	@echo "$(CYAN)Vérification du style de code...$(RESET)"
	flake8 $(APP_NAME) tests
	@echo "$(GREEN)Vérification terminée !$(RESET)"

# Formatage automatique du code avec black
format:
	@echo "$(CYAN)Formatage du code...$(RESET)"
	black $(APP_NAME) tests
	@echo "$(GREEN)Formatage terminé !$(RESET)"

# Commandes pour la base de données
db-init:
	@echo "$(CYAN)Initialisation de la base de données...$(RESET)"
	$(FLASK) db init
	@echo "$(GREEN)Initialisation terminée !$(RESET)"

db-migrate:
	@echo "$(CYAN)Création d'une nouvelle migration...$(RESET)"
	$(FLASK) db migrate -m "$(msg)"
	@echo "$(GREEN)Migration créée !$(RESET)"

db-upgrade:
	@echo "$(CYAN)Application des migrations...$(RESET)"
	$(FLASK) db upgrade
	@echo "$(GREEN)Migrations appliquées !$(RESET)"

# Test d'une seule classe de test
test-class:
	@if [ -z "$(class)" ]; then \
		echo "$(RED)Erreur: Spécifiez la classe de test avec class=NomDeLaClasse$(RESET)"; \
		exit 1; \
	fi
	@echo "$(CYAN)Lancement des tests pour la classe $(class)...$(RESET)"
	$(PYTHON) -m unittest tests.$(class) -v
	@echo "$(GREEN)Tests terminés !$(RESET)"

# Test d'un seul fichier de test
test-file:
	@if [ -z "$(file)" ]; then \
		echo "$(RED)Erreur: Spécifiez le fichier de test avec file=nom_du_fichier$(RESET)"; \
		exit 1; \
	fi
	@echo "$(CYAN)Lancement des tests pour le fichier $(file)...$(RESET)"
	$(PYTHON) -m unittest tests/$(file) -v
	@echo "$(GREEN)Tests terminés !$(RESET)"
