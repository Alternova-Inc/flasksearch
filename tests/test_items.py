import json
import pytest
from flask import current_app

def test_create_item(client, auth_headers, sample_item):
    """Test creating a new item via PUT endpoint."""
    # Make the request to create the item
    response = client.put(
        '/api/v1/items',
        data=json.dumps(sample_item),
        headers=auth_headers
    )
    
    # Check response
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Item successfully indexed'
    assert data['id'] == str(sample_item['id'])
    assert 'index' in data

def test_get_item(client, auth_headers, sample_item):
    """Test retrieving an item by ID."""
    # First create the item
    client.put(
        '/api/v1/items',
        data=json.dumps(sample_item),
        headers=auth_headers
    )
    
    # Then try to retrieve it
    response = client.get(
        f'/api/v1/items/{sample_item["id"]}',
        headers=auth_headers
    )
    
    # Check response
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == sample_item['id']
    assert data['name'] == sample_item['name']
    assert data['description'] == sample_item['description']
    assert data['tags'] == sample_item['tags']
    assert data['suggest_input'] == sample_item['suggest_input']

def test_get_nonexistent_item(client, auth_headers):
    """Test retrieving an item that doesn't exist."""
    response = client.get(
        '/api/v1/items/999999',
        headers=auth_headers
    )
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error'] == 'Item not found'

def test_create_item_without_auth(client, sample_item):
    """Test creating an item without authentication."""
    response = client.put(
        '/api/v1/items',
        data=json.dumps(sample_item),
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['error'] == 'Unauthorized'

def test_get_item_without_auth(client, sample_item):
    """Test retrieving an item without authentication."""
    response = client.get(
        f'/api/v1/items/{sample_item["id"]}',
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['error'] == 'Unauthorized'

def test_create_item_invalid_data(client, auth_headers):
    """Test creating an item with invalid data."""
    invalid_item = {
        "name": "Test Item"
        # Missing required fields: id, suggest_input
    }
    
    response = client.put(
        '/api/v1/items',
        data=json.dumps(invalid_item),
        headers=auth_headers
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error'] == 'Invalid request body'
    assert 'Missing required field' in data['detail'] 