#!/bin/bash
# Tests cURL pour HBNB API

# Variables pour stocker les IDs créés
USER_ID=""
PLACE_ID=""
AMENITY_ID=""
REVIEW_ID=""

echo "=== Testing User Endpoints ==="

echo "1. Creating a valid user"
USER_RESPONSE=$(curl -s -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}')
echo "$USER_RESPONSE"
USER_ID=$(echo $USER_RESPONSE | python -c "import sys, json; print(json.load(sys.stdin)['id'])")

echo "2. Creating a user with invalid email"
curl -s -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{
    "first_name": "Invalid",
    "last_name": "Email",
    "email": "invalid-email"
}'

echo "3. Getting all users"
curl -s -X GET "http://127.0.0.1:5000/api/v1/users/"

echo "4. Getting user by ID"
curl -s -X GET "http://127.0.0.1:5000/api/v1/users/$USER_ID"

echo "5. Getting non-existent user"
curl -s -X GET "http://127.0.0.1:5000/api/v1/users/non-existent-id"

echo "=== Testing Amenity Endpoints ==="

echo "1. Creating a valid amenity"
AMENITY_RESPONSE=$(curl -s -X POST "http://127.0.0.1:5000/api/v1/amenities/" -H "Content-Type: application/json" -d '{
    "name": "WiFi"
}')
echo "$AMENITY_RESPONSE"
AMENITY_ID=$(echo $AMENITY_RESPONSE | python -c "import sys, json; print(json.load(sys.stdin)['id'])")

echo "2. Creating an amenity with empty name"
curl -s -X POST "http://127.0.0.1:5000/api/v1/amenities/" -H "Content-Type: application/json" -d '{
    "name": ""
}'

echo "=== Testing Place Endpoints ==="

echo "1. Creating a valid place"
PLACE_RESPONSE=$(curl -s -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d "{
    \"title\": \"Beautiful Apartment\",
    \"description\": \"A nice apartment in the city center\",
    \"price\": 100.0,
    \"latitude\": 48.858844,
    \"longitude\": 2.294351,
    \"owner_id\": \"$USER_ID\",
    \"amenities\": [\"$AMENITY_ID\"]
}")
echo "$PLACE_RESPONSE"
PLACE_ID=$(echo $PLACE_RESPONSE | python -c "import sys, json; print(json.load(sys.stdin)['id'])")

echo "2. Creating a place with invalid latitude"
curl -s -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d "{
    \"title\": \"Invalid Place\",
    \"price\": 50.0,
    \"latitude\": 100.0,
    \"longitude\": 2.0,
    \"owner_id\": \"$USER_ID\"
}"

echo "3. Creating a place with negative price"
curl -s -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d "{
    \"title\": \"Negative Price\",
    \"price\": -10.0,
    \"latitude\": 48.0,
    \"longitude\": 2.0,
    \"owner_id\": \"$USER_ID\"
}"

echo "=== Testing Review Endpoints ==="

echo "1. Creating a valid review"
REVIEW_RESPONSE=$(curl -s -X POST "http://127.0.0.1:5000/api/v1/reviews/" -H "Content-Type: application/json" -d "{
    \"text\": \"Great place to stay!\",
    \"rating\": 5,
    \"user_id\": \"$USER_ID\",
    \"place_id\": \"$PLACE_ID\"
}")
echo "$REVIEW_RESPONSE"
REVIEW_ID=$(echo $REVIEW_RESPONSE | python -c "import sys, json; print(json.load(sys.stdin)['id'])")

echo "2. Creating a review with invalid rating"
curl -s -X POST "http://127.0.0.1:5000/api/v1/reviews/" -H "Content-Type: application/json" -d "{
    \"text\": \"Invalid rating\",
    \"rating\": 10,
    \"user_id\": \"$USER_ID\",
    \"place_id\": \"$PLACE_ID\"
}"

echo "3. Getting reviews for a place"
curl -s -X GET "http://127.0.0.1:5000/api/v1/places/$PLACE_ID/reviews"

echo "4. Deleting a review"
curl -s -X DELETE "http://127.0.0.1:5000/api/v1/reviews/$REVIEW_ID"

echo "5. Verifying review deletion"
curl -s -X GET "http://127.0.0.1:5000/api/v1/reviews/$REVIEW_ID"
