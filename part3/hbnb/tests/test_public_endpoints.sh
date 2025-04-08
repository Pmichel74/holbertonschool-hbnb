#!/bin/bash

# Test script for public endpoints

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Base URL for the API
BASE_URL="http://127.0.0.1:5000/api/v1"

echo -e "${GREEN}Testing Public Endpoints${NC}"

# Step 1: Retrieve a list of places
echo -e "\n${GREEN}Step 1: Retrieve a list of places${NC}"
echo -e "curl -X GET \"$BASE_URL/places/\""

PLACES_RESPONSE=$(curl -s -X GET "$BASE_URL/places/")

echo -e "\nResponse: $PLACES_RESPONSE"

# Check if the response contains place data
if echo "$PLACES_RESPONSE" | grep -q "id"; then
  echo -e "${GREEN}PASS: Successfully retrieved list of places${NC}"
else
  echo -e "${RED}FAIL: Could not retrieve list of places${NC}"
fi

# Extract the first place ID from the response
PLACE_ID=$(echo $PLACES_RESPONSE | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$PLACE_ID" ]; then
  echo -e "${RED}Failed to extract place ID from response${NC}"
  # Use a placeholder place ID
  PLACE_ID="1fa85f64-5717-4562-b3fc-2c963f66afa6"
else
  echo -e "\nPlace ID: $PLACE_ID"
fi

# Step 2: Retrieve detailed information about a specific place
echo -e "\n${GREEN}Step 2: Retrieve detailed information about a specific place${NC}"
echo -e "curl -X GET \"$BASE_URL/places/$PLACE_ID\""

PLACE_DETAILS_RESPONSE=$(curl -s -X GET "$BASE_URL/places/$PLACE_ID")

echo -e "\nResponse: $PLACE_DETAILS_RESPONSE"

# Check if the response contains detailed place data
if echo "$PLACE_DETAILS_RESPONSE" | grep -q "description"; then
  echo -e "${GREEN}PASS: Successfully retrieved place details${NC}"
else
  echo -e "${RED}FAIL: Could not retrieve place details${NC}"
fi

# Step 3: Test accessing a protected endpoint without authentication
echo -e "\n${GREEN}Step 3: Test accessing a protected endpoint without authentication${NC}"
echo -e "curl -X POST \"$BASE_URL/places/\" -d '{\"title\": \"New Place\", \"price\": 100, \"latitude\": 40.7128, \"longitude\": -74.0060}' -H \"Content-Type: application/json\""

UNAUTHORIZED_RESPONSE=$(curl -s -X POST "$BASE_URL/places/" -d '{
  "title": "New Place",
  "price": 100,
  "latitude": 40.7128,
  "longitude": -74.0060
}' -H "Content-Type: application/json")

echo -e "\nResponse: $UNAUTHORIZED_RESPONSE"

# Check if the response contains an authentication error
if echo "$UNAUTHORIZED_RESPONSE" | grep -q "Missing Authorization Header"; then
  echo -e "${GREEN}PASS: Protected endpoint correctly requires authentication${NC}"
else
  echo -e "${RED}FAIL: Protected endpoint does not require authentication${NC}"
fi

echo -e "\n${GREEN}Public Endpoints Test Completed${NC}"
