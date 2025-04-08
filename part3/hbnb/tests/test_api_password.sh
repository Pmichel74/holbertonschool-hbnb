#!/bin/bash

# Test script for password hashing in the API

# Base URL for the API
BASE_URL="http://localhost:5000/api/v1"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "Testing password hashing in the API..."

# 1. Create a new user with a password
echo -e "\n${GREEN}1. Creating a new user with a password...${NC}"
USER_RESPONSE=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "password": "password123"
  }' \
  $BASE_URL/users/)

echo "Response: $USER_RESPONSE"

# Check if the response contains a password field
if echo "$USER_RESPONSE" | grep -q "password"; then
  echo -e "${RED}FAIL: Response contains a password field${NC}"
else
  echo -e "${GREEN}PASS: Response does not contain a password field${NC}"
fi

# Extract the user ID from the response
USER_ID=$(echo "$USER_RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)

if [ -z "$USER_ID" ]; then
  echo -e "${RED}Failed to extract user ID from response${NC}"
  exit 1
fi

echo "User ID: $USER_ID"

# 2. Get the user details
echo -e "\n${GREEN}2. Getting user details...${NC}"
USER_DETAILS=$(curl -s -X GET $BASE_URL/users/$USER_ID)

echo "Response: $USER_DETAILS"

# Check if the response contains a password field
if echo "$USER_DETAILS" | grep -q "password"; then
  echo -e "${RED}FAIL: Response contains a password field${NC}"
else
  echo -e "${GREEN}PASS: Response does not contain a password field${NC}"
fi

echo -e "\n${GREEN}Tests completed.${NC}"
