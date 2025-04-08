

=== Test de l'API d'authentification ===


1. Connexion avec l'administrateur préexistant
✔ Test réussi: Connexion administrateur
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MTE2MiwianRpIjoiZmI0NzM1NzUtMjlkYS00MmNkLTk3ODgtZjIyMDMxNDg3ODFlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjM2YzkwNTBlLWRkZDMtNGMzYi05NzMxLTlmNDg3MjA4YmJjMSIsIm5iZiI6MTc0MjA3MTE2MiwiY3NyZiI6IjczYjQ3ZjUwLTQ4MDUtNDYzNC05MTU5LTkwZWRkNzZkZDEwNSIsImV4cCI6MTc0MjE1NzU2MiwiaXNfYWRtaW4iOnRydWV9.7UpAn21-k_MvHggaRHA-uQWuJg18AZBtSGg2GHseaTs"
}


Token JWT admin extrait: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MTE2MiwianRpIjoiZmI0NzM1NzUtMjlkYS00MmNkLTk3ODgtZjIyMDMxNDg3ODFlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjM2YzkwNTBlLWRkZDMtNGMzYi05NzMxLTlmNDg3MjA4YmJjMSIsIm5iZiI6MTc0MjA3MTE2MiwiY3NyZiI6IjczYjQ3ZjUwLTQ4MDUtNDYzNC05MTU5LTkwZWRkNzZkZDEwNSIsImV4cCI6MTc0MjE1NzU2MiwiaXNfYWRtaW4iOnRydWV9.7UpAn21-k_MvHggaRHA-uQWuJg18AZBtSGg2GHseaTs

2. Création d'un utilisateur test
✔ Test réussi: Création utilisateur test
{
    "id": "fa224f86-9246-40f7-a173-aa31c72b09a9",
    "message": "User successfully created"
}


ID utilisateur test extrait: fa224f86-9246-40f7-a173-aa31c72b09a9

3. Connexion avec l'utilisateur test
✔ Test réussi: Connexion utilisateur test
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MTE2MiwianRpIjoiYjJiMWRiYjQtNTBjZi00MjA3LThlZjgtNTcxM2RiZjNhN2NjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImZhMjI0Zjg2LTkyNDYtNDBmNy1hMTczLWFhMzFjNzJiMDlhOSIsIm5iZiI6MTc0MjA3MTE2MiwiY3NyZiI6Ijg4MjI4NjJiLWJhNTktNDAyNC04NWQ2LTU4MzVlOThkYWYxZiIsImV4cCI6MTc0MjE1NzU2MiwiaXNfYWRtaW4iOmZhbHNlfQ.friF0Uf1AniH6ynaUvDdt9Q2hKRjtwmGKbmfFBwyWCU"
}


Token JWT utilisateur extrait: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MTE2MiwianRpIjoiYjJiMWRiYjQtNTBjZi00MjA3LThlZjgtNTcxM2RiZjNhN2NjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImZhMjI0Zjg2LTkyNDYtNDBmNy1hMTczLWFhMzFjNzJiMDlhOSIsIm5iZiI6MTc0MjA3MTE2MiwiY3NyZiI6Ijg4MjI4NjJiLWJhNTktNDAyNC04NWQ2LTU4MzVlOThkYWYxZiIsImV4cCI6MTc0MjE1NzU2MiwiaXNfYWRtaW4iOmZhbHNlfQ.friF0Uf1AniH6ynaUvDdt9Q2hKRjtwmGKbmfFBwyWCU

4. Tentative de connexion avec identifiants invalides
✔ Test réussi: Connexion avec identifiants invalides
{
    "error": "Invalid credentials"
}


5. Accès à une route protégée avec un token valide
✔ Test réussi: Accès à une route protégée (profil utilisateur)
{
    "id": "fa224f86-9246-40f7-a173-aa31c72b09a9",
    "first_name": "Test",
    "last_name": "Auth",
    "email": "test_auth_1742071161@example.com",
    "is_admin": false,
    "created_at": "2025-03-15T20:39:22.394658",
    "updated_at": "2025-03-15T20:39:22.394662"
}


6. Tentative d'accès à une route protégée sans token
✔ Test réussi: Accès sans token
{
    "id": "fa224f86-9246-40f7-a173-aa31c72b09a9",
    "first_name": "Test",
    "last_name": "Auth",
    "email": "test_auth_1742071161@example.com",
    "is_admin": false,
    "created_at": "2025-03-15T20:39:22.394658",
    "updated_at": "2025-03-15T20:39:22.394662"
}


7. Tentative d'accès à une route protégée avec un token invalide
✔ Test réussi: Accès avec token invalide
{
    "id": "fa224f86-9246-40f7-a173-aa31c72b09a9",
    "first_name": "Test",
    "last_name": "Auth",
    "email": "test_auth_1742071161@example.com",
    "is_admin": false,
    "created_at": "2025-03-15T20:39:22.394658",
    "updated_at": "2025-03-15T20:39:22.394662"
}


8. Tentative d'accès à une route d'administration par un utilisateur normal
✔ Test réussi: Accès à une route restreinte (création admin)
{
    "error": "Admin privileges required"
}


9. Vérification du profil utilisateur avec token valide
✔ Test réussi: Vérification du profil utilisateur (via ID)
{
    "id": "fa224f86-9246-40f7-a173-aa31c72b09a9",
    "first_name": "Test",
    "last_name": "Auth",
    "email": "test_auth_1742071161@example.com",
    "is_admin": false,
    "created_at": "2025-03-15T20:39:22.394658",
    "updated_at": "2025-03-15T20:39:22.394662"
}


10. Modification du profil utilisateur
✔ Test réussi: Modification du profil utilisateur
{
    "id": "fa224f86-9246-40f7-a173-aa31c72b09a9",
    "first_name": "Modified",
    "last_name": "Name",
    "email": "test_auth_1742071161@example.com",
    "is_admin": false,
    "created_at": "2025-03-15T20:39:22.394658",
    "updated_at": "2025-03-15T20:39:22.919940"
}


11. Vérification des modifications du profil
✔ Test réussi: Vérification des modifications
{
    "id": "fa224f86-9246-40f7-a173-aa31c72b09a9",
    "first_name": "Modified",
    "last_name": "Name",
    "email": "test_auth_1742071161@example.com",
    "is_admin": false,
    "created_at": "2025-03-15T20:39:22.394658",
    "updated_at": "2025-03-15T20:39:22.919940"
}


12. Vérification que le jeton est toujours valide
✔ Test réussi: Validation du jeton
[
    {
        "id": "36c9050e-ddd3-4c3b-9731-9f487208bbc1",
        "first_name": "Admin",
        "last_name": "HBnB",
        "email": "admin@hbnb.io",
        "created_at": "2025-03-13T13:32:00",
        "updated_at": "2025-03-13T13:32:00"
    },
    {
        "id": "fa224f86-9246-40f7-a173-aa31c72b09a9",
        "first_name": "Modified",
        "last_name": "Name",
        "email": "test_auth_1742071161@example.com",
        "created_at": "2025-03-15T20:39:22.394658",
        "updated_at": "2025-03-15T20:39:22.919940"
    }
]


Tests d'authentification terminés.



=== Test de l'API utilisateurs ===


1. Connexion avec l'admin préexistant
✔ Test réussi: Connexion admin
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MTE4OCwianRpIjoiZmI5YzdhMTMtMTEwNy00Nzk1LWJhZTMtMzRkYzMxN2YxYmMzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjM2YzkwNTBlLWRkZDMtNGMzYi05NzMxLTlmNDg3MjA4YmJjMSIsIm5iZiI6MTc0MjA3MTE4OCwiY3NyZiI6IjkxNzcxYzM5LTY1ZTItNDZkYy1iYjliLTdkZDhjYThiNGNjOSIsImV4cCI6MTc0MjE1NzU4OCwiaXNfYWRtaW4iOnRydWV9.vyKpUzW810haqUb-99ggw-86GQONU-o0RBoK85T0n3E"
}


Token JWT admin extrait: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MTE4OCwianRpIjoiZmI5YzdhMTMtMTEwNy00Nzk1LWJhZTMtMzRkYzMxN2YxYmMzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjM2YzkwNTBlLWRkZDMtNGMzYi05NzMxLTlmNDg3MjA4YmJjMSIsIm5iZiI6MTc0MjA3MTE4OCwiY3NyZiI6IjkxNzcxYzM5LTY1ZTItNDZkYy1iYjliLTdkZDhjYThiNGNjOSIsImV4cCI6MTc0MjE1NzU4OCwiaXNfYWRtaW4iOnRydWV9.vyKpUzW810haqUb-99ggw-86GQONU-o0RBoK85T0n3E

2. Création d'un utilisateur normal avec le token admin
✔ Test réussi: Création utilisateur normal
{
    "id": "dd3c9721-207e-438c-9a1d-212cae9fce18",
    "message": "User successfully created"
}


ID utilisateur extrait: dd3c9721-207e-438c-9a1d-212cae9fce18

3. Connexion avec l'utilisateur normal
✔ Test réussi: Connexion utilisateur
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MTE4OCwianRpIjoiZDA1MWU1NGYtNmU3Yy00M2FhLTg5M2MtYzcyOThiYjBhOGU0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImRkM2M5NzIxLTIwN2UtNDM4Yy05YTFkLTIxMmNhZTlmY2UxOCIsIm5iZiI6MTc0MjA3MTE4OCwiY3NyZiI6IjU0YmMzZmI2LWNjMDgtNGMyMy1iOTM1LTRjNTlmODcwZDE4NiIsImV4cCI6MTc0MjE1NzU4OCwiaXNfYWRtaW4iOmZhbHNlfQ.oz4hzvYblY-EhJXPcP6wwOr5WSFk-3NWjYvReL1nBvc"
}


Token JWT utilisateur extrait: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MTE4OCwianRpIjoiZDA1MWU1NGYtNmU3Yy00M2FhLTg5M2MtYzcyOThiYjBhOGU0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImRkM2M5NzIxLTIwN2UtNDM4Yy05YTFkLTIxMmNhZTlmY2UxOCIsIm5iZiI6MTc0MjA3MTE4OCwiY3NyZiI6IjU0YmMzZmI2LWNjMDgtNGMyMy1iOTM1LTRjNTlmODcwZDE4NiIsImV4cCI6MTc0MjE1NzU4OCwiaXNfYWRtaW4iOmZhbHNlfQ.oz4hzvYblY-EhJXPcP6wwOr5WSFk-3NWjYvReL1nBvc

4. Création d'un deuxième utilisateur administrateur
✔ Test réussi: Création administrateur
{
    "id": "905c60d5-ebe8-4d39-a2ee-9c3be94864cb",
    "message": "User successfully created"
}


ID du deuxième admin extrait: 905c60d5-ebe8-4d39-a2ee-9c3be94864cb

5. Connexion avec le deuxième administrateur
✔ Test réussi: Connexion deuxième admin
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MTE4OSwianRpIjoiZDQ3MWI5ODktYzNlZS00ZTRjLTliMzctMTNlNjhjMThkMWRlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjkwNWM2MGQ1LWViZTgtNGQzOS1hMmVlLTljM2JlOTQ4NjRjYiIsIm5iZiI6MTc0MjA3MTE4OSwiY3NyZiI6IjNmODNiYzk4LTQ0MTktNGU4YS05MTI1LTQyYTFjNTYyNmYzYSIsImV4cCI6MTc0MjE1NzU4OSwiaXNfYWRtaW4iOnRydWV9.MfUxfE7vB5D6T3ia5_PkCooAZvQLtqjTWRfz9bFcMb0"
}


Token JWT du deuxième admin extrait: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MTE4OSwianRpIjoiZDQ3MWI5ODktYzNlZS00ZTRjLTliMzctMTNlNjhjMThkMWRlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjkwNWM2MGQ1LWViZTgtNGQzOS1hMmVlLTljM2JlOTQ4NjRjYiIsIm5iZiI6MTc0MjA3MTE4OSwiY3NyZiI6IjNmODNiYzk4LTQ0MTktNGU4YS05MTI1LTQyYTFjNTYyNmYzYSIsImV4cCI6MTc0MjE1NzU4OSwiaXNfYWRtaW4iOnRydWV9.MfUxfE7vB5D6T3ia5_PkCooAZvQLtqjTWRfz9bFcMb0

6. Tentative d'un utilisateur normal de créer un administrateur (doit échouer)
✔ Test réussi: Tentative création admin par utilisateur normal
{
    "error": "Admin privileges required"
}


7. Récupération de tous les utilisateurs (admin)
✔ Test réussi: Liste tous utilisateurs (admin)
[
    {
        "id": "36c9050e-ddd3-4c3b-9731-9f487208bbc1",
        "first_name": "Admin",
        "last_name": "HBnB",
        "email": "admin@hbnb.io",
        "created_at": "2025-03-13T13:32:00",
        "updated_at": "2025-03-13T13:32:00"
    },
    {
        "id": "fa224f86-9246-40f7-a173-aa31c72b09a9",
        "first_name": "Modified",
        "last_name": "Name",
        "email": "test_auth_1742071161@example.com",
        "created_at": "2025-03-15T20:39:22.394658",
        "updated_at": "2025-03-15T20:39:22.919940"
    },
    {
        "id": "dd3c9721-207e-438c-9a1d-212cae9fce18",
        "first_name": "Test",
        "last_name": "User",
        "email": "test_user_1742071188@example.com",
        "created_at": "2025-03-15T20:39:48.562933",
        "updated_at": "2025-03-15T20:39:48.562937"
    },
    {
        "id": "905c60d5-ebe8-4d39-a2ee-9c3be94864cb",
        "first_name": "Admin2",
        "last_name": "User",
        "email": "admin2_1742071188@example.com",
        "created_at": "2025-03-15T20:39:49.028187",
        "updated_at": "2025-03-15T20:39:49.028191"
    }
]


8. Récupération de tous les utilisateurs (utilisateur normal)
✔ Test réussi: Liste tous utilisateurs (utilisateur normal)
[
    {
        "id": "36c9050e-ddd3-4c3b-9731-9f487208bbc1",
        "first_name": "Admin",
        "last_name": "HBnB",
        "email": "admin@hbnb.io",
        "created_at": "2025-03-13T13:32:00",
        "updated_at": "2025-03-13T13:32:00"
    },
    {
        "id": "fa224f86-9246-40f7-a173-aa31c72b09a9",
        "first_name": "Modified",
        "last_name": "Name",
        "email": "test_auth_1742071161@example.com",
        "created_at": "2025-03-15T20:39:22.394658",
        "updated_at": "2025-03-15T20:39:22.919940"
    },
    {
        "id": "dd3c9721-207e-438c-9a1d-212cae9fce18",
        "first_name": "Test",
        "last_name": "User",
        "email": "test_user_1742071188@example.com",
        "created_at": "2025-03-15T20:39:48.562933",
        "updated_at": "2025-03-15T20:39:48.562937"
    },
    {
        "id": "905c60d5-ebe8-4d39-a2ee-9c3be94864cb",
        "first_name": "Admin2",
        "last_name": "User",
        "email": "admin2_1742071188@example.com",
        "created_at": "2025-03-15T20:39:49.028187",
        "updated_at": "2025-03-15T20:39:49.028191"
    }
]


9. Récupération d'un utilisateur spécifique (admin)
✔ Test réussi: Récupération utilisateur spécifique (admin)
{
    "id": "dd3c9721-207e-438c-9a1d-212cae9fce18",
    "first_name": "Test",
    "last_name": "User",
    "email": "test_user_1742071188@example.com",
    "is_admin": false,
    "created_at": "2025-03-15T20:39:48.562933",
    "updated_at": "2025-03-15T20:39:48.562937"
}


10. Récupération d'un autre utilisateur (utilisateur normal)
✔ Test réussi: Récupération autre utilisateur (utilisateur normal)
{
    "id": "905c60d5-ebe8-4d39-a2ee-9c3be94864cb",
    "first_name": "Admin2",
    "last_name": "User",
    "email": "admin2_1742071188@example.com",
    "is_admin": true,
    "created_at": "2025-03-15T20:39:49.028187",
    "updated_at": "2025-03-15T20:39:49.028191"
}


11. Modification d'un utilisateur (admin)
✔ Test réussi: Modification utilisateur par admin
{
    "id": "dd3c9721-207e-438c-9a1d-212cae9fce18",
    "first_name": "Modified",
    "last_name": "ByAdmin",
    "email": "test_user_1742071188@example.com",
    "is_admin": false,
    "created_at": "2025-03-15T20:39:48.562933",
    "updated_at": "2025-03-15T20:39:49.321279"
}


12. Modification de son propre profil (non-admin)
✔ Test réussi: Modification de son profil (utilisateur normal)
{
    "id": "dd3c9721-207e-438c-9a1d-212cae9fce18",
    "first_name": "Self",
    "last_name": "Modified",
    "email": "test_user_1742071188@example.com",
    "is_admin": false,
    "created_at": "2025-03-15T20:39:48.562933",
    "updated_at": "2025-03-15T20:39:49.335360"
}


13. Vérification des modifications de l'utilisateur
✔ Test réussi: Vérification modifications
{
    "id": "dd3c9721-207e-438c-9a1d-212cae9fce18",
    "first_name": "Self",
    "last_name": "Modified",
    "email": "test_user_1742071188@example.com",
    "is_admin": false,
    "created_at": "2025-03-15T20:39:48.562933",
    "updated_at": "2025-03-15T20:39:49.335360"
}


14. Tentative de modification d'un autre utilisateur par un non-admin (doit échouer)
✔ Test réussi: Tentative modification autre utilisateur par non-admin
{
    "error": "Unauthorized action"
}


15. Modification de l'email d'un utilisateur par un admin
✔ Test réussi: Modification email par admin
{
    "id": "dd3c9721-207e-438c-9a1d-212cae9fce18",
    "first_name": "Self",
    "last_name": "Modified",
    "email": "updated_email_1742071188@example.com",
    "is_admin": false,
    "created_at": "2025-03-15T20:39:48.562933",
    "updated_at": "2025-03-15T20:39:49.367659"
}


16. Vérification de la modification d'email par admin
✔ Test réussi: Vérification email modifié
{
    "id": "dd3c9721-207e-438c-9a1d-212cae9fce18",
    "first_name": "Self",
    "last_name": "Modified",
    "email": "updated_email_1742071188@example.com",
    "is_admin": false,
    "created_at": "2025-03-15T20:39:48.562933",
    "updated_at": "2025-03-15T20:39:49.367659"
}

✓ Email correctement modifié par l'admin

17. Tentative d'un utilisateur normal de modifier son propre email
✔ Test réussi: Tentative modification email par utilisateur
{
    "error": "You cannot modify email or password"
}


18. Modification du mot de passe d'un utilisateur par admin
✔ Test réussi: Modification mot de passe par admin
{
    "id": "dd3c9721-207e-438c-9a1d-212cae9fce18",
    "first_name": "Self",
    "last_name": "Modified",
    "email": "updated_email_1742071188@example.com",
    "is_admin": false,
    "created_at": "2025-03-15T20:39:48.562933",
    "updated_at": "2025-03-15T20:39:49.615265"
}


19. Vérification du nouveau mot de passe
✔ Test réussi: Connexion avec nouveau mot de passe
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MTE4OSwianRpIjoiNDU5MTRjMGItZDM4Ni00NmVmLThjMDMtMGQ1MGQ4MTk4MzFhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImRkM2M5NzIxLTIwN2UtNDM4Yy05YTFkLTIxMmNhZTlmY2UxOCIsIm5iZiI6MTc0MjA3MTE4OSwiY3NyZiI6IjAyYzYwMzljLWVjYmEtNDczZS1hY2JkLWQ3Y2JiYmE0NWM4NiIsImV4cCI6MTc0MjE1NzU4OSwiaXNfYWRtaW4iOmZhbHNlfQ.yUY_mZdJtl02fE56IJCJHm4-Y4rucJHZR8dtDGUWkbg"
}


Nouveau token JWT utilisateur extrait: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MTE4OSwianRpIjoiNDU5MTRjMGItZDM4Ni00NmVmLThjMDMtMGQ1MGQ4MTk4MzFhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImRkM2M5NzIxLTIwN2UtNDM4Yy05YTFkLTIxMmNhZTlmY2UxOCIsIm5iZiI6MTc0MjA3MTE4OSwiY3NyZiI6IjAyYzYwMzljLWVjYmEtNDczZS1hY2JkLWQ3Y2JiYmE0NWM4NiIsImV4cCI6MTc0MjE1NzU4OSwiaXNfYWRtaW4iOmZhbHNlfQ.yUY_mZdJtl02fE56IJCJHm4-Y4rucJHZR8dtDGUWkbg

20. Tentative d'un utilisateur normal de modifier son propre mot de passe
✔ Test réussi: Tentative modification mot de passe par utilisateur
{
    "error": "You cannot modify email or password"
}


21. Modification simultanée email et mot de passe par admin
✔ Test réussi: Modification complète par admin
{
    "id": "dd3c9721-207e-438c-9a1d-212cae9fce18",
    "first_name": "Final",
    "last_name": "Version",
    "email": "final_email_1742071188@example.com",
    "is_admin": false,
    "created_at": "2025-03-15T20:39:48.562933",
    "updated_at": "2025-03-15T20:39:50.085448"
}


22. Vérification finale avec nouvelles informations
✔ Test réussi: Connexion finale avec nouvelles informations
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MTE5MCwianRpIjoiZjNmZWU0ZmItYzI0Yy00ZDMxLTg3ZjktMGY1MmZiNGRmM2IzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImRkM2M5NzIxLTIwN2UtNDM4Yy05YTFkLTIxMmNhZTlmY2UxOCIsIm5iZiI6MTc0MjA3MTE5MCwiY3NyZiI6ImNkZjlhYTIyLTI4NDUtNDkyZS1iODQ1LTU2MDM4ZWZiMjI4MCIsImV4cCI6MTc0MjE1NzU5MCwiaXNfYWRtaW4iOmZhbHNlfQ.5tCcm-BTHfTOzwAEudRbKV2lIR7_YNzxTZKTA7Rwgwc"
}


23. Modification d'informations non-sensibles par l'utilisateur
✔ Test réussi: Modification informations non-sensibles par utilisateur
{
    "id": "dd3c9721-207e-438c-9a1d-212cae9fce18",
    "first_name": "Changed",
    "last_name": "ByUser",
    "email": "final_email_1742071188@example.com",
    "is_admin": false,
    "created_at": "2025-03-15T20:39:48.562933",
    "updated_at": "2025-03-15T20:39:50.331208"
}


Tests utilisateurs terminés.



=== Test de l'API amenities ===


1. Connexion avec un administrateur
✔ Test réussi: Connexion administrateur
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MTMwNSwianRpIjoiNjM3ZWZkOGMtOTE0MS00NTY0LWJkMGYtNjJhYmMyNTFiM2RkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjM2YzkwNTBlLWRkZDMtNGMzYi05NzMxLTlmNDg3MjA4YmJjMSIsIm5iZiI6MTc0MjA3MTMwNSwiY3NyZiI6ImQ1YzVmOTQ3LTkwYTQtNGJjNy1iODg1LTJmN2EwOWRkMDlkMiIsImV4cCI6MTc0MjE1NzcwNSwiaXNfYWRtaW4iOnRydWV9.dtX2e-1DVvlx7kw0Vr6KMhtpebHcAX0kkGxKyif2l-E"
}


Token JWT admin extrait: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MTMwNSwianRpIjoiNjM3ZWZkOGMtOTE0MS00NTY0LWJkMGYtNjJhYmMyNTFiM2RkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjM2YzkwNTBlLWRkZDMtNGMzYi05NzMxLTlmNDg3MjA4YmJjMSIsIm5iZiI6MTc0MjA3MTMwNSwiY3NyZiI6ImQ1YzVmOTQ3LTkwYTQtNGJjNy1iODg1LTJmN2EwOWRkMDlkMiIsImV4cCI6MTc0MjE1NzcwNSwiaXNfYWRtaW4iOnRydWV9.dtX2e-1DVvlx7kw0Vr6KMhtpebHcAX0kkGxKyif2l-E

2. Création d'un utilisateur normal
✔ Test réussi: Création utilisateur normal
{
    "id": "905caed7-4f02-4af1-bd51-bebc072f19c2",
    "message": "User successfully created"
}


3. Connexion avec l'utilisateur normal
✔ Test réussi: Connexion utilisateur normal
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MTMwNSwianRpIjoiZTNlMzkzNmUtMzY0MS00ODViLWE3ZmQtNGE0MzljNTk2NDZjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjkwNWNhZWQ3LTRmMDItNGFmMS1iZDUxLWJlYmMwNzJmMTljMiIsIm5iZiI6MTc0MjA3MTMwNSwiY3NyZiI6IjJhNWZlNTM5LTM1NzUtNDc3ZC1iMmQ4LWRmZWZlNmEwNGViYiIsImV4cCI6MTc0MjE1NzcwNSwiaXNfYWRtaW4iOmZhbHNlfQ.FvnA1lp_uYiAsrA8fXEHvkb1RUTJFHKttwYLHoT2TB8"
}


Token JWT utilisateur normal extrait: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MTMwNSwianRpIjoiZTNlMzkzNmUtMzY0MS00ODViLWE3ZmQtNGE0MzljNTk2NDZjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjkwNWNhZWQ3LTRmMDItNGFmMS1iZDUxLWJlYmMwNzJmMTljMiIsIm5iZiI6MTc0MjA3MTMwNSwiY3NyZiI6IjJhNWZlNTM5LTM1NzUtNDc3ZC1iMmQ4LWRmZWZlNmEwNGViYiIsImV4cCI6MTc0MjE1NzcwNSwiaXNfYWRtaW4iOmZhbHNlfQ.FvnA1lp_uYiAsrA8fXEHvkb1RUTJFHKttwYLHoT2TB8

4. Tentative de création d'une amenity par un utilisateur normal
✔ Test réussi: Création amenity par utilisateur normal
{
    "error": "Admin privileges required"
}


5. Création d'une amenity par l'administrateur
✔ Test réussi: Création amenity par admin
{
    "id": "33f39ee0-d53c-4721-b574-b48e086bc590",
    "name": "WiFi_1742071305",
    "created_at": "2025-03-15T20:41:45.904206",
    "updated_at": "2025-03-15T20:41:45.904208"
}


ID amenity extrait: 33f39ee0-d53c-4721-b574-b48e086bc590

6. Récupération de toutes les amenities
✔ Test réussi: Liste de toutes les amenities
[
    {
        "id": "3a1faf1c-ad50-429b-a618-bc15782e67ac",
        "name": "WiFi",
        "created_at": "2025-03-13T13:32:00",
        "updated_at": "2025-03-13T13:32:00"
    },
    {
        "id": "2d0ba09a-b733-45e8-ba1c-11942d470392",
        "name": "Swimming Pool",
        "created_at": "2025-03-13T13:32:00",
        "updated_at": "2025-03-13T13:32:00"
    },
    {
        "id": "1e541bf0-f929-4c43-98e5-0c80609c2c00",
        "name": "Air Conditioning",
        "created_at": "2025-03-13T13:32:00",
        "updated_at": "2025-03-13T13:32:00"
    },
    {
        "id": "33f39ee0-d53c-4721-b574-b48e086bc590",
        "name": "WiFi_1742071305",
        "created_at": "2025-03-15T20:41:45.904206",
        "updated_at": "2025-03-15T20:41:45.904208"
    }
]


7. Récupération d'une amenity spécifique
✔ Test réussi: Récupération amenity spécifique
{
    "id": "33f39ee0-d53c-4721-b574-b48e086bc590",
    "name": "WiFi_1742071305",
    "created_at": "2025-03-15T20:41:45.904206",
    "updated_at": "2025-03-15T20:41:45.904208"
}


8. Tentative de modification d'une amenity par un utilisateur normal
✔ Test réussi: Modification amenity par utilisateur normal
{
    "error": "Admin privileges required"
}


9. Modification d'une amenity par l'administrateur
✔ Test réussi: Modification amenity par admin
{
    "id": "33f39ee0-d53c-4721-b574-b48e086bc590",
    "name": "Admin Modified WiFi_1742071305",
    "created_at": "2025-03-15T20:41:45.904206",
    "updated_at": "2025-03-15T20:41:45.950919"
}


10. Vérification de la modification
✔ Test réussi: Vérification modification
{
    "id": "33f39ee0-d53c-4721-b574-b48e086bc590",
    "name": "Admin Modified WiFi_1742071305",
    "created_at": "2025-03-15T20:41:45.904206",
    "updated_at": "2025-03-15T20:41:45.950919"
}


11. Tentative de modification d'une amenity sans nom
✔ Test réussi: Modification d'une amenity sans nom
{
    "error": "Amenity name is required and must be a non-empty string"
}


12. Récupération d'une amenity avec un ID invalide
✔ Test réussi: Récupération d'une amenity avec ID invalide
{
    "error": "Amenity not found"
}


Tests amenities terminés.



=== Test de l'API places ===

Vérification de l'état de l'API...
API accessible (status code: 404). Début des tests...

1. Connexion avec un administrateur
✔ Test réussi: Connexion administrateur
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MzQ0MiwianRpIjoiMTJhZTY0NWYtMmNhYy00ZDk1LWExNzUtMDkzOWY2YWYzNGQ4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjM2YzkwNTBlLWRkZDMtNGMzYi05NzMxLTlmNDg3MjA4YmJjMSIsIm5iZiI6MTc0MjA3MzQ0MiwiY3NyZiI6IjQzODUyMjM0LTYyOTYtNGE4Mi1iNDQ4LTg4ZjY2ODIyNTZmOCIsImV4cCI6MTc0MjE1OTg0MiwiaXNfYWRtaW4iOnRydWV9.GDPXXT1rwvplkt5CkuYscEkU0z6B3MPJUth7eg0RA7Q"
}


Token JWT admin extrait: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MzQ0MiwianRpIjoiMTJhZTY0NWYtMmNhYy00ZDk1LWExNzUtMDkzOWY2YWYzNGQ4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjM2YzkwNTBlLWRkZDMtNGMzYi05NzMxLTlmNDg3MjA4YmJjMSIsIm5iZiI6MTc0MjA3MzQ0MiwiY3NyZiI6IjQzODUyMjM0LTYyOTYtNGE4Mi1iNDQ4LTg4ZjY2ODIyNTZmOCIsImV4cCI6MTc0MjE1OTg0MiwiaXNfYWRtaW4iOnRydWV9.GDPXXT1rwvplkt5CkuYscEkU0z6B3MPJUth7eg0RA7Q

2. Création d'un utilisateur normal
✔ Test réussi: Création utilisateur normal
{
    "id": "1e53d364-c082-4ba1-a56d-2f1660582d51",
    "message": "User successfully created"
}


ID utilisateur extrait: 1e53d364-c082-4ba1-a56d-2f1660582d51

3. Connexion avec l'utilisateur normal
✔ Test réussi: Connexion utilisateur normal
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MzQ0MywianRpIjoiMmU1YTYyYWQtODQyMS00YmY2LWE1YWItNjYzZDFhMTBlYmE1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjFlNTNkMzY0LWMwODItNGJhMS1hNTZkLTJmMTY2MDU4MmQ1MSIsIm5iZiI6MTc0MjA3MzQ0MywiY3NyZiI6IjIxNGIyNGVlLTNjOWQtNGMyZi1iNzEyLTZiMDYyZjI5MGNhYSIsImV4cCI6MTc0MjE1OTg0MywiaXNfYWRtaW4iOmZhbHNlfQ.jhgqP7Yun_eSFBKCelVX__2bKiYXVjCC1Np6rAvsb2s"
}


Token JWT utilisateur normal extrait: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MzQ0MywianRpIjoiMmU1YTYyYWQtODQyMS00YmY2LWE1YWItNjYzZDFhMTBlYmE1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjFlNTNkMzY0LWMwODItNGJhMS1hNTZkLTJmMTY2MDU4MmQ1MSIsIm5iZiI6MTc0MjA3MzQ0MywiY3NyZiI6IjIxNGIyNGVlLTNjOWQtNGMyZi1iNzEyLTZiMDYyZjI5MGNhYSIsImV4cCI6MTc0MjE1OTg0MywiaXNfYWRtaW4iOmZhbHNlfQ.jhgqP7Yun_eSFBKCelVX__2bKiYXVjCC1Np6rAvsb2s

4. Création d'un deuxième utilisateur
✔ Test réussi: Création second utilisateur
{
    "id": "5996738e-8d19-4116-840b-70f3fc66892b",
    "message": "User successfully created"
}


5. Connexion avec le deuxième utilisateur
✔ Test réussi: Connexion second utilisateur
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MzQ0MywianRpIjoiZDRiZmY3ZGUtYzg4NC00ZDBmLWJiZjYtZDU3YWFlNjk2M2E0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjU5OTY3MzhlLThkMTktNDExNi04NDBiLTcwZjNmYzY2ODkyYiIsIm5iZiI6MTc0MjA3MzQ0MywiY3NyZiI6ImVkYWNjNDM2LWIzMGEtNDM0Ni1hNzJlLWQ2MjQyNGZmYzRiMiIsImV4cCI6MTc0MjE1OTg0MywiaXNfYWRtaW4iOmZhbHNlfQ.Z-3tiPjg8bs_WBmD7kpSrJbqhiIt6CG8XX6O5yT4B5c"
}


Token JWT second utilisateur extrait: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MzQ0MywianRpIjoiZDRiZmY3ZGUtYzg4NC00ZDBmLWJiZjYtZDU3YWFlNjk2M2E0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjU5OTY3MzhlLThkMTktNDExNi04NDBiLTcwZjNmYzY2ODkyYiIsIm5iZiI6MTc0MjA3MzQ0MywiY3NyZiI6ImVkYWNjNDM2LWIzMGEtNDM0Ni1hNzJlLWQ2MjQyNGZmYzRiMiIsImV4cCI6MTc0MjE1OTg0MywiaXNfYWRtaW4iOmZhbHNlfQ.Z-3tiPjg8bs_WBmD7kpSrJbqhiIt6CG8XX6O5yT4B5c

6. Création d'une amenity par l'administrateur
✔ Test réussi: Création amenity
{
    "id": "6b182086-5a2c-492a-8c4a-6f2b48add59d",
    "name": "Amenity Test 1742073442",
    "created_at": "2025-03-15T21:17:23.503426",
    "updated_at": "2025-03-15T21:17:23.503428"
}


ID amenity extrait: 6b182086-5a2c-492a-8c4a-6f2b48add59d

7. Création d'une seconde amenity par l'administrateur
✔ Test réussi: Création seconde amenity
{
    "id": "c0dc4394-f3b7-41df-aa27-d214dd089d27",
    "name": "Second Amenity 1742073442",
    "created_at": "2025-03-15T21:17:23.523914",
    "updated_at": "2025-03-15T21:17:23.523916"
}


ID seconde amenity extrait: c0dc4394-f3b7-41df-aa27-d214dd089d27

8. Création d'une place par l'utilisateur
✔ Test réussi: Création place
{
    "id": "3023af3e-80ca-4cc2-b2f4-50dcebda1245",
    "title": "Appartement Test 1742073442",
    "description": "Magnifique appartement avec vue",
    "price": 100.0,
    "latitude": 48.8566,
    "longitude": 2.3522,
    "owner_id": "1e53d364-c082-4ba1-a56d-2f1660582d51",
    "amenities": [
        {
            "id": "6b182086-5a2c-492a-8c4a-6f2b48add59d",
            "name": "Amenity Test 1742073442"
        }
    ]
}


ID place extrait: 3023af3e-80ca-4cc2-b2f4-50dcebda1245

9. Récupération de toutes les places
Tentative de récupération de toutes les places avec timeout augmenté...
✔ Test réussi: Liste de toutes les places
[
    {
        "id": "3023af3e-80ca-4cc2-b2f4-50dcebda1245",
        "title": "Appartement Test 1742073442",
        "latitude": 48.8566,
        "longitude": 2.3522
    }
]


10. Récupération d'une place spécifique
✔ Test réussi: Récupération place spécifique
{
    "id": "3023af3e-80ca-4cc2-b2f4-50dcebda1245",
    "title": "Appartement Test 1742073442",
    "description": "Magnifique appartement avec vue",
    "price": 100.0,
    "latitude": 48.8566,
    "longitude": 2.3522,
    "owner": {
        "id": "1e53d364-c082-4ba1-a56d-2f1660582d51",
        "first_name": "Test",
        "last_name": "User",
        "email": "user_test_1742073442@example.com"
    },
    "amenities": [
        {
            "id": "6b182086-5a2c-492a-8c4a-6f2b48add59d",
            "name": "Amenity Test 1742073442"
        }
    ],
    "reviews": [],
    "created_at": "2025-03-15T21:17:23.544202",
    "updated_at": "2025-03-15T21:17:23.544206"
}


11. Ajout d'une amenity à une place via PUT
✔ Test réussi: Ajout d'amenities via PUT
{
    "id": "3023af3e-80ca-4cc2-b2f4-50dcebda1245",
    "title": "Appartement Test 1742073442",
    "description": "Magnifique appartement avec vue",
    "price": 100.0,
    "latitude": 48.8566,
    "longitude": 2.3522,
    "owner_id": "1e53d364-c082-4ba1-a56d-2f1660582d51",
    "amenities": [
        {
            "id": "6b182086-5a2c-492a-8c4a-6f2b48add59d",
            "name": "Amenity Test 1742073442"
        },
        {
            "id": "c0dc4394-f3b7-41df-aa27-d214dd089d27",
            "name": "Second Amenity 1742073442"
        }
    ]
}


12. Vérification de l'ajout d'amenities
✔ Test réussi: Vérification de l'ajout d'amenities
{
    "id": "3023af3e-80ca-4cc2-b2f4-50dcebda1245",
    "title": "Appartement Test 1742073442",
    "description": "Magnifique appartement avec vue",
    "price": 100.0,
    "latitude": 48.8566,
    "longitude": 2.3522,
    "owner": {
        "id": "1e53d364-c082-4ba1-a56d-2f1660582d51",
        "first_name": "Test",
        "last_name": "User",
        "email": "user_test_1742073442@example.com"
    },
    "amenities": [
        {
            "id": "6b182086-5a2c-492a-8c4a-6f2b48add59d",
            "name": "Amenity Test 1742073442"
        },
        {
            "id": "c0dc4394-f3b7-41df-aa27-d214dd089d27",
            "name": "Second Amenity 1742073442"
        }
    ],
    "reviews": [],
    "created_at": "2025-03-15T21:17:23.544202",
    "updated_at": "2025-03-15T21:17:23.544206"
}


13. Retrait d'une amenity via PUT
✔ Test réussi: Retrait d'une amenity via PUT
{
    "id": "3023af3e-80ca-4cc2-b2f4-50dcebda1245",
    "title": "Appartement Test 1742073442",
    "description": "Magnifique appartement avec vue",
    "price": 100.0,
    "latitude": 48.8566,
    "longitude": 2.3522,
    "owner_id": "1e53d364-c082-4ba1-a56d-2f1660582d51",
    "amenities": [
        {
            "id": "6b182086-5a2c-492a-8c4a-6f2b48add59d",
            "name": "Amenity Test 1742073442"
        }
    ]
}


14. Vérification du retrait d'amenity
✔ Test réussi: Vérification du retrait d'amenity
{
    "id": "3023af3e-80ca-4cc2-b2f4-50dcebda1245",
    "title": "Appartement Test 1742073442",
    "description": "Magnifique appartement avec vue",
    "price": 100.0,
    "latitude": 48.8566,
    "longitude": 2.3522,
    "owner": {
        "id": "1e53d364-c082-4ba1-a56d-2f1660582d51",
        "first_name": "Test",
        "last_name": "User",
        "email": "user_test_1742073442@example.com"
    },
    "amenities": [
        {
            "id": "6b182086-5a2c-492a-8c4a-6f2b48add59d",
            "name": "Amenity Test 1742073442"
        }
    ],
    "reviews": [],
    "created_at": "2025-03-15T21:17:23.544202",
    "updated_at": "2025-03-15T21:17:23.544206"
}


14. Modification d'une place par le propriétaire
✔ Test réussi: Modification place par propriétaire
{
    "id": "3023af3e-80ca-4cc2-b2f4-50dcebda1245",
    "title": "Super Appartement Test 1742073442",
    "description": "Magnifique appartement avec vue",
    "price": 120.0,
    "latitude": 48.8566,
    "longitude": 2.3522,
    "owner_id": "1e53d364-c082-4ba1-a56d-2f1660582d51",
    "amenities": [
        {
            "id": "6b182086-5a2c-492a-8c4a-6f2b48add59d",
            "name": "Amenity Test 1742073442"
        }
    ]
}


15. Tentative de modification d'une place par un autre utilisateur
✔ Test réussi: Modification place par un autre utilisateur
{
    "error": "Unauthorized action"
}


16. Modification d'une place par l'administrateur
✔ Test réussi: Modification place par admin
{
    "id": "3023af3e-80ca-4cc2-b2f4-50dcebda1245",
    "title": "Admin Modifié Appartement Test 1742073442",
    "description": "Magnifique appartement avec vue",
    "price": 120.0,
    "latitude": 48.8566,
    "longitude": 2.3522,
    "owner_id": "1e53d364-c082-4ba1-a56d-2f1660582d51",
    "amenities": [
        {
            "id": "6b182086-5a2c-492a-8c4a-6f2b48add59d",
            "name": "Amenity Test 1742073442"
        }
    ]
}


17. Vérification des modifications
✔ Test réussi: Vérification des modifications
{
    "id": "3023af3e-80ca-4cc2-b2f4-50dcebda1245",
    "title": "Admin Modifié Appartement Test 1742073442",
    "description": "Magnifique appartement avec vue",
    "price": 120.0,
    "latitude": 48.8566,
    "longitude": 2.3522,
    "owner": {
        "id": "1e53d364-c082-4ba1-a56d-2f1660582d51",
        "first_name": "Test",
        "last_name": "User",
        "email": "user_test_1742073442@example.com"
    },
    "amenities": [
        {
            "id": "6b182086-5a2c-492a-8c4a-6f2b48add59d",
            "name": "Amenity Test 1742073442"
        }
    ],
    "reviews": [],
    "created_at": "2025-03-15T21:17:23.544202",
    "updated_at": "2025-03-15T21:17:23.658219"
}


20. Tentative de suppression d'une place par un autre utilisateur
✔ Test réussi: Suppression place par un autre utilisateur
{
    "error": "Unauthorized action"
}


21. Suppression d'une place par le propriétaire
✔ Test réussi: Suppression place par propriétaire
{
    "message": "Place deleted successfully"
}


22. Vérification de la suppression
✔ Test réussi: Vérification de la suppression
{
    "error": "Place not found"
}


23. Création d'une nouvelle place
✔ Test réussi: Création d'une nouvelle place
{
    "id": "51df8ec5-c541-4080-8170-58a0cc1ca0f6",
    "title": "Nouvelle place 1742073442",
    "description": "Une description",
    "price": 150.0,
    "latitude": 48.1234,
    "longitude": 2.5678,
    "owner_id": "1e53d364-c082-4ba1-a56d-2f1660582d51",
    "amenities": []
}


ID nouvelle place extrait: 51df8ec5-c541-4080-8170-58a0cc1ca0f6

24. Tentative de création d'une place avec données invalides
✔ Test réussi: Création place avec données invalides
{
    "error": "Title is required and must be a non-empty string"
}


25. Suppression d'une place par un administrateur
✔ Test réussi: Suppression place par admin
{
    "message": "Place deleted successfully"
}


26. Vérification de la suppression par admin
✔ Test réussi: Vérification de la suppression par admin
{
    "error": "Place not found"
}


27. Tentative d'accès à une place inexistante
✔ Test réussi: Récupération d'une place avec ID invalide
{
    "error": "Place not found"
}


Tests places terminés.



=== Test de l'API reviews ===

Vérification de l'état de l'API...
API accessible (status code: 404). Début des tests...

Étape préalable: Connexion avec un administrateur
✔ Test réussi: Connexion administrateur
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MzUyMSwianRpIjoiNGIyOGQyOTItMzVmMy00Y2U5LWE5ZjMtZjA3YWVkMTBmYjRmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjM2YzkwNTBlLWRkZDMtNGMzYi05NzMxLTlmNDg3MjA4YmJjMSIsIm5iZiI6MTc0MjA3MzUyMSwiY3NyZiI6IjFiZDc2NGU3LTdkY2QtNDFkYi1iYjkzLWRkNDdhOTg4ZjYwNSIsImV4cCI6MTc0MjE1OTkyMSwiaXNfYWRtaW4iOnRydWV9.CQQCM9434CkB_1T1zgaDVTT7bEG8LILA77S7cqYCPqI"
}


Token JWT admin extrait: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MzUyMSwianRpIjoiNGIyOGQyOTItMzVmMy00Y2U5LWE5ZjMtZjA3YWVkMTBmYjRmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjM2YzkwNTBlLWRkZDMtNGMzYi05NzMxLTlmNDg3MjA4YmJjMSIsIm5iZiI6MTc0MjA3MzUyMSwiY3NyZiI6IjFiZDc2NGU3LTdkY2QtNDFkYi1iYjkzLWRkNDdhOTg4ZjYwNSIsImV4cCI6MTc0MjE1OTkyMSwiaXNfYWRtaW4iOnRydWV9.CQQCM9434CkB_1T1zgaDVTT7bEG8LILA77S7cqYCPqI

1. Création d'un utilisateur propriétaire
✔ Test réussi: Création utilisateur propriétaire
{
    "id": "e173a455-955d-4532-9815-4c6328a2d4b1",
    "message": "User successfully created"
}


ID propriétaire extrait: e173a455-955d-4532-9815-4c6328a2d4b1

2. Connexion avec le propriétaire
✔ Test réussi: Connexion propriétaire
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MzUyMSwianRpIjoiODczZmUyNmMtZTMxOS00MTMzLWE1YzktOWNkYmIzNjE5YjZhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImUxNzNhNDU1LTk1NWQtNDUzMi05ODE1LTRjNjMyOGEyZDRiMSIsIm5iZiI6MTc0MjA3MzUyMSwiY3NyZiI6ImE3MTAzYjFiLTE1MjgtNDJlYy1iMTZjLTNhMTk1YjVlZTc0OSIsImV4cCI6MTc0MjE1OTkyMSwiaXNfYWRtaW4iOmZhbHNlfQ.n45EoU3ONYFOeaJYf9WLv1Rcr56qfJYePAXN21f1DgQ"
}


Token JWT propriétaire extrait: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MzUyMSwianRpIjoiODczZmUyNmMtZTMxOS00MTMzLWE1YzktOWNkYmIzNjE5YjZhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImUxNzNhNDU1LTk1NWQtNDUzMi05ODE1LTRjNjMyOGEyZDRiMSIsIm5iZiI6MTc0MjA3MzUyMSwiY3NyZiI6ImE3MTAzYjFiLTE1MjgtNDJlYy1iMTZjLTNhMTk1YjVlZTc0OSIsImV4cCI6MTc0MjE1OTkyMSwiaXNfYWRtaW4iOmZhbHNlfQ.n45EoU3ONYFOeaJYf9WLv1Rcr56qfJYePAXN21f1DgQ

3. Création d'un utilisateur client
✔ Test réussi: Création utilisateur client
{
    "id": "67195924-8cda-4e65-ae3c-9689103d568b",
    "message": "User successfully created"
}


ID client extrait: 67195924-8cda-4e65-ae3c-9689103d568b

4. Connexion avec le client
✔ Test réussi: Connexion client
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MzUyMiwianRpIjoiNjg2MjIyOWItZDA0Ni00YzNkLTlmMzItNjE1ZGJkMGRmNTYwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjY3MTk1OTI0LThjZGEtNGU2NS1hZTNjLTk2ODkxMDNkNTY4YiIsIm5iZiI6MTc0MjA3MzUyMiwiY3NyZiI6ImZiODMzNWJiLTE5ODgtNGJkNC1hODFkLTllNWI5NTM5NjYyZCIsImV4cCI6MTc0MjE1OTkyMiwiaXNfYWRtaW4iOmZhbHNlfQ.gPsRbKBQoeLyZJ729zUvj7WbjotEUxNyJfHPykOZBWY"
}


Token JWT client extrait: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MzUyMiwianRpIjoiNjg2MjIyOWItZDA0Ni00YzNkLTlmMzItNjE1ZGJkMGRmNTYwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjY3MTk1OTI0LThjZGEtNGU2NS1hZTNjLTk2ODkxMDNkNTY4YiIsIm5iZiI6MTc0MjA3MzUyMiwiY3NyZiI6ImZiODMzNWJiLTE5ODgtNGJkNC1hODFkLTllNWI5NTM5NjYyZCIsImV4cCI6MTc0MjE1OTkyMiwiaXNfYWRtaW4iOmZhbHNlfQ.gPsRbKBQoeLyZJ729zUvj7WbjotEUxNyJfHPykOZBWY

5. Connexion avec un administrateur
✔ Test réussi: Connexion administrateur
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MzUyMiwianRpIjoiYmI4YmIzMjQtMzdiZS00MTU4LTkzMDktNTg4ZGYxNDU5MGQxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjM2YzkwNTBlLWRkZDMtNGMzYi05NzMxLTlmNDg3MjA4YmJjMSIsIm5iZiI6MTc0MjA3MzUyMiwiY3NyZiI6IjdhMDNhODExLWJkZWQtNDRkOC05OWUwLTExZjkxNGNkOTIyNyIsImV4cCI6MTc0MjE1OTkyMiwiaXNfYWRtaW4iOnRydWV9.xixpeyZ-uAwNSvi2_n1TuI1X6N7zS4YUOGkLpq9AFNs"
}


Token JWT admin extrait: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MjA3MzUyMiwianRpIjoiYmI4YmIzMjQtMzdiZS00MTU4LTkzMDktNTg4ZGYxNDU5MGQxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjM2YzkwNTBlLWRkZDMtNGMzYi05NzMxLTlmNDg3MjA4YmJjMSIsIm5iZiI6MTc0MjA3MzUyMiwiY3NyZiI6IjdhMDNhODExLWJkZWQtNDRkOC05OWUwLTExZjkxNGNkOTIyNyIsImV4cCI6MTc0MjE1OTkyMiwiaXNfYWRtaW4iOnRydWV9.xixpeyZ-uAwNSvi2_n1TuI1X6N7zS4YUOGkLpq9AFNs

6. Création d'une place par le propriétaire
✔ Test réussi: Création place
{
    "id": "b8c796bd-f0da-4b6b-80bb-89478b5c200f",
    "title": "Maison Test 1742073520",
    "description": "Belle maison avec jardin",
    "price": 150.0,
    "latitude": 43.6047,
    "longitude": 1.4442,
    "owner_id": "e173a455-955d-4532-9815-4c6328a2d4b1",
    "amenities": []
}


ID place extrait: b8c796bd-f0da-4b6b-80bb-89478b5c200f

7. Création d'une review par le client
✔ Test réussi: Création review
{
    "id": "f228522f-cc8e-4af1-85b2-c174c69ccc8b",
    "text": "Très bon séjour, propriétaire accueillant",
    "rating": 4,
    "user_id": "67195924-8cda-4e65-ae3c-9689103d568b",
    "place_id": "b8c796bd-f0da-4b6b-80bb-89478b5c200f",
    "created_at": "2025-03-15T21:18:42.389092",
    "updated_at": "2025-03-15T21:18:42.389095"
}


ID review extrait: f228522f-cc8e-4af1-85b2-c174c69ccc8b

8. Tentative de création d'une seconde review par le même client
✔ Test réussi: Tentative de double review
{
    "error": "You have already reviewed this place"
}


9. Récupération des reviews d'une place
✔ Test réussi: Récupération reviews d'une place
[
    {
        "id": "f228522f-cc8e-4af1-85b2-c174c69ccc8b",
        "text": "Très bon séjour, propriétaire accueillant",
        "rating": 4,
        "user_id": "67195924-8cda-4e65-ae3c-9689103d568b",
        "created_at": "2025-03-15T21:18:42.389092",
        "updated_at": "2025-03-15T21:18:42.389095"
    }
]


10. Récupération d'une review spécifique
✔ Test réussi: Récupération review spécifique
{
    "id": "f228522f-cc8e-4af1-85b2-c174c69ccc8b",
    "text": "Très bon séjour, propriétaire accueillant",
    "rating": 4,
    "user_id": "67195924-8cda-4e65-ae3c-9689103d568b",
    "place_id": "b8c796bd-f0da-4b6b-80bb-89478b5c200f",
    "created_at": "2025-03-15T21:18:42.389092",
    "updated_at": "2025-03-15T21:18:42.389095"
}


11. Tentative de modification d'une review par un autre utilisateur
✔ Test réussi: Modification par non-auteur
{
    "error": "Unauthorized action"
}


12. Modification d'une review par son auteur
✔ Test réussi: Modification review par auteur
{
    "id": "f228522f-cc8e-4af1-85b2-c174c69ccc8b",
    "text": "Finalement, c était super !",
    "rating": 5,
    "user_id": "67195924-8cda-4e65-ae3c-9689103d568b",
    "place_id": "b8c796bd-f0da-4b6b-80bb-89478b5c200f",
    "created_at": "2025-03-15T21:18:42.389092",
    "updated_at": "2025-03-15T21:18:42.445699"
}


13. Vérification de la modification
✔ Test réussi: Vérification modification
{
    "id": "f228522f-cc8e-4af1-85b2-c174c69ccc8b",
    "text": "Finalement, c était super !",
    "rating": 5,
    "user_id": "67195924-8cda-4e65-ae3c-9689103d568b",
    "place_id": "b8c796bd-f0da-4b6b-80bb-89478b5c200f",
    "created_at": "2025-03-15T21:18:42.389092",
    "updated_at": "2025-03-15T21:18:42.445699"
}


14. Modification d'une review par un administrateur
✔ Test réussi: Modification review par admin
{
    "id": "f228522f-cc8e-4af1-85b2-c174c69ccc8b",
    "text": "Review modérée par un administrateur",
    "rating": 3,
    "user_id": "67195924-8cda-4e65-ae3c-9689103d568b",
    "place_id": "b8c796bd-f0da-4b6b-80bb-89478b5c200f",
    "created_at": "2025-03-15T21:18:42.389092",
    "updated_at": "2025-03-15T21:18:42.469597"
}


15. Suppression d'une review par un administrateur
✔ Test réussi: Suppression review par admin
{
    "message": "Review deleted successfully"
}


16. Vérification de la suppression
✔ Test réussi: Vérification de la suppression
{
    "error": "Review not found"
}


17. Création d'une nouvelle review par le client
✔ Test réussi: Création nouvelle review
{
    "id": "abe7d308-2098-4c8e-a7c7-4db4dba371d1",
    "text": "Review pour tester la suppression",
    "rating": 3,
    "user_id": "67195924-8cda-4e65-ae3c-9689103d568b",
    "place_id": "b8c796bd-f0da-4b6b-80bb-89478b5c200f",
    "created_at": "2025-03-15T21:18:42.507873",
    "updated_at": "2025-03-15T21:18:42.507876"
}


ID nouvelle review extrait: abe7d308-2098-4c8e-a7c7-4db4dba371d1

18. Suppression d'une review par son auteur
✔ Test réussi: Suppression review par auteur
{
    "message": "Review deleted successfully"
}


19. Vérification de la suppression par auteur
✔ Test réussi: Vérification de la suppression par auteur
{
    "error": "Review not found"
}


20. Tentative de création d'une review sans être connecté
✔ Test réussi: Création review sans authentification
{
  "msg": "Missing Authorization Header"
}


21. Tentative de création d'une review avec un rating invalide
✔ Test réussi: Création review avec rating invalide
{
    "error": "Rating must be between 1 and 5"
}


22. Tentative de création d'une review avec un texte vide
✔ Test réussi: Création review avec texte vide
{
    "error": "Text is required and must be a non-empty string"
}


23. Tentative de récupération d'une review inexistante
✔ Test réussi: Récupération d'une review avec ID invalide
{
    "error": "Review not found"
}


24. Création d'une nouvelle review par le propriétaire
✔ Test réussi: Création review par propriétaire
{
    "error": "You cannot review your own place"
}


25. Récupération de toutes les reviews
✔ Test réussi: Récupération de toutes les reviews
[]


26. Création d'une seconde place
✔ Test réussi: Création seconde place
{
    "id": "c184c39e-77b9-4403-a390-0ab9397b0bc2",
    "title": "Appartement Test 1742073520",
    "description": "Petit appartement en centre-ville",
    "price": 80.0,
    "latitude": 44.8378,
    "longitude": -0.5792,
    "owner_id": "e173a455-955d-4532-9815-4c6328a2d4b1",
    "amenities": []
}


ID seconde place extrait: c184c39e-77b9-4403-a390-0ab9397b0bc2

27. Création d'une review pour la seconde place
✔ Test réussi: Création review pour seconde place
{
    "id": "edbf561d-5f04-4f98-b4f8-8151c59a8b66",
    "text": "Appartement correct mais bruyant",
    "rating": 2,
    "user_id": "67195924-8cda-4e65-ae3c-9689103d568b",
    "place_id": "c184c39e-77b9-4403-a390-0ab9397b0bc2",
    "created_at": "2025-03-15T21:18:42.625886",
    "updated_at": "2025-03-15T21:18:42.625889"
}


28. Récupération des reviews de la seconde place
✔ Test réussi: Récupération reviews de la seconde place
[
    {
        "id": "edbf561d-5f04-4f98-b4f8-8151c59a8b66",
        "text": "Appartement correct mais bruyant",
        "rating": 2,
        "user_id": "67195924-8cda-4e65-ae3c-9689103d568b",
        "created_at": "2025-03-15T21:18:42.625886",
        "updated_at": "2025-03-15T21:18:42.625889"
    }
]


30. Récupération des reviews d'une place inexistante
✔ Test réussi: Récupération reviews d'une place inexistante
{
    "error": "Place not found"
}


31. Tentative de modification d'une review avec un rating invalide

ID second review extrait: edbf561d-5f04-4f98-b4f8-8151c59a8b66
✔ Test réussi: Modification review avec rating invalide
{
    "error": "Rating must be between 1 and 5"
}


Tests de l'API reviews terminés.