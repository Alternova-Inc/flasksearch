import os
import json
import pytest
from app import create_app

@pytest.fixture
def app():
    """Create and configure a test Flask application instance."""
    # Ensure we're using test configurations
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['API_TOKEN'] = 'test-token'
    
    app = create_app()
    app.config['TESTING'] = True
    
    return app

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()

@pytest.fixture
def sample_item():
    """Load a sample item from the test data."""
    with open('data/test_establishments.json', 'r') as f:
        items = json.load(f)
        # Using Classic Library from New York as our test item
        return items[0]  # First item in the test data

@pytest.fixture
def auth_headers():
    """Return headers with test authentication token."""
    return {
        'X-API-Token': 'test-token',
        'Content-Type': 'application/json'
    } 