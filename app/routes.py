# app/routes.py
from flask import jsonify
from functools import wraps
from flask import Blueprint, request, current_app
from elasticsearch import NotFoundError
import os

# Create blueprint for items API
items_bp = Blueprint('items', __name__)

def require_api_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_token = request.headers.get('X-API-Token')
        expected_token = os.getenv('API_TOKEN')
        
        if not api_token or api_token != expected_token:
            return jsonify({
                "error": "Unauthorized",
                "detail": "Invalid or missing API token"
            }), 401
        return f(*args, **kwargs)
    return decorated_function

@items_bp.route('/api/v1/items/<string:id>', methods=['GET'])
@require_api_token
def get_item_by_id(id):
    """Get a single item by its ID."""
    try:
        es = current_app.elasticsearch
        result = es.get(index=os.getenv('ELASTICSEARCH_INDEX', 'items'), id=id)
        return jsonify(result['_source']), 200
    except NotFoundError:
        return jsonify({"error": "Item not found"}), 404
    except Exception as e:
        current_app.logger.error(f"Error retrieving item {id}: {str(e)}")
        return jsonify({"error": "Failed to retrieve item"}), 500

@items_bp.route('/api/v1/items', methods=['PUT'])
@require_api_token
def create_or_update_item():
    """Create or update an item in the search index."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['id', 'name', 'suggest_input']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "error": "Invalid request body",
                    "detail": f"Missing required field: {field}"
                }), 400

        # Optional fields with defaults
        data.setdefault('description', '')
        data.setdefault('tags', [])
        data.setdefault('metadata', {})

        es = current_app.elasticsearch
        result = es.index(
            index=os.getenv('ELASTICSEARCH_INDEX', 'items'),
            id=data['id'],
            document=data,
            refresh=True  # Make the document immediately searchable
        )

        return jsonify({
            "message": "Item successfully indexed",
            "id": data['id'],
            "index": result['_index']
        }), 200

    except ValueError as e:
        return jsonify({
            "error": "Invalid request body",
            "detail": str(e)
        }), 400
    except Exception as e:
        current_app.logger.error(f"Error indexing item: {str(e)}")
        return jsonify({"error": "Failed to index item"}), 500

def init_routes(app):
    @app.route('/api/status', methods=['GET'])
    def status():
        return jsonify({"status": "Search service is running"}), 200