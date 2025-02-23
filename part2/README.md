# HBnB - Business Logic Layer

## Features
- UUID-based identification
- Timestamp tracking
- Data validation
- Relationship management
- Object serialization
- Comprehensive unit tests

## Requirements
- Python 3.7+
- UUID module
- DateTime module

## Project Structure

### Models
The application is built around four core models:

#### BaseModel
- Provides common functionality for all models
- Attributes:
  - `id`: UUID string
  - `created_at`: DateTime of creation
  - `updated_at`: DateTime of last update
- Methods:
  - `save()`: Updates the updated_at timestamp
  - `update(data)`: Updates attributes from dictionary

#### User
- Manages user information and relationships
- Attributes:
  - `first_name`: String (max 50 chars)
  - `last_name`: String (max 50 chars)
  - `email`: Valid email address
  - `is_admin`: Boolean
- Methods:
  - `add_place(place)`: Associates a place with user
  - `add_review(review)`: Associates a review with user

#### Place
- Handles rental property information
- Attributes:
  - `title`: String (max 100 chars)
  - `description`: String
  - `price`: Positive float
  - `latitude`: Float (-90 to 90)
  - `longitude`: Float (-180 to 180)
  - `owner`: User reference
- Methods:
  - `add_review(review)`: Adds a review
  - `add_amenity(amenity)`: Adds an amenity

#### Review
- Manages user reviews for places
- Attributes:
  - `text`: Review content
  - `rating`: Integer (1-5)
  - `place`: Place reference
  - `user`: User reference

#### Amenity
- Represents available features
- Attributes:
  - `name`: String (max 50 chars)

## Usage Examples

### Creating a User and Place
```python
# Create a new user
user = User(
    first_name="John",
    last_name="Doe",
    email="john.doe@example.com"
)

# Create a place owned by the user
place = Place(
    title="Cozy Apartment",
    description="Beautiful city center apartment",
    price=100.0,
    latitude=48.8566,
    longitude=2.3522,
    owner=user
)

# Add amenities
wifi = Amenity("Wi-Fi")
place.add_amenity(wifi)

# Add a review
review = Review(
    text="Great stay!",
    rating=5,
    place=place,
    user=user
)
```

## Installation
```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Running Tests
```bash
python -m unittest tests/test_models.py
```


