from functools import wraps
from flask import request, jsonify
import os

def require_api_token(f):
    """Decorator to check for valid API token in request headers."""
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