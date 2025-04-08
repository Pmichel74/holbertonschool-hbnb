#!/bin/bash

# Test script for authenticated endpoints

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Base URL for the API
BASE_URL="http://127.0.0.1:5000/api/v1"

echo -e "${GREEN}Testing Authenticated Endpoints${NC}"

# Step 1: Login and get JWT token
echo -e "\n${GREEN}Step 1: Login and get JWT token${NC}"
echo -e "curl -X POST \"$BASE_URL/auth/login\" -H \"Content-Type: application/json\" -d '{
  \"email\": \"john.doe@example.com\",
  \"password\": \"password123\"
}'"

LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" -H "Content-Type: application/json" -d '{
  "email": "john.doe@example.com",
  "password": "password123"
}')

echo -e "\nResponse: $LOGIN_RESPONSE"

# Extract the JWT token from the response
JWT_TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

if [ -z "$JWT_TOKEN" ]; then
  echo -e "${RED}Failed to extract JWT token from response${NC}"
  exit 1
fi

echo -e "\nJWT Token: $JWT_TOKEN"

# Step 2: Test Place Creation (POST /api/v1/places/)
echo -e "\n${GREEN}Step 2: Test Place Creation (POST /api/v1/places/)${NC}"
echo -e "curl -X POST \"$BASE_URL/places/\" -d '{\"title\": \"New Place\", \"price\": 100, \"latitude\": 40.7128, \"longitude\": -74.0060}' -H \"Authorization: Bearer $JWT_TOKEN\" -H \"Content-Type: application/json\""

PLACE_RESPONSE=$(curl -s -X POST "$BASE_URL/places/" -d '{
  "title": "New Place",
  "price": 100,
  "latitude": 40.7128,
  "longitude": -74.0060
}' -H "Authorization: Bearer $JWT_TOKEN" -H "Content-Type: application/json")

echo -e "\nResponse: $PLACE_RESPONSE"

# Extract the place ID from the response
PLACE_ID=$(echo $PLACE_RESPONSE | grep -o '"id":"[^"]*"' | cut -d'"' -f4)

if [ -z "$PLACE_ID" ]; then
  echo -e "${RED}Failed to extract place ID from response${NC}"
  # Create a dummy place ID for testing subsequent steps
  PLACE_ID="dummy-place-id"
else
  echo -e "\nPlace ID: $PLACE_ID"
fi

# Step 3: Test Unauthorized Place Update (PUT /api/v1/places/<place_id>)
echo -e "\n${GREEN}Step 3: Test Unauthorized Place Update (PUT /api/v1/places/<place_id>)${NC}"
echo -e "curl -X PUT \"$BASE_URL/places/another-place-id\" -d '{\"title\": \"Updated Place\"}' -H \"Authorization: Bearer $JWT_TOKEN\" -H \"Content-Type: application/json\""

UNAUTHORIZED_RESPONSE=$(curl -s -X PUT "$BASE_URL/places/another-place-id" -d '{
  "title": "Updated Place"
}' -H "Authorization: Bearer $JWT_TOKEN" -H "Content-Type: application/json")

echo -e "\nResponse: $UNAUTHORIZED_RESPONSE"

# Check if the response contains the expected error message
if echo "$UNAUTHORIZED_RESPONSE" | grep -q "Unauthorized action"; then
  echo -e "${GREEN}PASS: Received expected 'Unauthorized action' error${NC}"
else
  echo -e "${RED}FAIL: Did not receive expected 'Unauthorized action' error${NC}"
fi

# Step 4: Test Creating a Review (POST /api/v1/reviews/)
echo -e "\n${GREEN}Step 4: Test Creating a Review (POST /api/v1/reviews/)${NC}"
echo -e "curl -X POST \"$BASE_URL/reviews/\" -d '{\"place_id\": \"$PLACE_ID\", \"text\": \"Great place!\", \"rating\": 5}' -H \"Authorization: Bearer $JWT_TOKEN\" -H \"Content-Type: application/json\""

REVIEW_RESPONSE=$(curl -s -X POST "$BASE_URL/reviews/" -d "{
  \"place_id\": \"$PLACE_ID\",
  \"text\": \"Great place!\",
  \"rating\": 5
}" -H "Authorization: Bearer $JWT_TOKEN" -H "Content-Type: application/json")

echo -e "\nResponse: $REVIEW_RESPONSE"

# Extract the review ID from the response
REVIEW_ID=$(echo $REVIEW_RESPONSE | grep -o '"id":"[^"]*"' | cut -d'"' -f4)

if [ -z "$REVIEW_ID" ]; then
  echo -e "${RED}Failed to extract review ID from response${NC}"
  # Create a dummy review ID for testing subsequent steps
  REVIEW_ID="dummy-review-id"
else
  echo -e "\nReview ID: $REVIEW_ID"
fi

# Step 5: Test Updating a Review (PUT /api/v1/reviews/<review_id>)
echo -e "\n${GREEN}Step 5: Test Updating a Review (PUT /api/v1/reviews/<review_id>)${NC}"
echo -e "curl -X PUT \"$BASE_URL/reviews/$REVIEW_ID\" -d '{\"text\": \"Updated review\"}' -H \"Authorization: Bearer $JWT_TOKEN\" -H \"Content-Type: application/json\""

UPDATE_REVIEW_RESPONSE=$(curl -s -X PUT "$BASE_URL/reviews/$REVIEW_ID" -d '{
  "text": "Updated review",
  "rating": 4
}' -H "Authorization: Bearer $JWT_TOKEN" -H "Content-Type: application/json")

echo -e "\nResponse: $UPDATE_REVIEW_RESPONSE"

# Step 6: Test Deleting a Review (DELETE /api/v1/reviews/<review_id>)
echo -e "\n${GREEN}Step 6: Test Deleting a Review (DELETE /api/v1/reviews/<review_id>)${NC}"
echo -e "curl -X DELETE \"$BASE_URL/reviews/$REVIEW_ID\" -H \"Authorization: Bearer $JWT_TOKEN\""

DELETE_REVIEW_RESPONSE=$(curl -s -X DELETE "$BASE_URL/reviews/$REVIEW_ID" -H "Authorization: Bearer $JWT_TOKEN")

echo -e "\nResponse: $DELETE_REVIEW_RESPONSE"

# Step 7: Test Modifying User Data (PUT /api/v1/users/<user_id>)
echo -e "\n${GREEN}Step 7: Test Modifying User Data (PUT /api/v1/users/<user_id>)${NC}"
echo -e "curl -X PUT \"$BASE_URL/users/current-user-id\" -d '{\"first_name\": \"Updated Name\"}' -H \"Authorization: Bearer $JWT_TOKEN\" -H \"Content-Type: application/json\""

# Extract the user ID from the JWT token (assuming it's a JWT token with a payload that contains the user ID)
USER_ID=$(echo $JWT_TOKEN | cut -d'.' -f2 | base64 -d 2>/dev/null | grep -o '"id":"[^"]*"' | cut -d'"' -f4)

if [ -z "$USER_ID" ]; then
  echo -e "${RED}Failed to extract user ID from JWT token${NC}"
  # Use a placeholder user ID
  USER_ID="current-user-id"
fi

echo -e "\nUser ID: $USER_ID"

USER_UPDATE_RESPONSE=$(curl -s -X PUT "$BASE_URL/users/$USER_ID" -d '{
  "first_name": "Updated Name"
}' -H "Authorization: Bearer $JWT_TOKEN" -H "Content-Type: application/json")

echo -e "\nResponse: $USER_UPDATE_RESPONSE"

# Step 8: Test Modifying User Email (should fail)
echo -e "\n${GREEN}Step 8: Test Modifying User Email (should fail)${NC}"
echo -e "curl -X PUT \"$BASE_URL/users/$USER_ID\" -d '{\"email\": \"new.email@example.com\"}' -H \"Authorization: Bearer $JWT_TOKEN\" -H \"Content-Type: application/json\""

EMAIL_UPDATE_RESPONSE=$(curl -s -X PUT "$BASE_URL/users/$USER_ID" -d '{
  "email": "new.email@example.com"
}' -H "Authorization: Bearer $JWT_TOKEN" -H "Content-Type: application/json")

echo -e "\nResponse: $EMAIL_UPDATE_RESPONSE"

# Check if the response contains the expected error message
if echo "$EMAIL_UPDATE_RESPONSE" | grep -q "You cannot modify email or password"; then
  echo -e "${GREEN}PASS: Received expected 'You cannot modify email or password' error${NC}"
else
  echo -e "${RED}FAIL: Did not receive expected 'You cannot modify email or password' error${NC}"
fi

echo -e "\n${GREEN}Authenticated Endpoints Test Completed${NC}"
