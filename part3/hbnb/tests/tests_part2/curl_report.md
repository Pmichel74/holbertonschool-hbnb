┌────────────────────────────────────────────┐
│         TESTS DES API UTILISATEURS         │
└────────────────────────────────────────────┘

Test 1: Création d'un utilisateur valide
Réponse: {
    "id": "1f90c245-7a2e-4cfc-8731-221aa2a60e4c",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "is_admin": false,
    "created_at": "2025-03-02T02:47:05.535168",
    "updated_at": "2025-03-02T02:47:05.535171"
}
ID extrait: 1f90c245-7a2e-4cfc-8731-221aa2a60e4c
✓ Création d'utilisateur réussie. ID: 1f90c245-7a2e-4cfc-8731-221aa2a60e4c

Test 2: Création d'un utilisateur avec email déjà existant
Réponse: {
    "error": "Email already registered"
}
✓ Détection correcte d'email dupliqué

Test 3: Création d'un utilisateur avec données invalides
Réponse: {
    "errors": {
        "first_name": "'first_name' is a required property"
    },
    "message": "Input payload validation failed"
}
✓ Détection correcte de données invalides

Test 4: Récupération de tous les utilisateurs
Réponse: [
    {
        "id": "fea62d6c-101a-4c67-8340-94cf0aeace68",
        "first_name": "strkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkking",
        "last_name": "string",
        "email": "string@sdf.sldkhf",
        "created_at": "2025-03-02T02:45:03.273531",
        "updated_at": "2025-03-02T02:45:03.273536"
    },
    {
        "id": "1f90c245-7a2e-4cfc-8731-221aa2a60e4c",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "created_at": "2025-03-02T02:47:05.535168",
        "updated_at": "2025-03-02T02:47:05.535171"
    }
]
✓ Récupération de la liste d'utilisateurs réussie

Test 5: Récupération d'un utilisateur par ID
Tentative de récupération pour l'ID: 1f90c245-7a2e-4cfc-8731-221aa2a60e4c
Réponse: {
    "id": "1f90c245-7a2e-4cfc-8731-221aa2a60e4c",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "is_admin": false,
    "created_at": "2025-03-02T02:47:05.535168",
    "updated_at": "2025-03-02T02:47:05.535171"
}
✓ Récupération de l'utilisateur réussie

Test 6: Récupération d'un utilisateur avec ID inexistant
Réponse: {
    "error": "User not found"
}
✓ Gestion correcte d'ID inexistant

Test 7: Mise à jour d'un utilisateur
Tentative de mise à jour pour l'ID: 1f90c245-7a2e-4cfc-8731-221aa2a60e4c
Réponse: {
    "id": "1f90c245-7a2e-4cfc-8731-221aa2a60e4c",
    "first_name": "John-Updated",
    "last_name": "Doe-Updated",
    "email": "john.updated@example.com",
    "is_admin": false,
    "created_at": "2025-03-02T02:47:05.535168",
    "updated_at": "2025-03-02T02:47:05.599425"
}
✓ Mise à jour de l'utilisateur réussie

Test 8: Mise à jour d'un utilisateur avec ID inexistant
Réponse: {
    "error": "User not found"
}
✓ Gestion correcte de mise à jour avec ID inexistant

Test 9: Création d'un deuxième utilisateur
Réponse: {
    "id": "b0814e42-d719-4472-88b3-13f86a8fe58f",
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane.smith@example.com",
    "is_admin": false,
    "created_at": "2025-03-02T02:47:05.620040",
    "updated_at": "2025-03-02T02:47:05.620043"
}
ID extrait: b0814e42-d719-4472-88b3-13f86a8fe58f
✓ Création du deuxième utilisateur réussie. ID: b0814e42-d719-4472-88b3-13f86a8fe58f

Test 10: Vérification de la liste avec deux utilisateurs
Réponse: [
    {
        "id": "fea62d6c-101a-4c67-8340-94cf0aeace68",
        "first_name": "strkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkking",
        "last_name": "string",
        "email": "string@sdf.sldkhf",
        "created_at": "2025-03-02T02:45:03.273531",
        "updated_at": "2025-03-02T02:45:03.273536"
    },
    {
        "id": "1f90c245-7a2e-4cfc-8731-221aa2a60e4c",
        "first_name": "John-Updated",
        "last_name": "Doe-Updated",
        "email": "john.updated@example.com",
        "created_at": "2025-03-02T02:47:05.535168",
        "updated_at": "2025-03-02T02:47:05.599425"
    },
    {
        "id": "b0814e42-d719-4472-88b3-13f86a8fe58f",
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "created_at": "2025-03-02T02:47:05.620040",
        "updated_at": "2025-03-02T02:47:05.620043"
    }
]
✓ Liste contient les deux utilisateurs

┌────────────────────────────────────────────┐
│          TESTS DES API AMENITIES           │
└────────────────────────────────────────────┘

Test 1: Création d'une amenity valide
Réponse: {
    "id": "5f452871-7de5-4080-88b7-e4196ae644ac",
    "name": "Wi-Fi",
    "created_at": "2025-03-02T02:47:05.649138",
    "updated_at": "2025-03-02T02:47:05.649142"
}
ID extrait: 5f452871-7de5-4080-88b7-e4196ae644ac
✓ Création d'amenity réussie. ID: 5f452871-7de5-4080-88b7-e4196ae644ac

Test 2: Création d'une amenity avec données invalides
Réponse: {
    "errors": {
        "name": "'name' is a required property"
    },
    "message": "Input payload validation failed"
}
✓ Détection correcte de données invalides

Test 3: Récupération de toutes les amenities
Réponse: [
    {
        "id": "5f452871-7de5-4080-88b7-e4196ae644ac",
        "name": "Wi-Fi",
        "created_at": "2025-03-02T02:47:05.649138",
        "updated_at": "2025-03-02T02:47:05.649142"
    }
]
✓ Récupération de la liste d'amenities réussie

Test 4: Récupération d'une amenity par ID
Tentative de récupération pour l'ID: 5f452871-7de5-4080-88b7-e4196ae644ac
Réponse: {
    "id": "5f452871-7de5-4080-88b7-e4196ae644ac",
    "name": "Wi-Fi",
    "created_at": "2025-03-02T02:47:05.649138",
    "updated_at": "2025-03-02T02:47:05.649142"
}
✓ Récupération de l'amenity réussie

Test 5: Récupération d'une amenity avec ID inexistant
Réponse: {
    "error": "Amenity not found"
}
✓ Gestion correcte d'ID inexistant

Test 6: Mise à jour d'une amenity
Tentative de mise à jour pour l'ID: 5f452871-7de5-4080-88b7-e4196ae644ac
Réponse: {
    "id": "5f452871-7de5-4080-88b7-e4196ae644ac",
    "name": "Air Conditioning",
    "created_at": "2025-03-02T02:47:05.649138",
    "updated_at": "2025-03-02T02:47:05.698803"
}
✓ Mise à jour de l'amenity réussie

Test 7: Mise à jour d'une amenity avec ID inexistant
Réponse: {
    "error": "Amenity not found"
}
✓ Gestion correcte de mise à jour avec ID inexistant

Test 8: Création d'une deuxième amenity
Réponse: {
    "id": "4a075d3c-bce2-4f68-8186-473ad00f45b4",
    "name": "Swimming Pool",
    "created_at": "2025-03-02T02:47:05.717006",
    "updated_at": "2025-03-02T02:47:05.717007"
}
ID extrait: 4a075d3c-bce2-4f68-8186-473ad00f45b4
✓ Création de la deuxième amenity réussie. ID: 4a075d3c-bce2-4f68-8186-473ad00f45b4

Test 9: Vérification de la liste avec deux amenities
Réponse: [
    {
        "id": "5f452871-7de5-4080-88b7-e4196ae644ac",
        "name": "Air Conditioning",
        "created_at": "2025-03-02T02:47:05.649138",
        "updated_at": "2025-03-02T02:47:05.698803"
    },
    {
        "id": "4a075d3c-bce2-4f68-8186-473ad00f45b4",
        "name": "Swimming Pool",
        "created_at": "2025-03-02T02:47:05.717006",
        "updated_at": "2025-03-02T02:47:05.717007"
    }
]
✓ Liste contient les deux amenities

┌────────────────────────────────────────────┐
│             TESTS DES API PLACES           │
└────────────────────────────────────────────┘

Test préliminaire: Création d'un utilisateur pour les tests
ID utilisateur extrait: bf6fe115-4025-48f4-9580-c474e20009cf
Test préliminaire: Création d'amenities pour les tests
ID amenity 1 extrait: 647cc858-b560-433e-81e1-d8230b4b72dd
ID amenity 2 extrait: d85b4620-989b-4b96-bc88-14be3f22a93b
Test 1: Création d'un place valide
Réponse: {
    "id": "5ee10e3d-c89f-407c-a3c7-ff99b3b7c178",
    "title": "Cozy Apartment",
    "description": "A nice place to stay",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "bf6fe115-4025-48f4-9580-c474e20009cf",
    "amenities": [
        "647cc858-b560-433e-81e1-d8230b4b72dd",
        "d85b4620-989b-4b96-bc88-14be3f22a93b"
    ]
}
ID place extrait: 5ee10e3d-c89f-407c-a3c7-ff99b3b7c178
✓ Création de place réussie. ID: 5ee10e3d-c89f-407c-a3c7-ff99b3b7c178

Test 2: Création d'un place avec propriétaire invalide
Réponse: {
    "error": "Owner with ID invalid_owner_id does not exist"
}
✓ Détection correcte de propriétaire invalide

Test 3: Création d'un place avec prix négatif
Réponse: {
    "error": "Price cannot be negative"
}
✓ Détection correcte de prix négatif

Test 4: Création d'un place avec latitude invalide
Réponse: {
    "error": "Latitude must be between -90 and 90"
}
✓ Détection correcte de latitude invalide

Test 5: Récupération de tous les places
Réponse: [
    {
        "id": "5ee10e3d-c89f-407c-a3c7-ff99b3b7c178",
        "title": "Cozy Apartment",
        "latitude": 37.7749,
        "longitude": -122.4194
    }
]
✓ Récupération de la liste de places réussie

Test 6: Récupération d'un place par ID
Tentative de récupération pour l'ID: 5ee10e3d-c89f-407c-a3c7-ff99b3b7c178
Réponse: {
    "id": "5ee10e3d-c89f-407c-a3c7-ff99b3b7c178",
    "title": "Cozy Apartment",
    "description": "A nice place to stay",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner": {
        "id": "bf6fe115-4025-48f4-9580-c474e20009cf",
        "first_name": "Place",
        "last_name": "Owner",
        "email": "place.owner1740880025@example.com"
    },
    "amenities": [
        {
            "id": "647cc858-b560-433e-81e1-d8230b4b72dd",
            "name": "Wi-Fi"
        },
        {
            "id": "d85b4620-989b-4b96-bc88-14be3f22a93b",
            "name": "Swimming Pool"
        }
    ],
    "reviews": [],
    "created_at": "2025-03-02T02:47:05.782083",
    "updated_at": "2025-03-02T02:47:05.782087"
}
✓ Récupération du place avec détails complets réussie

Test 7: Récupération d'un place avec ID inexistant
Réponse: {
    "error": "Place not found"
}
✓ Gestion correcte d'ID inexistant

Test 8: Mise à jour d'un place
Tentative de mise à jour pour l'ID: 5ee10e3d-c89f-407c-a3c7-ff99b3b7c178
Réponse: {
    "id": "5ee10e3d-c89f-407c-a3c7-ff99b3b7c178",
    "title": "Updated Apartment",
    "description": "An updated description",
    "price": 150.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "bf6fe115-4025-48f4-9580-c474e20009cf",
    "amenities": [
        "647cc858-b560-433e-81e1-d8230b4b72dd",
        "d85b4620-989b-4b96-bc88-14be3f22a93b"
    ]
}
✓ Mise à jour du place réussie

Test 9: Mise à jour d'un place avec ID inexistant
Réponse: {
    "error": "Place not found"
}
✓ Gestion correcte de mise à jour avec ID inexistant

┌────────────────────────────────────────────┐
│             TESTS DES API REVIEWS           │
└────────────────────────────────────────────┘

Test préliminaire: Création d'un utilisateur pour les tests
ID utilisateur extrait: 7455e4d4-7535-4ba9-918c-357047ea6b78
Test préliminaire: Création d'un place pour les tests
ID place extrait: b38e3530-c3e8-4af7-b75c-cb55bb114766
Test 1: Création d'une review valide
Réponse: {
    "id": "3cc1b2f7-5dc4-4855-a28d-b0ed9e85d525",
    "text": "Great place to stay!",
    "rating": 5,
    "user_id": "7455e4d4-7535-4ba9-918c-357047ea6b78",
    "place_id": "b38e3530-c3e8-4af7-b75c-cb55bb114766",
    "created_at": "2025-03-02T02:47:05.902166",
    "updated_at": "2025-03-02T02:47:05.902168"
}
ID review extrait: 3cc1b2f7-5dc4-4855-a28d-b0ed9e85d525
✓ Création de review réussie. ID: 3cc1b2f7-5dc4-4855-a28d-b0ed9e85d525

Test 2: Création d'une review avec utilisateur inexistant
Réponse: {
    "error": "User with ID invalid_user_id does not exist"
}
✓ Détection correcte d'utilisateur invalide

Test 3: Création d'une review avec place inexistant
Réponse: {
    "error": "Place with ID invalid_place_id does not exist"
}
✓ Détection correcte de place invalide

Test 4: Création d'une review avec note invalide
Réponse: {
    "error": "Rating must be between 1 and 5"
}
✓ Détection correcte de note invalide

Test 5: Récupération de toutes les reviews
Réponse: [
    {
        "id": "3cc1b2f7-5dc4-4855-a28d-b0ed9e85d525",
        "text": "Great place to stay!",
        "rating": 5,
        "created_at": "2025-03-02T02:47:05.902166",
        "updated_at": "2025-03-02T02:47:05.902168"
    }
]
✓ Récupération de la liste des reviews réussie

Test 6: Récupération d'une review par ID
Tentative de récupération pour l'ID: 3cc1b2f7-5dc4-4855-a28d-b0ed9e85d525
Réponse: {
    "id": "3cc1b2f7-5dc4-4855-a28d-b0ed9e85d525",
    "text": "Great place to stay!",
    "rating": 5,
    "user_id": "7455e4d4-7535-4ba9-918c-357047ea6b78",
    "place_id": "b38e3530-c3e8-4af7-b75c-cb55bb114766",
    "created_at": "2025-03-02T02:47:05.902166",
    "updated_at": "2025-03-02T02:47:05.902168"
}
✓ Récupération de la review réussie

Test 7: Récupération des reviews par place ID
Réponse: [
    {
        "id": "3cc1b2f7-5dc4-4855-a28d-b0ed9e85d525",
        "text": "Great place to stay!",
        "rating": 5,
        "user_id": "7455e4d4-7535-4ba9-918c-357047ea6b78",
        "created_at": "2025-03-02T02:47:05.902166",
        "updated_at": "2025-03-02T02:47:05.902168"
    }
]
✓ Récupération des reviews par place ID réussie

Test 8: Mise à jour d'une review
Tentative de mise à jour pour l'ID: 3cc1b2f7-5dc4-4855-a28d-b0ed9e85d525
Réponse: {
    "id": "3cc1b2f7-5dc4-4855-a28d-b0ed9e85d525",
    "text": "Updated review text",
    "rating": 4,
    "user_id": "7455e4d4-7535-4ba9-918c-357047ea6b78",
    "place_id": "b38e3530-c3e8-4af7-b75c-cb55bb114766",
    "created_at": "2025-03-02T02:47:05.902166",
    "updated_at": "2025-03-02T02:47:05.980146"
}
✓ Mise à jour de la review réussie

Test 9: Mise à jour avec note invalide
Réponse: {
    "error": "Rating must be between 1 and 5"
}
✓ Détection correcte de note invalide lors de la mise à jour

Test 10: Mise à jour avec ID inexistant
Réponse: {
    "error": "Review not found"
}
✓ Gestion correcte de mise à jour avec ID inexistant

Test 11: Suppression d'une review
Tentative de suppression pour l'ID: 3cc1b2f7-5dc4-4855-a28d-b0ed9e85d525
Réponse: {
    "message": "Review deleted successfully"
}
✓ Suppression de la review réussie

Test 12: Suppression avec ID inexistant
Réponse: {
    "error": "Review not found"
}
✓ Gestion correcte de suppression avec ID inexistant

Test 13: Vérification que la review a bien été supprimée
Réponse: {
    "error": "Review not found"
}
✓ La review a bien été supprimée

Test 14: Création d'une nouvelle review et vérification dans les détails du place
ID nouvelle review: 7d7863fb-a257-48ea-a1cc-a5513f7dd702
Réponse détails place: {
    "id": "b38e3530-c3e8-4af7-b75c-cb55bb114766",
    "title": "Place for Reviews",
    "description": "A place to test reviews",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner": {
        "id": "7455e4d4-7535-4ba9-918c-357047ea6b78",
        "first_name": "Review",
        "last_name": "Tester",
        "email": "review.tester1740880025@example.com"
    },
    "amenities": [],
    "reviews": [
        {
            "id": "7d7863fb-a257-48ea-a1cc-a5513f7dd702",
            "text": "Another great review",
            "rating": 5,
            "user_id": "7455e4d4-7535-4ba9-918c-357047ea6b78"
        }
    ],
    "created_at": "2025-03-02T02:47:05.889947",
    "updated_at": "2025-03-02T02:47:05.889954"
}
✓ La nouvelle review apparaît dans les détails du place

┌────────────────────────────────────────────┐
│              TESTS TERMINÉS                │
└────────────────────────────────────────────┘
