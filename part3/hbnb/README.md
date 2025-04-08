# HBnB Application 🏠

A Flask-based API for the HBnB (Holberton Bed and Breakfast) application.

## Table of Contents 📑

- Overview
- Project Structure
- Setup and Installation
- Running the Application
- API Documentation
- API Endpoints
  - User Endpoints
  - Amenity Endpoints
- Running Tests
- Project Components
- Business Logic Layer
- Development
- Next Steps

## Overview 🔎

HBnB is a property management application inspired by Airbnb, offering a RESTful API for managing users, amenities, places, and bookings.

## Project Structure 🏗️

```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── tests/
│   ├── test_users_api.sh
├── run.py
├── config.py
├── requirements.txt
├── README.md
```

## Setup and Installation 🛠️

1. Clone the repository
2. Navigate to the project directory
3. Create a virtual environment:
   ```
   python3 -m venv venv
   ```
4. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`
5. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Application 🚀

To run the application, use the following commands:

```
source venv/bin/activate  # Activate the virtual environment (if not already activated)
python run.py
```

The application will start and be accessible at `http://localhost:5000`.

## API Documentation 📚

API documentation will be available at `http://localhost:5000/api/v1/` when the application is running. This includes Swagger UI for interactive API testing.

## API Endpoints 🔌

### User Endpoints 👤

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|------------|
| POST | `/api/v1/users/` | Create a new user | 201 Created |
| GET | `/api/v1/users/` | Get a list of all users | 200 OK |
| GET | `/api/v1/users/<user_id>` | Get details of a specific user | 200 OK |
| PUT | `/api/v1/users/<user_id>` | Update a user's information | 200 OK |

### Amenity Endpoints 🧩

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|------------|
| POST | `/api/v1/amenities/` | Create a new amenity | 201 Created |
| GET | `/api/v1/amenities/` | Get a list of all amenities | 200 OK |
| GET | `/api/v1/amenities/<amenity_id>` | Get details of a specific amenity | 200 OK |
| PUT | `/api/v1/amenities/<amenity_id>` | Update an amenity's information | 200 OK |

For detailed information on request/response formats and status codes, please refer to the API documentation.

## Running Tests 🧪

To run the API tests, use the following commands:

```bash
# Make the test script executable
chmod +x tests/test_users_api.sh

# Run the tests
./tests/test_users_api.sh
```

Make sure the application is running before executing the tests. The test script tests both User and Amenity endpoints.

## Project Components 🧩

- `app/__init__.py`: Creates and configures the Flask application
- `app/api/v1/`: Contains the API endpoints
  - `users.py`: Implements User API endpoints
  - `amenities.py`: Implements Amenity API endpoints
- `app/models/`: Contains the business logic classes
  - `base_model.py`: Base class for all models
  - `user.py`: User model
  - `place.py`: Place model
  - `review.py`: Review model
  - `amenity.py`: Amenity model
- `app/services/facade.py`: Implements the Facade pattern for communication between layers
- `app/persistence/repository.py`: Implements the in-memory repository
- `run.py`: Entry point for running the application
- `config.py`: Configuration settings for the application
- `tests/test_users_api.sh`: Shell script for running API tests using curl

## Business Logic Layer 💼

The Business Logic layer is implemented in the `app/models/` directory. It consists of the following classes:

- `BaseModel`: A base class that provides common attributes and methods for all models.
- `User`: Represents a user of the application.
- `Place`: Represents a place that can be rented.
- `Review`: Represents a review for a place.
- `Amenity`: Represents an amenity that a place can have.

These classes implement data validation, relationships between entities, and business rules. They use UUIDs as identifiers and include timestamps for creation and updates.

## Development 👨‍💻

This project uses a layered architecture with:
- 🖥️ **Presentation Layer** (API): REST endpoints for interacting with the application
- 🧠 **Business Logic Layer**: Facade and services implementing business rules
- 💾 **Persistence Layer**: Repositories for data management

The Facade pattern is used for communication between these layers, providing a simplified interface to the complex subsystem.

For now, an in-memory repository is used for data storage. In future iterations, this will be replaced with a database-backed solution.

## Next Steps 🔜

- ✅ Implement User API endpoints
- ✅ Implement Amenity API endpoints
- 🔄 Implement API endpoints for Places and Reviews
- 🔄 Add search functionality
- 🔄 Add authentication and authorization
- 🔄 Integrate with a persistent database
- 🔄 Deploy to production
- 🔄 Implement error handling and logging