# app/routes.py
from urllib import request
from flask import Blueprint, jsonify
from .middleware.auth import require_api_token
from .controllers.items import get_item, create_or_update_item, delete_item

# Create blueprint for items API
items_bp = Blueprint('items', __name__)

# Item routes
@items_bp.route('/api/v1/items/<string:id>', methods=['GET'])
@require_api_token
def get_item_by_id(id):
    return get_item(id)

@items_bp.route('/api/v1/items', methods=['PUT'])
@require_api_token
def update_item():
    return create_or_update_item()

@items_bp.route('/api/v1/items/<id>', methods=['DELETE'])
@require_api_token
def delete_item_route(id):
    return delete_item(id)

@items_bp.route('/api/v1/items/search', methods=['GET'])
@require_api_token
def search_items():
    query = request.args.get('query', '')
    zipcode = request.args.get('zipcode', '')
    return jsonify(search_items(query, zipcode))

# Health check route
def init_routes(app):
    @app.route('/api/status', methods=['GET'])
    def status():
        return jsonify({"status": "Search service is running"}), 200