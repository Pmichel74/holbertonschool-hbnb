meurtphy@m23:~/holbertonschool-hbnb/part2/hbnb/part2/hbnb/tests$ python3 test_users_api_unittest.py
test_01_create_user_valid (__main__.TestHBnBAPI.test_01_create_user_valid)
Test 1: Création d'un utilisateur valide ... Réponse: {
    "id": "4c7d777f-8f65-4ee7-bb11-b97785c404fd",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "is_admin": false,
    "created_at": "2025-03-02T22:13:38.127313",
    "updated_at": "2025-03-02T22:13:38.127315"
}

ID extrait: 4c7d777f-8f65-4ee7-bb11-b97785c404fd
ok
test_02_create_user_duplicate_email (__main__.TestHBnBAPI.test_02_create_user_duplicate_email)
Test 2: Création d'un utilisateur avec email déjà existant ... Réponse: {
    "error": "Email already registered"
}

ok
test_03_create_user_invalid_data (__main__.TestHBnBAPI.test_03_create_user_invalid_data)
Test 3: Création d'un utilisateur avec données invalides (manque first_name) ... Réponse: {
    "errors": {
        "first_name": "'first_name' is a required property"
    },
    "message": "Input payload validation failed"
}

ok
test_04_get_all_users (__main__.TestHBnBAPI.test_04_get_all_users)
Test 4: Récupération de tous les utilisateurs ... Réponse: [
    {
        "id": "4c7d777f-8f65-4ee7-bb11-b97785c404fd",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "created_at": "2025-03-02T22:13:38.127313",
        "updated_at": "2025-03-02T22:13:38.127315"
    }
]

ok
test_05_get_user_by_id (__main__.TestHBnBAPI.test_05_get_user_by_id)
Test 5: Récupération d'un utilisateur par ID ... Réponse: {
    "id": "4c7d777f-8f65-4ee7-bb11-b97785c404fd",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "is_admin": false,
    "created_at": "2025-03-02T22:13:38.127313",
    "updated_at": "2025-03-02T22:13:38.127315"
}

ok
test_06_get_user_invalid_id (__main__.TestHBnBAPI.test_06_get_user_invalid_id)
Test 6: Récupération d'un utilisateur avec ID inexistant ... Réponse: {
    "error": "User not found"
}

ok
test_07_update_user (__main__.TestHBnBAPI.test_07_update_user)
Test 7: Mise à jour d'un utilisateur ... Réponse: {
    "id": "4c7d777f-8f65-4ee7-bb11-b97785c404fd",
    "first_name": "John-Updated",
    "last_name": "Doe-Updated",
    "email": "john.updated@example.com",
    "is_admin": false,
    "created_at": "2025-03-02T22:13:38.127313",
    "updated_at": "2025-03-02T22:13:38.143857"
}

ok
test_08_update_user_invalid_id (__main__.TestHBnBAPI.test_08_update_user_invalid_id)
Test 8: Mise à jour d'un utilisateur avec ID inexistant ... Réponse: {
    "error": "User not found"
}

ok
test_09_create_second_user (__main__.TestHBnBAPI.test_09_create_second_user)
Test 9: Création d'un deuxième utilisateur ... Réponse: {
    "id": "62efb659-e0ac-456d-b7da-e5745fca10ec",
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane.smith@example.com",
    "is_admin": false,
    "created_at": "2025-03-02T22:13:38.148262",
    "updated_at": "2025-03-02T22:13:38.148264"
}

ID extrait (2e user): 62efb659-e0ac-456d-b7da-e5745fca10ec
ok
test_10_verify_two_users (__main__.TestHBnBAPI.test_10_verify_two_users)
Test 10: Vérification de la liste pour voir les deux utilisateurs ... Réponse: [
    {
        "id": "4c7d777f-8f65-4ee7-bb11-b97785c404fd",
        "first_name": "John-Updated",
        "last_name": "Doe-Updated",
        "email": "john.updated@example.com",
        "created_at": "2025-03-02T22:13:38.127313",
        "updated_at": "2025-03-02T22:13:38.143857"
    },
    {
        "id": "62efb659-e0ac-456d-b7da-e5745fca10ec",
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "created_at": "2025-03-02T22:13:38.148262",
        "updated_at": "2025-03-02T22:13:38.148264"
    }
]

ok
test_11_create_amenity_valid (__main__.TestHBnBAPI.test_11_create_amenity_valid)
Test 1: Création d'une amenity valide ... Réponse: {
    "id": "68fe546a-3d5e-465d-a637-f43df10d11f8",
    "name": "Wi-Fi",
    "created_at": "2025-03-02T22:13:38.153923",
    "updated_at": "2025-03-02T22:13:38.153925"
}

ID extrait amenity: 68fe546a-3d5e-465d-a637-f43df10d11f8
ok
test_12_create_amenity_invalid (__main__.TestHBnBAPI.test_12_create_amenity_invalid)
Test 2: Création d'une amenity avec données invalides ... Réponse: {
    "errors": {
        "name": "'name' is a required property"
    },
    "message": "Input payload validation failed"
}

ok
test_13_get_all_amenities (__main__.TestHBnBAPI.test_13_get_all_amenities)
Test 3: Récupération de toutes les amenities ... Réponse: [
    {
        "id": "68fe546a-3d5e-465d-a637-f43df10d11f8",
        "name": "Wi-Fi",
        "created_at": "2025-03-02T22:13:38.153923",
        "updated_at": "2025-03-02T22:13:38.153925"
    }
]

ok
test_14_get_amenity_by_id (__main__.TestHBnBAPI.test_14_get_amenity_by_id)
Test 4: Récupération d'une amenity par ID ... Réponse: {
    "id": "68fe546a-3d5e-465d-a637-f43df10d11f8",
    "name": "Wi-Fi",
    "created_at": "2025-03-02T22:13:38.153923",
    "updated_at": "2025-03-02T22:13:38.153925"
}

ok
test_15_get_amenity_invalid_id (__main__.TestHBnBAPI.test_15_get_amenity_invalid_id)
Test 5: Récupération d'une amenity avec ID inexistant ... Réponse: {
    "error": "Amenity not found"
}

ok
test_16_update_amenity (__main__.TestHBnBAPI.test_16_update_amenity)
Test 6: Mise à jour d'une amenity ... Réponse: {
    "id": "68fe546a-3d5e-465d-a637-f43df10d11f8",
    "name": "Air Conditioning",
    "created_at": "2025-03-02T22:13:38.153923",
    "updated_at": "2025-03-02T22:13:38.163780"
}

ok
test_17_update_amenity_invalid_id (__main__.TestHBnBAPI.test_17_update_amenity_invalid_id)
Test 7: Mise à jour d'une amenity avec ID inexistant ... Réponse: {
    "error": "Amenity not found"
}

ok
test_18_create_second_amenity (__main__.TestHBnBAPI.test_18_create_second_amenity)
Test 8: Création d'une deuxième amenity ... Réponse: {
    "id": "724a0bd3-5905-408b-82ab-850189a26eb9",
    "name": "Swimming Pool",
    "created_at": "2025-03-02T22:13:38.169113",
    "updated_at": "2025-03-02T22:13:38.169115"
}

ID extrait 2e amenity: 724a0bd3-5905-408b-82ab-850189a26eb9
ok
test_19_verify_two_amenities (__main__.TestHBnBAPI.test_19_verify_two_amenities)
Test 9: Vérification de la liste avec deux amenities ... Réponse: [
    {
        "id": "68fe546a-3d5e-465d-a637-f43df10d11f8",
        "name": "Air Conditioning",
        "created_at": "2025-03-02T22:13:38.153923",
        "updated_at": "2025-03-02T22:13:38.163780"
    },
    {
        "id": "724a0bd3-5905-408b-82ab-850189a26eb9",
        "name": "Swimming Pool",
        "created_at": "2025-03-02T22:13:38.169113",
        "updated_at": "2025-03-02T22:13:38.169115"
    }
]

ok
test_20_create_user_for_place (__main__.TestHBnBAPI.test_20_create_user_for_place)
Test préliminaire: Création d'un utilisateur pour les tests de place ... Réponse: {
    "id": "619e6ba5-eedc-4406-b6ec-d5df3dcf8717",
    "first_name": "Place",
    "last_name": "Owner",
    "email": "place.owner1740950018@example.com",
    "is_admin": false,
    "created_at": "2025-03-02T22:13:38.174779",
    "updated_at": "2025-03-02T22:13:38.174781"
}

ID utilisateur extrait (pour place): 619e6ba5-eedc-4406-b6ec-d5df3dcf8717
ok
test_21_create_amenities_for_place (__main__.TestHBnBAPI.test_21_create_amenities_for_place)
Test préliminaire: Création d'amenities pour les tests place ... Amenity1: c938fde8-5f8c-40cc-8f16-da14152665a7 Amenity2: de2a5254-a344-4af7-8503-157b6ac056c1
ok
test_22_create_place_valid (__main__.TestHBnBAPI.test_22_create_place_valid)
Test 1: Création d'un place valide ... Réponse: {
    "id": "d346b012-2bb7-417e-9d71-a61b5790ce46",
    "title": "Cozy Apartment",
    "description": "A nice place to stay",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "619e6ba5-eedc-4406-b6ec-d5df3dcf8717",
    "amenities": [
        "c938fde8-5f8c-40cc-8f16-da14152665a7",
        "de2a5254-a344-4af7-8503-157b6ac056c1"
    ]
}

ID place extrait: d346b012-2bb7-417e-9d71-a61b5790ce46
ok
test_23_create_place_invalid_owner (__main__.TestHBnBAPI.test_23_create_place_invalid_owner)
Test 2: Création d'un place avec propriétaire invalide ... Réponse: {
    "error": "Owner with ID invalid_owner_id does not exist"
}

ok
test_24_create_place_negative_price (__main__.TestHBnBAPI.test_24_create_place_negative_price)
Test 3: Création d'un place avec prix négatif ... Réponse: {
    "error": "Price cannot be negative"
}

ok
test_25_create_place_invalid_latitude (__main__.TestHBnBAPI.test_25_create_place_invalid_latitude)
Test 4: Création d'un place avec latitude invalide ... Réponse: {
    "error": "Latitude must be between -90 and 90"
}

ok
test_26_get_all_places (__main__.TestHBnBAPI.test_26_get_all_places)
Test 5: Liste de tous les places ... Réponse: [
    {
        "id": "d346b012-2bb7-417e-9d71-a61b5790ce46",
        "title": "Cozy Apartment",
        "latitude": 37.7749,
        "longitude": -122.4194
    }
]

ok
test_27_get_place_by_id (__main__.TestHBnBAPI.test_27_get_place_by_id)
Test 6: Détail d'un place par ID ... Réponse: {
    "id": "d346b012-2bb7-417e-9d71-a61b5790ce46",
    "title": "Cozy Apartment",
    "description": "A nice place to stay",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner": {
        "id": "619e6ba5-eedc-4406-b6ec-d5df3dcf8717",
        "first_name": "Place",
        "last_name": "Owner",
        "email": "place.owner1740950018@example.com"
    },
    "amenities": [
        {
            "id": "c938fde8-5f8c-40cc-8f16-da14152665a7",
            "name": "Wi-Fi"
        },
        {
            "id": "de2a5254-a344-4af7-8503-157b6ac056c1",
            "name": "Swimming Pool"
        }
    ],
    "reviews": [],
    "created_at": "2025-03-02T22:13:38.184474",
    "updated_at": "2025-03-02T22:13:38.184476"
}

ok
test_28_get_place_invalid_id (__main__.TestHBnBAPI.test_28_get_place_invalid_id)
Test 7: Récupération d'un place avec ID inexistant ... Réponse: {
    "error": "Place not found"
}

ok
test_29_update_place (__main__.TestHBnBAPI.test_29_update_place)
Test 8: Mise à jour d'un place ... Réponse: {
    "id": "d346b012-2bb7-417e-9d71-a61b5790ce46",
    "title": "Updated Apartment",
    "description": "An updated description",
    "price": 150.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "619e6ba5-eedc-4406-b6ec-d5df3dcf8717",
    "amenities": [
        "c938fde8-5f8c-40cc-8f16-da14152665a7",
        "de2a5254-a344-4af7-8503-157b6ac056c1"
    ]
}

ok
test_30_update_place_invalid_id (__main__.TestHBnBAPI.test_30_update_place_invalid_id)
Test 9: Mise à jour d'un place avec ID inexistant ... Réponse: {
    "error": "Place not found"
}

ok
test_31_create_user_for_review (__main__.TestHBnBAPI.test_31_create_user_for_review)
Test préliminaire: Création d'un utilisateur pour les tests review ... Réponse: {
    "id": "17608fd5-e6ad-44cb-9832-65493f0a5d1d",
    "first_name": "Review",
    "last_name": "Tester",
    "email": "review.tester1740950018@example.com",
    "is_admin": false,
    "created_at": "2025-03-02T22:13:38.204779",
    "updated_at": "2025-03-02T22:13:38.204780"
}

ok
test_32_create_place_for_review (__main__.TestHBnBAPI.test_32_create_place_for_review)
Test préliminaire: Création d'un place pour les tests review ... Réponse: {
    "id": "ede67286-1cc3-44ee-bba7-3cca78c647af",
    "title": "Place for Reviews",
    "description": "A place to test reviews",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "17608fd5-e6ad-44cb-9832-65493f0a5d1d",
    "amenities": []
}

ok
test_33_create_review_valid (__main__.TestHBnBAPI.test_33_create_review_valid)
Test 1: Création d'une review valide ... Réponse: {
    "id": "019561a1-d594-4798-8ada-fa7d21e6a8a8",
    "text": "Great place to stay!",
    "rating": 5,
    "user_id": "17608fd5-e6ad-44cb-9832-65493f0a5d1d",
    "place_id": "ede67286-1cc3-44ee-bba7-3cca78c647af",
    "created_at": "2025-03-02T22:13:38.210081",
    "updated_at": "2025-03-02T22:13:38.210083"
}

ok
test_34_create_review_invalid_user (__main__.TestHBnBAPI.test_34_create_review_invalid_user)
Test 2: Création d'une review avec un utilisateur inexistant ... Réponse: {
    "error": "User with ID invalid_user_id does not exist"
}

ok
test_35_create_review_invalid_place (__main__.TestHBnBAPI.test_35_create_review_invalid_place)
Test 3: Création d'une review avec place inexistant ... Réponse: {
    "error": "Place with ID invalid_place_id does not exist"
}

ok
test_36_create_review_invalid_rating (__main__.TestHBnBAPI.test_36_create_review_invalid_rating)
Test 4: Création d'une review avec note invalide ... Réponse: {
    "error": "Rating must be between 1 and 5"
}

ok
test_37_get_all_reviews (__main__.TestHBnBAPI.test_37_get_all_reviews)
Test 5: Récupération de toutes les reviews ... Réponse: [
    {
        "id": "019561a1-d594-4798-8ada-fa7d21e6a8a8",
        "text": "Great place to stay!",
        "rating": 5,
        "created_at": "2025-03-02T22:13:38.210081",
        "updated_at": "2025-03-02T22:13:38.210083"
    }
]

ok
test_38_get_review_by_id (__main__.TestHBnBAPI.test_38_get_review_by_id)
Test 6: Récupération d'une review par ID ... Réponse: {
    "id": "019561a1-d594-4798-8ada-fa7d21e6a8a8",
    "text": "Great place to stay!",
    "rating": 5,
    "user_id": "17608fd5-e6ad-44cb-9832-65493f0a5d1d",
    "place_id": "ede67286-1cc3-44ee-bba7-3cca78c647af",
    "created_at": "2025-03-02T22:13:38.210081",
    "updated_at": "2025-03-02T22:13:38.210083"
}

ok
test_39_get_reviews_by_place (__main__.TestHBnBAPI.test_39_get_reviews_by_place)
Test 7: Récupération de toutes les reviews d'un place par son ID ... Réponse: [
    {
        "id": "019561a1-d594-4798-8ada-fa7d21e6a8a8",
        "text": "Great place to stay!",
        "rating": 5,
        "user_id": "17608fd5-e6ad-44cb-9832-65493f0a5d1d",
        "created_at": "2025-03-02T22:13:38.210081",
        "updated_at": "2025-03-02T22:13:38.210083"
    }
]

ok
test_40_update_review (__main__.TestHBnBAPI.test_40_update_review)
Test 8: Mise à jour d'une review ... Réponse: {
    "id": "019561a1-d594-4798-8ada-fa7d21e6a8a8",
    "text": "Updated review text",
    "rating": 4,
    "user_id": "17608fd5-e6ad-44cb-9832-65493f0a5d1d",
    "place_id": "ede67286-1cc3-44ee-bba7-3cca78c647af",
    "created_at": "2025-03-02T22:13:38.210081",
    "updated_at": "2025-03-02T22:13:38.225390"
}

ok
test_41_update_review_invalid_rating (__main__.TestHBnBAPI.test_41_update_review_invalid_rating)
Test 9: Mise à jour avec note invalide ... Réponse: {
    "error": "Rating must be between 1 and 5"
}

ok
test_42_update_review_invalid_id (__main__.TestHBnBAPI.test_42_update_review_invalid_id)
Test 10: Mise à jour avec ID inexistant ... Réponse: {
    "error": "Review not found"
}

ok
test_43_delete_review (__main__.TestHBnBAPI.test_43_delete_review)
Test 11: Suppression d'une review ... Réponse: {
    "message": "Review deleted successfully"
}

ok
test_44_delete_review_invalid_id (__main__.TestHBnBAPI.test_44_delete_review_invalid_id)
Test 12: Suppression avec ID inexistant ... Réponse: {
    "error": "Review not found"
}

ok
test_45_verify_review_deleted (__main__.TestHBnBAPI.test_45_verify_review_deleted)
Test 13: Vérification que la review a bien été supprimée ... Réponse: {
    "error": "Review not found"
}

ok
test_46_create_new_review_for_place_details (__main__.TestHBnBAPI.test_46_create_new_review_for_place_details)
Test 14: Création d'une nouvelle review et vérification dans les détails du place ... Réponse (new review): {
    "id": "2a8a5c99-d9ff-4596-a870-f07de3b64869",
    "text": "Another great review",
    "rating": 5,
    "user_id": "17608fd5-e6ad-44cb-9832-65493f0a5d1d",
    "place_id": "ede67286-1cc3-44ee-bba7-3cca78c647af",
    "created_at": "2025-03-02T22:13:38.235770",
    "updated_at": "2025-03-02T22:13:38.235772"
}

Réponse détails place: {
    "id": "ede67286-1cc3-44ee-bba7-3cca78c647af",
    "title": "Place for Reviews",
    "description": "A place to test reviews",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner": {
        "id": "17608fd5-e6ad-44cb-9832-65493f0a5d1d",
        "first_name": "Review",
        "last_name": "Tester",
        "email": "review.tester1740950018@example.com"
    },
    "amenities": [],
    "reviews": [
        {
            "id": "2a8a5c99-d9ff-4596-a870-f07de3b64869",
            "text": "Another great review",
            "rating": 5,
            "user_id": "17608fd5-e6ad-44cb-9832-65493f0a5d1d"
        }
    ],
    "created_at": "2025-03-02T22:13:38.207501",
    "updated_at": "2025-03-02T22:13:38.207503"
}

ok

----------------------------------------------------------------------
Ran 46 tests in 0.117s

OK