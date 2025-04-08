import unittest
import requests
import time
import json

BASE_URL = "http://localhost:5000/api/v1"
USER_ENDPOINT = f"{BASE_URL}/users"
AMENITY_ENDPOINT = f"{BASE_URL}/amenities"
PLACE_ENDPOINT = f"{BASE_URL}/places"
REVIEW_ENDPOINT = f"{BASE_URL}/reviews"


class TestHBnBAPI(unittest.TestCase):
    """
    Réplique du script Bash complet (Sections Users, Amenities, Places, Reviews).
    Chaque 'Test X:' du script correspond à une méthode test_X_... ici.
    """

    @classmethod
    def setUpClass(cls):
        """
        Préparation : on crée une session requests commune.
        On stockera tous les ID créés au fur et à mesure, de la même manière
        que le script Bash stocke ses variables.
        """
        cls.session = requests.Session()

        # SECTION 1 variables
        cls.user_id = None
        cls.user_id2 = None

        # SECTION 2 variables
        cls.amenity_id = None
        cls.amenity_id2 = None

        # SECTION 3 variables
        # (pour le test place on crée "USER_ID" + 2 amenities + place)
        cls.place_test_user_id = None
        cls.place_test_amenity1_id = None
        cls.place_test_amenity2_id = None
        cls.place_id = None

        # SECTION 4 variables
        # (pour reviews : user, place, review)
        cls.review_test_user_id = None
        cls.review_test_place_id = None
        cls.review_id = None

    #
    # ============================
    # SECTION 1: TESTS DES ENDPOINTS UTILISATEUR
    # ============================
    #

    def test_01_create_user_valid(self):
        """Test 1: Création d'un utilisateur valide"""
        payload = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        }
        resp = self.session.post(USER_ENDPOINT, json=payload)
        print("Réponse:", resp.text)

        self.assertIn(resp.status_code, [200, 201], "Le statut devrait être 200 ou 201")
        data = resp.json()
        self.__class__.user_id = data.get("id")
        print("ID extrait:", self.user_id)
        self.assertTrue(self.user_id, "Échec de la création d'utilisateur")

    def test_02_create_user_duplicate_email(self):
        """Test 2: Création d'un utilisateur avec email déjà existant"""
        payload = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "john.doe@example.com"
        }
        resp = self.session.post(USER_ENDPOINT, json=payload)
        print("Réponse:", resp.text)

        # Le script Bash vérifie si "Email already registered" apparaît
        self.assertEqual(resp.status_code, 400, "Le code HTTP devrait être 400 pour email dupliqué")
        self.assertIn("Email already registered", resp.text)

    def test_03_create_user_invalid_data(self):
        """Test 3: Création d'un utilisateur avec données invalides (manque first_name)"""
        payload = {
            "last_name": "Doe",
            "email": "invalid_user@example.com"
        }
        resp = self.session.post(USER_ENDPOINT, json=payload)
        print("Réponse:", resp.text)

        self.assertEqual(resp.status_code, 400, "Le code HTTP devrait être 400 pour data invalide")
        self.assertTrue("error" in resp.text or "errors" in resp.text,
                        "Le message d'erreur attendu n'est pas présent")

    def test_04_get_all_users(self):
        """Test 4: Récupération de tous les utilisateurs"""
        resp = self.session.get(USER_ENDPOINT)
        print("Réponse:", resp.text)

        self.assertEqual(resp.status_code, 200, "Status code inattendu pour GET all users")
        users_list = resp.json()
        self.assertIsInstance(users_list, list, "La réponse doit être une liste")
        self.assertTrue(len(users_list) > 0, "La liste d'utilisateurs est vide")

    def test_05_get_user_by_id(self):
        """Test 5: Récupération d'un utilisateur par ID"""
        self.assertIsNotNone(self.user_id, "user_id non défini (test_01 a échoué ?)")
        url = f"{USER_ENDPOINT}/{self.user_id}"
        resp = self.session.get(url)
        print("Réponse:", resp.text)

        self.assertEqual(resp.status_code, 200, "Le code HTTP devrait être 200 pour get user by id")
        data = resp.json()
        self.assertEqual(data.get("id"), self.user_id, "L'ID ne correspond pas")

    def test_06_get_user_invalid_id(self):
        """Test 6: Récupération d'un utilisateur avec ID inexistant"""
        url = f"{USER_ENDPOINT}/invalid_id_12345"
        resp = self.session.get(url)
        print("Réponse:", resp.text)

        self.assertEqual(resp.status_code, 404, "Le code HTTP devrait être 404 pour un ID inexistant")
        self.assertTrue("not found" in resp.text or "error" in resp.text,
                        "Pas de message 'not found' ou 'error'")

    def test_07_update_user(self):
        """Test 7: Mise à jour d'un utilisateur"""
        self.assertIsNotNone(self.user_id, "user_id non défini")
        url = f"{USER_ENDPOINT}/{self.user_id}"
        payload = {
            "first_name": "John-Updated",
            "last_name": "Doe-Updated",
            "email": "john.updated@example.com"
        }
        resp = self.session.put(url, json=payload)
        print("Réponse:", resp.text)

        self.assertEqual(resp.status_code, 200, "Le code HTTP devrait être 200 pour la mise à jour")
        updated_name = resp.json().get("first_name")
        self.assertEqual(updated_name, "John-Updated", "La mise à jour n'a pas fonctionné")

    def test_08_update_user_invalid_id(self):
        """Test 8: Mise à jour d'un utilisateur avec ID inexistant"""
        url = f"{USER_ENDPOINT}/invalid_id_12345"
        payload = {
            "first_name": "Invalid",
            "last_name": "Update",
            "email": "invalid.update@example.com"
        }
        resp = self.session.put(url, json=payload)
        print("Réponse:", resp.text)

        self.assertEqual(resp.status_code, 404, "Le code HTTP devrait être 404 pour un ID inexistant")
        self.assertTrue("not found" in resp.text or "error" in resp.text)

    def test_09_create_second_user(self):
        """Test 9: Création d'un deuxième utilisateur"""
        payload = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com"
        }
        resp = self.session.post(USER_ENDPOINT, json=payload)
        print("Réponse:", resp.text)

        self.assertIn(resp.status_code, [200, 201], "Le code devrait être 200 ou 201 pour la création")
        data = resp.json()
        self.__class__.user_id2 = data.get("id")
        print("ID extrait (2e user):", self.user_id2)
        self.assertTrue(self.user_id2, "Échec de la création du deuxième utilisateur")

    def test_10_verify_two_users(self):
        """Test 10: Vérification de la liste pour voir les deux utilisateurs"""
        self.assertIsNotNone(self.user_id, "Premier user_id absent")
        self.assertIsNotNone(self.user_id2, "Deuxième user_id absent")

        resp = self.session.get(USER_ENDPOINT)
        print("Réponse:", resp.text)
        self.assertEqual(resp.status_code, 200, "Status code inattendu pour GET all users")

        all_users = resp.json()
        all_ids = [u.get("id") for u in all_users if "id" in u]
        self.assertIn(self.user_id, all_ids, "Le premier user est introuvable")
        self.assertIn(self.user_id2, all_ids, "Le deuxième user est introuvable")

    #
    # ============================
    # SECTION 2: TESTS DES ENDPOINTS AMENITY
    # ============================
    #

    def test_11_create_amenity_valid(self):
        """Test 1: Création d'une amenity valide"""
        payload = {"name": "Wi-Fi"}
        resp = self.session.post(AMENITY_ENDPOINT, json=payload)
        print("Réponse:", resp.text)

        self.assertIn(resp.status_code, [200, 201], "Le statut devrait être 200 ou 201")
        data = resp.json()
        self.__class__.amenity_id = data.get("id")
        print("ID extrait amenity:", self.amenity_id)
        self.assertTrue(self.amenity_id, "Échec de la création d'amenity")

    def test_12_create_amenity_invalid(self):
        """Test 2: Création d'une amenity avec données invalides"""
        payload = {}
        resp = self.session.post(AMENITY_ENDPOINT, json=payload)
        print("Réponse:", resp.text)

        self.assertEqual(resp.status_code, 400, "Le code devrait être 400 pour données invalides")
        self.assertTrue("error" in resp.text or "errors" in resp.text)

    def test_13_get_all_amenities(self):
        """Test 3: Récupération de toutes les amenities"""
        resp = self.session.get(AMENITY_ENDPOINT)
        print("Réponse:", resp.text)

        self.assertEqual(resp.status_code, 200, "Le code devrait être 200 pour GET all amenities")
        amenities = resp.json()
        self.assertTrue(len(amenities) > 0, "Liste d'amenities vide")

    def test_14_get_amenity_by_id(self):
        """Test 4: Récupération d'une amenity par ID"""
        self.assertIsNotNone(self.amenity_id, "amenity_id non défini")
        url = f"{AMENITY_ENDPOINT}/{self.amenity_id}"
        resp = self.session.get(url)
        print("Réponse:", resp.text)

        self.assertEqual(resp.status_code, 200, "Le code devrait être 200 pour get amenity by id")
        data = resp.json()
        self.assertEqual(data.get("id"), self.amenity_id)

    def test_15_get_amenity_invalid_id(self):
        """Test 5: Récupération d'une amenity avec ID inexistant"""
        url = f"{AMENITY_ENDPOINT}/invalid_id_12345"
        resp = self.session.get(url)
        print("Réponse:", resp.text)

        # Le script Bash vérifie "not found" ou "error",  on suppose 404 ou 400
        self.assertIn(resp.status_code, [400, 404])
        self.assertTrue("not found" in resp.text or "error" in resp.text)

    def test_16_update_amenity(self):
        """Test 6: Mise à jour d'une amenity"""
        self.assertIsNotNone(self.amenity_id, "amenity_id non défini")
        payload = {"name": "Air Conditioning"}
        url = f"{AMENITY_ENDPOINT}/{self.amenity_id}"
        resp = self.session.put(url, json=payload)
        print("Réponse:", resp.text)

        self.assertEqual(resp.status_code, 200, "Le code devrait être 200 pour update amenity")
        updated_name = resp.json().get("name")
        self.assertEqual(updated_name, "Air Conditioning", "Mise à jour amenity échouée")

    def test_17_update_amenity_invalid_id(self):
        """Test 7: Mise à jour d'une amenity avec ID inexistant"""
        url = f"{AMENITY_ENDPOINT}/invalid_id_12345"
        payload = {"name": "Invalid Update"}
        resp = self.session.put(url, json=payload)
        print("Réponse:", resp.text)

        self.assertIn(resp.status_code, [400, 404])
        self.assertTrue("not found" in resp.text or "error" in resp.text)

    def test_18_create_second_amenity(self):
        """Test 8: Création d'une deuxième amenity"""
        payload = {"name": "Swimming Pool"}
        resp = self.session.post(AMENITY_ENDPOINT, json=payload)
        print("Réponse:", resp.text)

        self.assertIn(resp.status_code, [200, 201])
        data = resp.json()
        self.__class__.amenity_id2 = data.get("id")
        print("ID extrait 2e amenity:", self.amenity_id2)
        self.assertTrue(self.amenity_id2, "Échec de la création de la deuxième amenity")

    def test_19_verify_two_amenities(self):
        """Test 9: Vérification de la liste avec deux amenities"""
        self.assertIsNotNone(self.amenity_id, "amenity_id non défini")
        self.assertIsNotNone(self.amenity_id2, "amenity_id2 non défini")

        resp = self.session.get(AMENITY_ENDPOINT)
        print("Réponse:", resp.text)
        self.assertEqual(resp.status_code, 200, "Le code devrait être 200 pour GET amenities")

        all_am = resp.json()
        all_ids = [am.get("id") for am in all_am if "id" in am]
        self.assertIn(self.amenity_id, all_ids, "Première amenity introuvable")
        self.assertIn(self.amenity_id2, all_ids, "Deuxième amenity introuvable")

    #
    # ============================
    # SECTION 3: TESTS DES ENDPOINTS PLACE
    # ============================
    #
    # 0. Create test user and amenities first
    #

    def test_20_create_user_for_place(self):
        """Test préliminaire: Création d'un utilisateur pour les tests de place"""
        payload = {
            "first_name": "Place",
            "last_name": "Owner",
            "email": f"place.owner{int(time.time())}@example.com"
        }
        resp = self.session.post(USER_ENDPOINT, json=payload)
        print("Réponse:", resp.text)

        if resp.status_code in [200, 201]:
            self.__class__.place_test_user_id = resp.json().get("id")
        print("ID utilisateur extrait (pour place):", self.place_test_user_id)
        self.assertTrue(self.place_test_user_id, "Échec de la création d'utilisateur pour place")

    def test_21_create_amenities_for_place(self):
        """Test préliminaire: Création d'amenities pour les tests place"""
        # Amenity 1
        payload_am1 = {"name": "Wi-Fi"}
        r_am1 = self.session.post(AMENITY_ENDPOINT, json=payload_am1)
        if r_am1.status_code in [200, 201]:
            self.__class__.place_test_amenity1_id = r_am1.json().get("id")

        # Amenity 2
        payload_am2 = {"name": "Swimming Pool"}
        r_am2 = self.session.post(AMENITY_ENDPOINT, json=payload_am2)
        if r_am2.status_code in [200, 201]:
            self.__class__.place_test_amenity2_id = r_am2.json().get("id")

        print("Amenity1:", self.place_test_amenity1_id, "Amenity2:", self.place_test_amenity2_id)
        self.assertTrue(self.place_test_amenity1_id, "Échec creation amenity 1 pour place")
        self.assertTrue(self.place_test_amenity2_id, "Échec creation amenity 2 pour place")

    def test_22_create_place_valid(self):
        """Test 1: Création d'un place valide"""
        self.assertTrue(self.place_test_user_id, "Pas de user pour créer un place")
        payload = {
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.place_test_user_id,
            "amenities": [
                self.place_test_amenity1_id,
                self.place_test_amenity2_id
            ]
        }
        resp = self.session.post(PLACE_ENDPOINT, json=payload)
        print("Réponse:", resp.text)
        self.assertIn(resp.status_code, [200, 201])
        data = resp.json()
        self.__class__.place_id = data.get("id")
        print("ID place extrait:", self.place_id)
        self.assertTrue(self.place_id, "Échec de la création de place")

    def test_23_create_place_invalid_owner(self):
        """Test 2: Création d'un place avec propriétaire invalide"""
        payload = {
            "title": "Invalid Owner Apartment",
            "description": "A place with invalid owner",
            "price": 120.0,
            "latitude": 38.7749,
            "longitude": -121.4194,
            "owner_id": "invalid_owner_id",
            "amenities": []
        }
        resp = self.session.post(PLACE_ENDPOINT, json=payload)
        print("Réponse:", resp.text)

        # Le script Bash check: if [[ $INVALID_OWNER_RESPONSE == *\"error\"* ]]
        self.assertIn(resp.status_code, [400, 404], "Le code doit être 400 ou 404 pour owner invalide")
        self.assertIn("error", resp.text, "Pas de mention d'erreur")

    def test_24_create_place_negative_price(self):
        """Test 3: Création d'un place avec prix négatif"""
        self.assertTrue(self.place_test_user_id, "Pas de user valide pour tester price négatif")
        payload = {
            "title": "Negative Price Place",
            "description": "A place with negative price",
            "price": -50.0,
            "latitude": 39.7749,
            "longitude": -120.4194,
            "owner_id": self.place_test_user_id,
            "amenities": []
        }
        resp = self.session.post(PLACE_ENDPOINT, json=payload)
        print("Réponse:", resp.text)
        self.assertEqual(resp.status_code, 400, "La création devrait échouer (prix négatif)")
        self.assertIn("error", resp.text)

    def test_25_create_place_invalid_latitude(self):
        """Test 4: Création d'un place avec latitude invalide"""
        self.assertTrue(self.place_test_user_id, "Pas de user valide pour tester latitude invalide")
        payload = {
            "title": "Invalid Latitude Place",
            "description": "A place with invalid latitude",
            "price": 150.0,
            "latitude": 95.0,
            "longitude": -120.4194,
            "owner_id": self.place_test_user_id,
            "amenities": []
        }
        resp = self.session.post(PLACE_ENDPOINT, json=payload)
        print("Réponse:", resp.text)
        self.assertEqual(resp.status_code, 400, "La création devrait échouer (latitude invalide)")
        self.assertIn("error", resp.text)

    def test_26_get_all_places(self):
        """Test 5: Liste de tous les places"""
        resp = self.session.get(PLACE_ENDPOINT)
        print("Réponse:", resp.text)
        self.assertEqual(resp.status_code, 200, "Le code devrait être 200 pour GET places")
        all_places = resp.json()
        self.assertIsInstance(all_places, list, "Réponse pas une liste")

    def test_27_get_place_by_id(self):
        """Test 6: Détail d'un place par ID"""
        self.assertTrue(self.place_id, "Aucun place_id créé")
        url = f"{PLACE_ENDPOINT}/{self.place_id}"
        resp = self.session.get(url)
        print("Réponse:", resp.text)
        self.assertEqual(resp.status_code, 200, "Le code devrait être 200 pour get place by id")
        data = resp.json()
        self.assertEqual(data.get("id"), self.place_id)

        # Vérifier owner
        owner = data.get("owner", {})
        self.assertEqual(owner.get("id"), self.place_test_user_id, "Owner incorrect")
        # Vérifier amenities
        am_list = data.get("amenities", [])
        self.assertEqual(len(am_list), 2, "2 amenities attendues")

    def test_28_get_place_invalid_id(self):
        """Test 7: Récupération d'un place avec ID inexistant"""
        url = f"{PLACE_ENDPOINT}/invalid_id_12345"
        resp = self.session.get(url)
        print("Réponse:", resp.text)
        self.assertIn(resp.status_code, [400, 404])
        self.assertTrue("not found" in resp.text or "error" in resp.text)

    def test_29_update_place(self):
        """Test 8: Mise à jour d'un place"""
        self.assertTrue(self.place_id, "Pas de place_id")
        url = f"{PLACE_ENDPOINT}/{self.place_id}"
        payload = {
            "title": "Updated Apartment",
            "description": "An updated description",
            "price": 150.0
        }
        resp = self.session.put(url, json=payload)
        print("Réponse:", resp.text)
        self.assertEqual(resp.status_code, 200, "Le code devrait être 200 pour update place")
        updated_title = resp.json().get("title")
        self.assertEqual(updated_title, "Updated Apartment", "Mise à jour place échouée")

    def test_30_update_place_invalid_id(self):
        """Test 9: Mise à jour d'un place avec ID inexistant"""
        url = f"{PLACE_ENDPOINT}/invalid_id_12345"
        payload = {
            "title": "Invalid Update",
            "price": 200.0
        }
        resp = self.session.put(url, json=payload)
        print("Réponse:", resp.text)
        self.assertIn(resp.status_code, [400, 404])
        self.assertTrue("not found" in resp.text or "error" in resp.text)

    #
    # ============================
    # SECTION 4: TESTS DES ENDPOINTS REVIEWS
    # ============================
    #
    # 0. Tests préliminaires : création d'un utilisateur et d'un place pour les tests
    #

    def test_31_create_user_for_review(self):
        """Test préliminaire: Création d'un utilisateur pour les tests review"""
        payload = {
            "first_name": "Review",
            "last_name": "Tester",
            "email": f"review.tester{int(time.time())}@example.com"
        }
        resp = self.session.post(USER_ENDPOINT, json=payload)
        print("Réponse:", resp.text)
        if resp.status_code in [200, 201]:
            self.__class__.review_test_user_id = resp.json().get("id")
        self.assertTrue(self.review_test_user_id, "Échec création user pour review")

    def test_32_create_place_for_review(self):
        """Test préliminaire: Création d'un place pour les tests review"""
        payload = {
            "title": "Place for Reviews",
            "description": "A place to test reviews",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.review_test_user_id,
            "amenities": []
        }
        resp = self.session.post(PLACE_ENDPOINT, json=payload)
        print("Réponse:", resp.text)
        if resp.status_code in [200, 201]:
            self.__class__.review_test_place_id = resp.json().get("id")
        self.assertTrue(self.review_test_place_id, "Échec création place pour reviews")

    def test_33_create_review_valid(self):
        """Test 1: Création d'une review valide"""
        self.assertTrue(self.review_test_user_id, "Aucun user pour créer review")
        self.assertTrue(self.review_test_place_id, "Aucun place pour créer review")

        payload = {
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": self.review_test_user_id,
            "place_id": self.review_test_place_id
        }
        resp = self.session.post(REVIEW_ENDPOINT, json=payload)
        print("Réponse:", resp.text)
        self.assertIn(resp.status_code, [200, 201])
        data = resp.json()
        self.__class__.review_id = data.get("id")
        self.assertTrue(self.review_id, "Création review échouée")

    def test_34_create_review_invalid_user(self):
        """Test 2: Création d'une review avec un utilisateur inexistant"""
        payload = {
            "text": "Invalid user review",
            "rating": 4,
            "user_id": "invalid_user_id",
            "place_id": self.review_test_place_id
        }
        resp = self.session.post(REVIEW_ENDPOINT, json=payload)
        print("Réponse:", resp.text)
        self.assertIn(resp.status_code, [400, 404])
        self.assertIn("error", resp.text)

    def test_35_create_review_invalid_place(self):
        """Test 3: Création d'une review avec place inexistant"""
        payload = {
            "text": "Invalid place review",
            "rating": 3,
            "user_id": self.review_test_user_id,
            "place_id": "invalid_place_id"
        }
        resp = self.session.post(REVIEW_ENDPOINT, json=payload)
        print("Réponse:", resp.text)
        self.assertIn(resp.status_code, [400, 404])
        self.assertIn("error", resp.text)

    def test_36_create_review_invalid_rating(self):
        """Test 4: Création d'une review avec note invalide"""
        payload = {
            "text": "Invalid rating review",
            "rating": 10,
            "user_id": self.review_test_user_id,
            "place_id": self.review_test_place_id
        }
        resp = self.session.post(REVIEW_ENDPOINT, json=payload)
        print("Réponse:", resp.text)
        self.assertEqual(resp.status_code, 400, "Le rating=10 devrait être invalide")
        self.assertIn("error", resp.text)

    def test_37_get_all_reviews(self):
        """Test 5: Récupération de toutes les reviews"""
        resp = self.session.get(REVIEW_ENDPOINT)
        print("Réponse:", resp.text)
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.json(), list, "La réponse doit être une liste")

    def test_38_get_review_by_id(self):
        """Test 6: Récupération d'une review par ID"""
        self.assertTrue(self.review_id, "Pas de review_id créé")
        url = f"{REVIEW_ENDPOINT}/{self.review_id}"
        resp = self.session.get(url)
        print("Réponse:", resp.text)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data.get("id"), self.review_id)
        self.assertEqual(data.get("text"), "Great place to stay!")
        self.assertEqual(data.get("rating"), 5)

    def test_39_get_reviews_by_place(self):
        """Test 7: Récupération de toutes les reviews d'un place par son ID"""
        url = f"{PLACE_ENDPOINT}/{self.review_test_place_id}/reviews"
        resp = self.session.get(url)
        print("Réponse:", resp.text)
        self.assertEqual(resp.status_code, 200)
        reviews_for_place = resp.json()
        self.assertIsInstance(reviews_for_place, list)
        # Vérifier la presence de self.review_id
        found = any(r.get("id") == self.review_id for r in reviews_for_place)
        self.assertTrue(found, "La review n'est pas trouvée dans la liste des reviews du place")

    def test_40_update_review(self):
        """Test 8: Mise à jour d'une review"""
        self.assertTrue(self.review_id, "Pas de review_id")
        url = f"{REVIEW_ENDPOINT}/{self.review_id}"
        payload = {"text": "Updated review text", "rating": 4}
        resp = self.session.put(url, json=payload)
        print("Réponse:", resp.text)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data.get("text"), "Updated review text")
        self.assertEqual(data.get("rating"), 4)

    def test_41_update_review_invalid_rating(self):
        """Test 9: Mise à jour avec note invalide"""
        self.assertTrue(self.review_id, "Pas de review_id")
        url = f"{REVIEW_ENDPOINT}/{self.review_id}"
        payload = {"rating": 0}
        resp = self.session.put(url, json=payload)
        print("Réponse:", resp.text)
        self.assertEqual(resp.status_code, 400, "rating=0 devrait être invalide")
        self.assertIn("error", resp.text)

    def test_42_update_review_invalid_id(self):
        """Test 10: Mise à jour avec ID inexistant"""
        url = f"{REVIEW_ENDPOINT}/invalid_id_12345"
        payload = {"text": "This should not work", "rating": 2}
        resp = self.session.put(url, json=payload)
        print("Réponse:", resp.text)
        self.assertIn(resp.status_code, [400, 404])
        self.assertTrue("not found" in resp.text or "error" in resp.text)

    def test_43_delete_review(self):
        """Test 11: Suppression d'une review"""
        self.assertTrue(self.review_id, "Pas de review_id")
        url = f"{REVIEW_ENDPOINT}/{self.review_id}"
        resp = self.session.delete(url)
        print("Réponse:", resp.text)
        # Le script Bash vérifie: if [[ $DELETE_RESPONSE == *\"successfully\"* ]]
        # On suppose code 200, et message success
        self.assertEqual(resp.status_code, 200, "Le code devrait être 200 pour DELETE review")
        self.assertTrue("success" in resp.text or "successfully" in resp.text,
                        "Pas de message de succès dans la réponse")

    def test_44_delete_review_invalid_id(self):
        """Test 12: Suppression avec ID inexistant"""
        url = f"{REVIEW_ENDPOINT}/invalid_id_12345"
        resp = self.session.delete(url)
        print("Réponse:", resp.text)
        # Le script Bash accepte "not found" ou "error"
        # On suppose code 404 ou 405
        self.assertIn(resp.status_code, [404, 405])
        self.assertTrue("not found" in resp.text or "error" in resp.text)

    def test_45_verify_review_deleted(self):
        """Test 13: Vérification que la review a bien été supprimée"""
        # On refait un GET sur la review
        self.assertTrue(self.review_id, "Pas de review_id")
        url = f"{REVIEW_ENDPOINT}/{self.review_id}"
        resp = self.session.get(url)
        print("Réponse:", resp.text)
        self.assertIn(resp.status_code, [400, 404],
                      "Le GET sur une review supprimée devrait renvoyer 404 (ou 400)")
        self.assertTrue("not found" in resp.text or "error" in resp.text)

    def test_46_create_new_review_for_place_details(self):
        """Test 14: Création d'une nouvelle review et vérification dans les détails du place"""
        # On recrée une review pour le place (review_test_place_id)
        payload = {
            "text": "Another great review",
            "rating": 5,
            "user_id": self.review_test_user_id,
            "place_id": self.review_test_place_id
        }
        resp = self.session.post(REVIEW_ENDPOINT, json=payload)
        print("Réponse (new review):", resp.text)
        self.assertIn(resp.status_code, [200, 201])
        new_review_id = resp.json().get("id")
        self.assertTrue(new_review_id, "Échec de la création d'une nouvelle review")

        # Vérif dans les détails du place
        url = f"{PLACE_ENDPOINT}/{self.review_test_place_id}"
        place_resp = self.session.get(url)
        print("Réponse détails place:", place_resp.text)
        self.assertEqual(place_resp.status_code, 200)
        place_data = place_resp.json()
        has_reviews = "reviews" in place_data
        self.assertTrue(has_reviews, "Le place ne contient pas de champ 'reviews'")

        reviews_list = place_data["reviews"]
        found = any(r.get("id") == new_review_id for r in reviews_list)
        self.assertTrue(found, "La nouvelle review n'apparaît pas dans les détails du place")


if __name__ == "__main__":
    # Lance tous les tests
    unittest.main(verbosity=2)
