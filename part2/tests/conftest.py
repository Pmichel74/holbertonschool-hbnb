# tests/conftest.py
import pytest
import sys
import os

# Ajout du chemin du projet au PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def api_prefix():
    """Return the API prefix."""
    return '/api/v1'

@pytest.fixture
def headers():
    """Return the default headers for API requests."""
    return {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
