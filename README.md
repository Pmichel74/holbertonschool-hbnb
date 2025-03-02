# HBNB API Documentation

## 📁 Project Structure
```bash
hbnb-2/
├── app/
│   ├── __init__.py           # App initialization and configuration
│   ├── api/
│   │   └── v1/              # API endpoints 
│   │       ├── amenities.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── users.py
│   ├── models/              # Data models
│   │   ├── amenity.py
│   │   ├── base_model.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── user.py
│   ├── persistence/         # Data storage
│   │   └── repository.py
│   └── services/           # Business logic
│       ├── facade.py
│       └── test.py
├── config.py               # Configuration settings
├── run.py                 # Application entry point
└── requirements.txt       # Project dependencies
```

## 🚀 Installation & Setup

1. Create and activate virtual environment:
```bash
python3 -m venv env
source env/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python3 run.py
```

The API will be available at `http://127.0.0.1:5000`

## ⚙️ Configuration

The application supports different environments through `config.py`:

- Development (default): Debug mode enabled
- Testing: For running tests
- Production: For deployment

To change environment:
```bash
export FLASK_ENV=development  # or testing/production
```

## 🧪 API Testing Documentation

### Manual Test Cases

| Endpoint | Method | Test Data | Expected | Status |
|----------|--------|-----------|-----------|---------|
| `/api/v1/users/` | POST | `{"first_name": "John", "last_name": "Doe", "email": "john@example.com"}` | 201 | ✅ |
| `/api/v1/places/` | POST | `{"title": "Cozy Cabin", "price": 100, "latitude": 40.7128, "longitude": -74.0060}` | 201 | ✅ |
| `/api/v1/reviews/` | POST | `{"text": "Great!", "rating": 5, "place_id": "uuid", "user_id": "uuid"}` | 201 | ✅ |
| `/api/v1/amenities/` | POST | `{"name": "WiFi"}` | 201 | ✅ |

### Running Tests
```bash
python3 -m unittest discover tests
```

### Example Test Cases

#### User Creation Test
```python
def test_create_user(self):
    response = self.client.post('/api/v1/users/', json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@example.com"
    })
    self.assertEqual(response.status_code, 201)
```

#### Place Creation Test
```python
def test_create_place(self):
    response = self.client.post('/api/v1/places/', json={
        "title": "Mountain View",
        "price": 150.0,
        "latitude": 37.7749,
        "longitude": -122.4194
    })
    self.assertEqual(response.status_code, 201)
```

#### Review Creation Test
```python
def test_create_review(self):
    response = self.client.post('/api/v1/reviews/', json={
        "text": "Amazing place!",
        "rating": 5,
        "place_id": "place-uuid",
        "user_id": "user-uuid"
    })
    self.assertEqual(response.status_code, 201)
```

## 🚀 API Endpoints

### Users API
- `POST /api/v1/users/`: Create new user
- `GET /api/v1/users/`: List all users
- `GET /api/v1/users/<id>`: Get specific user
- `PUT /api/v1/users/<id>`: Update user

### Places API
- `POST /api/v1/places/`: Create new place
- `GET /api/v1/places/`: List all places
- `GET /api/v1/places/<id>`: Get specific place
- `PUT /api/v1/places/<id>`: Update place

### Reviews API
- `POST /api/v1/reviews/`: Create new review
- `GET /api/v1/reviews/`: List all reviews
- `GET /api/v1/reviews/<id>`: Get specific review
- `PUT /api/v1/reviews/<id>`: Update review

### Amenities API
- `POST /api/v1/amenities/`: Create new amenity
- `GET /api/v1/amenities/`: List all amenities
- `GET /api/v1/amenities/<id>`: Get specific amenity
- `PUT /api/v1/amenities/<id>`: Update amenity

## 📊 Response Formats

### Success Response
```json
{
    "id": "uuid",
    "created_at": "timestamp",
    "updated_at": "timestamp",
    ...resource specific fields...
}
```

### Error Response
```json
{
    "error": "Error message"
}
```

## 🔑 Model Validation Rules

### User Model
- First name and last name cannot be empty
- Valid email format required

### Place Model
- Title cannot be empty
- Price must be positive
- Latitude must be between -90 and 90
- Longitude must be between -180 and 180

### Review Model
- Text cannot be empty
- Rating must be between 1 and 5
- Valid user_id and place_id required

### Amenity Model
- Name cannot be empty
- Name must be between 1 and 50 characters
