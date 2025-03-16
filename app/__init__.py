# app/__init__.py
from flask import Flask
from flask_cors import CORS
from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, resources={
        r"/api/*": {"origins": os.getenv('CORS_ORIGINS', '*')}
    })

    # Configure Elasticsearch
    app.elasticsearch = Elasticsearch(
        os.getenv('ELASTICSEARCH_URL'),
        api_key=os.getenv('ELASTICSEARCH_API_KEY')
    )

    # Register blueprints
    from .routes import items_bp
    app.register_blueprint(items_bp)

    # Create index if it doesn't exist
    index_name = os.getenv('ELASTICSEARCH_INDEX', 'items')
    if not app.elasticsearch.indices.exists(index=index_name):
        app.elasticsearch.indices.create(
            index=index_name,
            mappings={
                "properties": {
                    "id": {"type": "keyword"},
                    "name": {"type": "text"},
                    "description": {"type": "text"},
                    "tags": {"type": "keyword"},
                    "suggest_input": {"type": "completion"},
                    "metadata": {
                        "type": "object",
                        "dynamic": True
                    }
                }
            }
        )

    return app
