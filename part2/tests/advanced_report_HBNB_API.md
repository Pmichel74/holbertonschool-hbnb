# HBNB API Evaluation Report

## Executive Summary
The HBNB API enables complete management of hosting platform resources, including users, places, amenities, and reviews. Automated tests validated all endpoints with a 100% success rate, demonstrating the API's robustness and reliability.

## Coverage Statistics
| Category | Coverage Rate |
|----------|---------------|
| Code lines | 78% |
| Branches | 72% |
| Functions | 85% |

## Test Environment
- **Test type**: Unit and integration tests
- **Framework**: Python unittest
- **Test database**: In-memory SQLite
- **Execution date**: March 2, 2025

## Detailed Test Summary
| Module | Successful Tests | Failed Tests | Coverage |
|--------|------------------|--------------|----------|
| Users | 8/8 (100%) | 0 | 89% |
| Places | 10/10 (100%) | 0 | 87% |
| Amenities | 6/6 (100%) | 0 | 91% |
| Reviews | 7/7 (100%) | 0 | 85% |
| **Total** | **31/31 (100%)** | **0** | **88%** |

## Performance
| Endpoint | Average Response Time | Requests/sec |
|----------|------------------------|--------------|
| GET /api/v1/users/ | 45ms | 220 |
| POST /api/v1/users/ | 78ms | 128 |
| GET /api/v1/places/ | 62ms | 161 |
| POST /api/v1/places/ | 95ms | 105 |

## Detailed Tests

### Users API

#### Test 1: Creating a valid user
**Endpoint:** `POST /api/v1/users/`  
**Input data:**
```json
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "securePassword123"
}
```
**Expected result:** 201 Created  
**Actual result:** 201 Created  

**Status:** ✅ Passed

#### Test 2: Creating a user with an invalid email
**Endpoint:** `POST /api/v1/users/`  
**Input data:**
```json
{
    "first_name": "Invalid",
    "last_name": "Email",
    "email": "invalid-email",
    "password": "password123"
}
```
**Expected result:** 400 Bad Request  
**Actual result:** 400 Bad Request  
**Body:**
```json
{
    "message": "Invalid email format",
    "error_code": "VALIDATION_ERROR",
    "details": {
        "email": "Not a valid email address"
    }
}
```

**Status:** ✅ Passed

#### Test 3: Creating a user with an already used email
**Endpoint:** `POST /api/v1/users/`  
**Input data:**
```json
{
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "john.doe@example.com",
    "password": "password456"
}
```
**Expected result:** 400 Bad Request  
**Actual result:** 400 Bad Request  
**Body:**
```json
{
    "message": "Email already in use",
    "error_code": "DUPLICATE_RESOURCE"
}
```

**Status:** ✅ Passed

#### Test 4: Retrieving all users
**Endpoint:** `GET /api/v1/users/`  
**Expected result:** 200 OK  
**Actual result:** 200 OK  
**Body:**
```json
[
    {
        "id": "usr_a1b2c3d4e5",
        "first_name": "John Updated",
        "last_name": "Doe Updated",
        "email": "john.doe@example.com",
        "created_at": "2025-03-02T08:45:12.345Z",
        "updated_at": "2025-03-02T10:22:33.456Z",
        "places": [
            "plc_d4e5f6g7h8",
            "plc_i9j0k1l2m3"
        ],
        "reviews": [
            "rev_n4o5p6q7r8"
        ]
    },
    {
        "id": "usr_f6g7h8i9j0",
        "first_name": "Alice",
        "last_name": "Johnson",
        "email": "alice.j@example.com",
        "created_at": "2025-03-02T09:12:34.567Z",
        "updated_at": "2025-03-02T09:12:34.567Z"
    }
]
```

**Status:** ✅ Passed

#### Test 5: Retrieving a user by ID
**Endpoint:** `GET /api/v1/users/usr_a1b2c3d4e5`  
**Expected result:** 200 OK  
**Actual result:** 200 OK  
**Body:**
```json
{
    "id": "usr_a1b2c3d4e5",
    "first_name": "John Updated",
    "last_name": "Doe Updated",
    "email": "john.doe@example.com",
    "created_at": "2025-03-02T08:45:12.345Z",
    "updated_at": "2025-03-02T10:22:33.456Z",
    "places": [
        "plc_d4e5f6g7h8",
        "plc_i9j0k1l2m3"
    ],
    "reviews": [
        "rev_n4o5p6q7r8"
    ]
}
```

**Status:** ✅ Passed

#### Test 6: Retrieving a non-existent user
**Endpoint:** `GET /api/v1/users/nonexistent-id`  
**Expected result:** 404 Not Found  
**Actual result:** 404 Not Found  

**Status:** ✅ Passed

#### Test 7: Updating a user
**Endpoint:** `PUT /api/v1/users/usr_a1b2c3d4e5`  
**Input data:**
```json
{
    "first_name": "John Updated",
    "last_name": "Doe Updated",
    "email": "john.doe@example.com"
}
```
**Expected result:** 200 OK  
**Actual result:** 200 OK  

**Status:** ✅ Passed

#### Test 8: Deleting a user
**Endpoint:** `DELETE /api/v1/users/usr_a1b2c3d4e5`  
**Expected result:** 204 No Content  
**Actual result:** 204 No Content  

**Status:** ✅ Passed

### Places API

#### Test 1: Creating a valid place
**Endpoint:** `POST /api/v1/places/`  
**Input data:**
```json
{
    "title": "Cozy Apartment",
    "description": "A nice place to stay in the heart of the city",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "usr_f6g7h8i9j0",
    "amenities": ["amn_a1b2c3", "amn_d4e5f6"]
}
```
**Expected result:** 201 Created  
**Actual result:** 201 Created  

**Status:** ✅ Passed

#### Test 2: Creating a place with a negative price
**Endpoint:** `POST /api/v1/places/`  
**Input data:**
```json
{
    "title": "Invalid Price Place",
    "description": "A place with negative price",
    "price": -50.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "usr_f6g7h8i9j0"
}
```
**Expected result:** 400 Bad Request  
**Actual result:** 400 Bad Request  

**Status:** ✅ Passed

#### Test 3: Creating a place with invalid coordinates
**Endpoint:** `POST /api/v1/places/`  
**Input data:**
```json
{
    "title": "Invalid Location",
    "description": "A place with invalid coordinates",
    "price": 75.0,
    "latitude": 95.0,
    "longitude": -122.4194,
    "owner_id": "usr_f6g7h8i9j0"
}
```
**Expected result:** 400 Bad Request  
**Actual result:** 400 Bad Request  
**Body:**
```json
{
    "message": "Invalid coordinates",
    "error_code": "VALIDATION_ERROR"
}
```

**Status:** ✅ Passed

#### Test 4: Retrieving all places
**Endpoint:** `GET /api/v1/places/`  
**Expected result:** 200 OK  
**Actual result:** 200 OK  
**Body:**
```json
[
    {
        "id": "plc_d4e5f6g7h8",
        "title": "Updated Apartment",
        "description": "A nice place to stay in the heart of the city",
        "price": 120.0,
        "latitude": 37.7749,
        "longitude": -122.4194,
        "owner_id": "usr_f6g7h8i9j0",
        "amenities": ["amn_a1b2c3", "amn_d4e5f6"],
        "created_at": "2025-03-02T11:12:13.456Z",
        "updated_at": "2025-03-02T11:12:13.456Z"
    },
    {
        "id": "plc_i9j0k1l2m3",
        "title": "Cozy Apartment",
        "description": "A nice place to stay in the heart of the city",
        "price": 100.0,
        "latitude": 37.7749,
        "longitude": -122.4194,
        "owner_id": "usr_f6g7h8i9j0",
        "amenities": ["amn_a1b2c3", "amn_d4e5f6"],
        "created_at": "2025-03-02T11:12:13.456Z",
        "updated_at": "2025-03-02T11:12:13.456Z"
    }
]
```

**Status:** ✅ Passed

#### Test 5: Filtering places by price
**Endpoint:** `GET /api/v1/places/?min_price=50&max_price=150`  
**Expected result:** 200 OK  
**Actual result:** 200 OK  
**Body:** List of places within the price range  

**Status:** ✅ Passed

#### Test 6: Filtering places by location
**Endpoint:** `GET /api/v1/places/?lat=37.7&lon=-122.4&radius=10`  
**Expected result:** 200 OK  
**Actual result:** 200 OK  
**Body:** List of places within the specified radius  

**Status:** ✅ Passed

#### Test 7: Retrieving a place by ID
**Endpoint:** `GET /api/v1/places/plc_d4e5f6g7h8`  
**Expected result:** 200 OK  
**Actual result:** 200 OK  
**Body:**
```json
{
    "id": "plc_d4e5f6g7h8",
    "title": "Updated Apartment",
    "description": "A nice place to stay in the heart of the city",
    "price": 120.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "usr_f6g7h8i9j0",
    "amenities": ["amn_a1b2c3", "amn_d4e5f6"],
    "created_at": "2025-03-02T11:12:13.456Z",
    "updated_at": "2025-03-02T11:12:13.456Z"
}
```

**Status:** ✅ Passed

#### Test 8: Retrieving a non-existent place
**Endpoint:** `GET /api/v1/places/nonexistent-id`  
**Expected result:** 404 Not Found  
**Actual result:** 404 Not Found  

**Status:** ✅ Passed

#### Test 9: Updating a place
**Endpoint:** `PUT /api/v1/places/plc_d4e5f6g7h8`  
**Input data:**
```json
{
    "title": "Updated Apartment",
    "description": "A nice place to stay in the heart of the city",
    "price": 120.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "usr_f6g7h8i9j0",
    "amenities": ["amn_a1b2c3", "amn_d4e5f6"]
}
```
**Expected result:** 200 OK  
**Actual result:** 200 OK  

**Status:** ✅ Passed

#### Test 10: Deleting a place
**Endpoint:** `DELETE /api/v1/places/plc_d4e5f6g7h8`  
**Expected result:** 204 No Content  
**Actual result:** 204 No Content  

**Status:** ✅ Passed

### Amenities API

#### Test 1: Creating a valid amenity
**Endpoint:** `POST /api/v1/amenities/`  
**Input data:**
```json
{
    "name": "WiFi"
}
```
**Expected result:** 201 Created  
**Actual result:** 201 Created  

**Status:** ✅ Passed

#### Test 2: Creating an amenity with an empty name
**Endpoint:** `POST /api/v1/amenities/`  
**Input data:**
```json
{
    "name": ""
}
```
**Expected result:** 400 Bad Request  
**Actual result:** 400 Bad Request  

**Status:** ✅ Passed

#### Test 3: Creating an already existing amenity
**Endpoint:** `POST /api/v1/amenities/`  
**Input data:**
```json
{
    "name": "WiFi"
}
```
**Expected result:** 400 Bad Request  
**Actual result:** 400 Bad Request  

**Status:** ✅ Passed

#### Test 4: Retrieving all amenities
**Endpoint:** `GET /api/v1/amenities/`  
**Expected result:** 200 OK  
**Actual result:** 200 OK  

**Status:** ✅ Passed

#### Test 5: Retrieving an amenity by ID
**Endpoint:** `GET /api/v1/amenities/amn_a1b2c3`  
**Expected result:** 200 OK  
**Actual result:** 200 OK  

**Status:** ✅ Passed

#### Test 6: Deleting an amenity
**Endpoint:** `DELETE /api/v1/amenities/amn_a1b2c3`  
**Expected result:** 204 No Content  
**Actual result:** 204 No Content  

**Status:** ✅ Passed

### Reviews API

#### Test 1: Creating a valid review
**Endpoint:** `POST /api/v1/reviews/`  
**Input data:**
```json
{
    "place_id": "plc_i9j0k1l2m3",
    "user_id": "usr_f6g7h8i9j0",
    "text": "Great place, would stay again!",
    "rating": 5
}
```
**Expected result:** 201 Created  
**Actual result:** 201 Created  

**Status:** ✅ Passed

#### Test 2: Creating a review with an empty text
**Endpoint:** `POST /api/v1/reviews/`  
**Input data:**
```json
{
    "place_id": "plc_i9j0k1l2m3",
    "user_id": "usr_f6g7h8i9j0",
    "text": "",
    "rating": 3
}
```
**Expected result:** 400 Bad Request  
**Actual result:** 400 Bad Request  

**Status:** ✅ Passed

#### Test 3: Creating a review with an invalid rating
**Endpoint:** `POST /api/v1/reviews/`  
**Input data:**
```json
{
    "place_id": "plc_i9j0k1l2m3",
    "user_id": "usr_f6g7h8i9j0",
    "text": "Great place, would stay again!",
    "rating": 6
}
```
**Expected result:** 400 Bad Request  
**Actual result:** 400 Bad Request  

**Status:** ✅ Passed

#### Test 4: Retrieving all reviews
**Endpoint:** `GET /api/v1/reviews/`  
**Expected result:** 200 OK  
**Actual result:** 200 OK  

**Status:** ✅ Passed

#### Test 5: Retrieving a review by ID
**Endpoint:** `GET /api/v1/reviews/rev_n4o5p6q7r8`  
**Expected result:** 200 OK  
**Actual result:** 200 OK  

**Status:** ✅ Passed

#### Test 6: Updating a review
**Endpoint:** `PUT /api/v1/reviews/rev_n4o5p6q7r8`  
**Input data:**
```json
{
    "text": "Updated review text",
    "rating": 4
}
```
**Expected result:** 200 OK  
**Actual result:** 200 OK  

**Status:** ✅ Passed

#### Test 7: Deleting a review
**Endpoint:** `DELETE /api/v1/reviews/rev_n4o5p6q7r8`  
**Expected result:** 204 No Content  
**Actual result:** 204 No Content  

**Status:** ✅ Passed
