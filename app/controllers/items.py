from flask import jsonify, request, current_app
from elasticsearch import NotFoundError
import os

def get_item(id):
    """Get a single item by its ID."""
    try:
        es = current_app.elasticsearch
        result = es.get(index=os.getenv('ELASTICSEARCH_INDEX', 'items'), id=str(id))
        return jsonify(result['_source']), 200
    except NotFoundError:
        return jsonify({"error": "Item not found"}), 404
    except Exception as e:
        current_app.logger.error(f"Error retrieving item {id}: {str(e)}")
        return jsonify({"error": "Failed to retrieve item"}), 500

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

        # Ensure id is converted to string for consistency
        item_id = str(data['id'])
        data['id'] = item_id

        es = current_app.elasticsearch
        result = es.index(
            index=os.getenv('ELASTICSEARCH_INDEX', 'items'),
            id=item_id,
            document=data,
            refresh=True  # Make the document immediately searchable
        )

        return jsonify({
            "message": "Item successfully indexed",
            "id": item_id,
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