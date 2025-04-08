#!/bin/bash

# Test script for authentication flow

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Base URL for the API
BASE_URL="http://127.0.0.1:5000/api/v1"

echo -e "${GREEN}Testing Authentication Flow${NC}"

# Step 1: Login and get JWT token
echo -e "\n${GREEN}Step 1: Login and get JWT token${NC}"
echo -e "curl -X POST \"$BASE_URL/auth/login\" -H \"Content-Type: application/json\" -d '{
  \"email\": \"john.doe@example.com\",
  \"password\": \"your_password\"
}'"

LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" -H "Content-Type: application/json" -d '{
  "email": "john.doe@example.com",
  "password": "your_password"
}')

echo -e "\nResponse: $LOGIN_RESPONSE"

# Extract the JWT token from the response
JWT_TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

if [ -z "$JWT_TOKEN" ]; then
  echo -e "${RED}Failed to extract JWT token from response${NC}"
  exit 1
fi

echo -e "\nJWT Token: $JWT_TOKEN"

# Step 2: Access a protected endpoint
echo -e "\n${GREEN}Step 2: Access a protected endpoint${NC}"
echo -e "curl -X GET \"$BASE_URL/auth/protected\" -H \"Authorization: Bearer $JWT_TOKEN\""

PROTECTED_RESPONSE=$(curl -s -X GET "$BASE_URL/auth/protected" -H "Authorization: Bearer $JWT_TOKEN")

echo -e "\nResponse: $PROTECTED_RESPONSE"

# Check if the response contains the expected message
if echo "$PROTECTED_RESPONSE" | grep -q "Hello, user"; then
  echo -e "${GREEN}PASS: Successfully accessed protected endpoint${NC}"
else
  echo -e "${RED}FAIL: Could not access protected endpoint${NC}"
fi

echo -e "\n${GREEN}Authentication Flow Test Completed${NC}"
