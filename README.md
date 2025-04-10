# 🏠 HBNB - AirBnB Clone Project

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [Project Structure](#-project-structure)
- [Project Phases](#-project-phases)
  - [Part 2: API Backend](#-part-2-api-backend)
  - [Part 3: Database Models](#-part-3-database-models)
  - [Part 4: Frontend](#-part-4-frontend)
- [Installation & Setup](#-installation--setup)
- [API Endpoints](#-api-endpoints)
- [Response Formats](#-response-formats)
- [Model Validation Rules](#-model-validation-rules)
- [API Testing Documentation](#-api-testing-documentation)

## 🌐 Project Overview

HBNB is a full-stack web application clone of AirBnB, comprising a RESTful API backend, database models, and an interactive front-end interface. This project demonstrates the implementation of a complete web application architecture following best practices in software development.

## 📁 Project Structure
```bash
holbertonschool-hbnb/
├── part2/                   # API Backend
│   ├── app/
│   │   ├── __init__.py      # App initialization and configuration
│   │   ├── api/
│   │   │   └── v1/          # API endpoints 
│   │   │       ├── amenities.py
│   │   │       ├── places.py
│   │   │       ├── reviews.py
│   │   │       └── users.py
│   │   ├── models/          # Data models
│   │   │   ├── amenity.py
│   │   │   ├── base_model.py
│   │   │   ├── place.py
│   │   │   ├── review.py
│   │   │   └── user.py
│   │   ├── persistence/     # Data storage
│   │   │   └── repository.py
│   │   └── services/        # Business logic
│   │       ├── facade.py
│   │       └── test.py
│   ├── config.py            # Configuration settings
│   ├── run.py               # Application entry point
│   ├── requirements.txt     # Project dependencies
│   └── tests/               # API test suite
│
├── part3/                   # Database Models
│   ├── hbnb/                # Main application package
│   │   ├── __init__.py
│   │   ├── models/          # SQLAlchemy ORM models
│   │   │   ├── amenity.py
│   │   │   ├── base.py
│   │   │   ├── place.py
│   │   │   ├── review.py
│   │   │   └── user.py
│   │   ├── routes/          # API routes
│   │   └── templates/       # Flask templates
│   ├── instance/            # Instance-specific configs
│   └── venv/                # Virtual environment
│
├── part4/                   # Frontend Implementation
│   ├── img/                 # Image assets
│   ├── js/                  # JavaScript modules
│   ├── tests/               # Frontend tests
│   ├── index.html           # Main landing page
│   ├── login.html           # User authentication page
│   ├── place.html           # Place details page
│   ├── scripts.js           # Main JavaScript file
│   └── styles.css           # CSS styles
│
└── uml/                     # UML diagrams
```

## 📚 Project Phases

### 🚀 Part 2: API Backend

The API backend provides RESTful endpoints for managing users, places, reviews, and amenities. Built with Flask, it follows a structured architecture with:

- **API Layer**: RESTful endpoint definitions with proper HTTP method handling
- **Model Layer**: Data models with validation rules
- **Persistence Layer**: Data storage abstraction (repository pattern)
- **Service Layer**: Business logic implementation

**Key Features:**
- RESTful API design principles
- Resource-based URL structure
- Proper HTTP status codes
- JSON response formatting
- Error handling and validation

**Technology Stack:**
- Python 3.8+
- Flask RESTful
- Custom validation middleware
- Unit testing with pytest

### 💾 Part 3: Database Models

This phase implements the database layer using SQLAlchemy ORM:

- **Entity Models**: SQLAlchemy ORM models for all application entities
- **Relationships**: Many-to-many and one-to-many relationships
- **Migration System**: Alembic migrations for versioned schema changes
- **Database Configuration**: Support for multiple database backends

**Key Features:**
- Database schema design
- SQLAlchemy ORM implementation
- Foreign key relationships
- Cascading deletions
- Indexes for performance optimization

**Technology Stack:**
- SQLAlchemy ORM
- Alembic migrations
- PostgreSQL (primary)
- SQLite (development/testing)

### 🖥️ Part 4: Frontend

The frontend provides a responsive user interface for interacting with the HBNB application:

- **Landing Page**: Display of featured places
- **Search Interface**: Filtering places by location, price, amenities
- **User Authentication**: Login/signup flows
- **Place Details**: Detailed view of places with amenities and reviews
- **Booking System**: Calendar-based booking interface

**Key Features:**
- Responsive design (mobile-first approach)
- Interactive UI components
- Client-side form validation
- API integration with fetch API
- Image gallery with lazy loading

**Technology Stack:**
- HTML5/CSS3
- JavaScript (ES6+)
- Fetch API for AJAX requests
- CSS Grid and Flexbox for layouts
- Jest for frontend testing

## ⚙️ Installation & Setup

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

## 👨‍💻 Author
- **Patrick Michel** - [PMichel74](https://github.com/PMichel74)

## 📄 License
All projects are licensed under their respective licenses as specified in each repository.
