Documentation des Tests de l'API HBnB

1. Introduction

Ce document décrit le processus de test de l'API HBnB, en mettant en avant les scénarios réussis ainsi que les cas limites traités correctement.
Tous les tests ont été automatisés à l'aide d'un script Bash (utilisant cURL et jq) pour interagir avec l'API et vérifier les réponses étape par étape.

Les tests couvrent les opérations CRUD (Create, Read, Update, Delete) pour les entités suivantes :

Users

Amenities

Places

Reviews

De plus, Swagger UI a été utilisé pour valider manuellement les endpoints et vérifier la documentation de l'API.

2. Objectifs des Tests

Les objectifs principaux de ces tests sont de garantir que :

L'API fonctionne correctement pour toutes les actions CRUD.

Les entrées utilisateur sont correctement validées.

Les erreurs (valeurs invalides, ID inexistants, etc.) sont correctement gérées.

Les relations entre entités (ex. : un lieu avec les bonnes commodités et avis) sont respectées.

L'API empêche les actions non autorisées.

La documentation Swagger est générée correctement et décrit fidèlement l'API.

3. Environnement de Test

Serveur API : Flask-RESTx

Outils de test :

cURL et jq pour les tests automatisés en Bash

Vérifications manuelles via Swagger UI

Tests unitaires avec unittest et pytest

Méthodes de test :

Script Bash automatisé

Exploration manuelle avec Swagger UI

Tests unitaires en Python

4. Utilisation de Swagger pour les Tests Manuels

Swagger UI a été utilisé pour tester visuellement l'API et interagir directement avec elle. Cet outil permet de :

Parcourir tous les endpoints disponibles via une interface web.

Envoyer des requêtes API depuis le navigateur.

Voir les schémas de données et formats attendus.

Vérifier les réponses et repérer d'éventuelles erreurs en temps réel.

Accès à Swagger

Lorsque l'API est en cours d'exécution, Swagger UI est accessible à l'adresse suivante :

http://127.0.0.1:5000/api/v1/

Vérifications effectuées avec Swagger

Endpoint

Vérifications effectuées

/users

Création, récupération, mise à jour et suppression d'utilisateurs.

/amenities

Ajout et récupération de commodités.

/places

Vérification des relations entre lieux et commodités.

/reviews

Validation des avis, calcul des notes moyennes, etc.

5. Exemples de Requêtes cURL pour Tester l'API

Création d'un Utilisateur Valide

curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "first_name": "John",
       "last_name": "Doe",
       "email": "john.doe@example.com"
     }'

Réponse attendue :

{
  "id": "uuid",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com"
}

Création d'un Utilisateur avec un Email Déjà Existant

curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "first_name": "Jane",
       "last_name": "Smith",
       "email": "john.doe@example.com"
     }'

Réponse attendue :

{
  "error": "Email already registered"
}

Récupération de Tous les Utilisateurs

curl -X GET "http://127.0.0.1:5000/api/v1/users/" \
     -H "accept: application/json"

Mise à Jour d'un Utilisateur

curl -X PUT "http://127.0.0.1:5000/api/v1/users/{user_id}" \
     -H "Content-Type: application/json" \
     -d '{
       "first_name": "John-Updated",
       "last_name": "Doe-Updated",
       "email": "john.updated@example.com"
     }'

6. Résumé des Résultats

Module testé

✅ Succès

❌ Échecs

Notes

Users (/users)

10/10

0

Toutes les opérations CRUD ont réussi.

Amenities (/amenities)

9/9

0

Bonne détection des erreurs (nom manquant, ID inexistant, etc.).

Places (/places)

9/9

0

Validation correcte des propriétaires invalides, prix négatifs, latitude incorrecte, etc.

Reviews (/reviews)

14/14

0

Bonne gestion des erreurs, mise à jour correcte des données, suppression validée.

Taux de succès global : 100 % (42 tests réussis sur 42).

7. Améliorations Futures

Bien que les tests confirment le bon fonctionnement de l'API, des optimisations sont envisageables :

Tests de Performance : Mesurer les temps de réponse en charge normale et élevée.

Tests de Charge / Stress : Évaluer la scalabilité de l'API sous forte concurrence.

Tests de Sécurité : Vérifier que les utilisateurs non autorisés ne puissent pas exécuter d'actions interdites.

Tests Automatisés de Swagger : Générer automatiquement des requêtes à partir de la documentation pour valider la conformité des endpoints.

greedo
🚀 Conclusion

L'API HBnB a démontré une excellente stabilité et fiabilité sur tous les endpoints testés. Grâce à une suite complète de tests cURL automatisés et à des vérifications manuelles via Swagger, le service est prêt pour le déploiement. Les prochaines améliorations pourront se concentrer sur la performance, la sécurité et l'automatisation afin de renforcer encore davantage la robustesse de l'API.

