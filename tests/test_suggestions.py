import json
import pytest
from flask import current_app

def test_suggestions_basic_search(client, auth_headers):
    """Test basic suggestions search with query and zipcode."""
    query_term = "bookstore"
    zipcode = "10001"
    
    response = client.get(
        f'/api/v1/suggestions?query={query_term}&zipcode={zipcode}',
        headers=auth_headers
    )
    
    # Check response
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'items' in data
    assert isinstance(data['items'], list)
    assert 'meta' in data
    assert data['meta']['time_ms'] >= 0
    assert 'count' in data['meta']
    assert 'total' in data['meta']
    assert isinstance(data['meta']['count'], int)
    assert isinstance(data['meta']['total'], int)

def test_suggestions_missing_parameters(client, auth_headers):
    """Test suggestions with missing required parameters."""
    # Test missing query
    response = client.get(
        '/api/v1/suggestions?zipcode=10001',
        headers=auth_headers
    )
    assert response.status_code == 400
    
    # Test missing zipcode
    response = client.get(
        '/api/v1/suggestions?query=test',
        headers=auth_headers
    )
    assert response.status_code == 400

def test_suggestions_without_auth(client):
    """Test suggestions endpoint without authentication."""
    response = client.get(
        '/api/v1/suggestions?query=test&zipcode=10001',
        headers={'Content-Type': 'application/json'}
    )
    
    # Should return 401 Unauthorized
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['error'] == 'Unauthorized'
