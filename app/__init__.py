# app/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Load environment variables if needed
    from dotenv import load_dotenv
    load_dotenv()

    # Register routes
    from .routes import init_routes
    init_routes(app)

    return app
