# Complete Documentation: API Endpoints Testing and Validation

## **Objective**

This documentation describes the validation process, the tests performed using `cURL`, and automated tests with `unittest`. The goal is to ensure that the API endpoints function correctly, respect the defined input and output formats, and that validation rules are properly applied.

---

## **1. Business Logic Validation Implementation**

### **1.1 User Model Validation**

#### **Validated Attributes:**
- `first_name`: Must not be empty.
- `last_name`: Must not be empty.
- `email`: Must follow a valid email format.

#### **Validation Code (Python):**

```python
import re

class User:
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def validate(self):
        if not self.first_name or not self.last_name:
            raise ValueError("First name and last name cannot be empty.")
        if not self.email or not self.is_valid_email(self.email):
            raise ValueError("Invalid email format.")
        return True

    def is_valid_email(self, email):
        # Simple regex for email validation
        email_regex = r"(^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$)"
        return re.match(email_regex, email) is not None
```
### **1.2 Place Model Validation**
```
Validated Attributes:
title: Must not be empty.
price: Must be a positive number.
latitude: Must be between -90 and 90.
longitude: Must be between -180 and 180.

Validation Code (Python):
class Place:
    def __init__(self, title, price, latitude, longitude):
        self.title = title
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

    def validate(self):
        if not self.title:
            raise ValueError("Title cannot be empty.")
        if self.price <= 0:
            raise ValueError("Price must be a positive number.")
        if not (-90 <= self.latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if not (-180 <= self.longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        return True
```
### **1.3 Review Model Validation**
```
Validated Attributes:
text: Must not be empty.
user_id and place_id: Must reference valid entities.
rating: Must be between 1 and 5.

Validation Code (Python):
class Review:
    def __init__(self, text, rating, user_id, place_id):
        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id

    def validate(self):
        if not self.text:
            raise ValueError("Text cannot be empty.")
        if not self.user_id or not self.place_id:
            raise ValueError("User ID and Place ID must be valid.")
        if not (1 <= self.rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        return True
```
## **2. Endpoint Tests Using cURL**
## **2.1 Create a User (POST /api/v1/users/)**
```
Example of a valid test:
curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}'

Expected Response:
{
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}

Example of an invalid test:
curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{
    "first_name": "",
    "last_name": "",
    "email": "invalid-email"
}'

Expected Response:
{
    "error": "Invalid input data"
}
```
### **2.2 Create a Place (POST /api/v1/places/)**
```
Example of a valid test:
curl -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{
    "title": "Beautiful House",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194
}'

Expected Response:
{
    "id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
    "title": "Beautiful House",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194
}

Example of an invalid test (negative price):
curl -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{
    "title": "Beautiful House",
    "price": -100.0,
    "latitude": 37.7749,
    "longitude": -122.4194
}'
```
## **2.3 Create a Review (POST /api/v1/reviews/)**
```
Example of a valid test:
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" -H "Content-Type: application/json" -d '{
    "text": "Great place to stay!",
    "rating": 5,
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "place_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6"
}'

Expected Response:
{
    "id": "2fa85f64-5717-4562-b3fc-2c963f66afa6",
    "text": "Great place to stay!",
    "rating": 5,
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "place_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6"
}

Example of an invalid test (empty text):
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" -H "Content-Type: application/json" -d '{
    "text": "",
    "rating": 6,
    "user_id": "",
    "place_id": ""
}'

Expected Response:
{
    "error": "Invalid input data"
}
```
### **3. Automated Tests with unittest**
### **3.1 Example Test for Creating a User**
```
import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)
```
## **3.2 Example Test for Creating a Review**
```
class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_review(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Amazing place!",
            "rating": 5,
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "place_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)

    def test_create_review_invalid_data(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 6,
            "user_id": "",
            "place_id": ""
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)
```
## **4. Test Procedure Documentation**

### **4.1 Manual Test Cases**

| Test Case | Endpoint | Input Data | Expected Result | Status |
|-----------|----------|------------|-----------------|---------|
| TC-001 | POST /api/v1/users | `{"email": "user@example.com", "password": "strongpass123", "first_name": "John", "last_name": "Doe"}` | Created: 201 | ✅ Pass |
| TC-002 | POST /api/v1/places | `{"name": "Cozy Cabin", "description": "A peaceful retreat", "number_rooms": 2, "number_bathrooms": 1, "max_guest": 4, "price_by_night": 100, "latitude": 40.7128, "longitude": -74.0060}` | Created: 201 | ✅ Pass |
| TC-003 | POST /api/v1/reviews | `{"text": "Great stay!", "place_id": "place-uuid", "user_id": "user-uuid"}` | Created: 201 | ✅ Pass |
| TC-004 | GET /api/v1/users | N/A | Success: 200, List of users | ✅ Pass |
| TC-005 | GET /api/v1/places | N/A | Success: 200, List of places | ✅ Pass |
| TC-006 | GET /api/v1/reviews | N/A | Success: 200, List of reviews | ✅ Pass |

### **4.2 Authentication Tests**

| Test Case | Endpoint | Input Data | Expected Result | Status |
|-----------|----------|------------|-----------------|---------|
| TC-007 | POST /api/v1/auth/login | `{"email": "user@example.com", "password": "strongpass123"}` | Success: 200, JWT Token | ✅ Pass |
| TC-008 | POST /api/v1/auth/register | `{"email": "new@example.com", "password": "newpass123", "first_name": "Jane", "last_name": "Smith"}` | Created: 201 | ✅ Pass |

### **4.3 Automated Test Cases**

Our test suite includes comprehensive unit tests for:
- ✅ User authentication and registration
- ✅ CRUD operations for Places
- ✅ CRUD operations for Reviews
- ✅ Input validation and error handling
- ✅ API endpoint security

All tests can be run using:
```bash
python3 -m unittest discover tests
```
````
Unit tests have been executed and passed all test cases, including valid and invalid cases for each entity (user, place, review).

Conclusion

Validation Implemented: Validations were applied at the model level (user, place, review).
cURL Tests: Manual tests were performed using cURL to test the endpoints.
Automated Tests: Automated tests were executed with unittest to test both valid and invalid cases.
