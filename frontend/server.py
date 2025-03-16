#!/usr/bin/env python3
"""
Simple HTTP server for the frontend files.
This is just for development and testing purposes.
"""

import http.server
import socketserver
import os
import json

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add CORS headers for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept, X-API-Token')
        super().end_headers()
    
    def do_OPTIONS(self):
        # Handle OPTIONS requests for CORS preflight
        self.send_response(200)
        self.end_headers()
    
    def do_GET(self):
        # Special handling for .env file
        if self.path == '/.env':
            # Check if .env file exists
            env_path = os.path.join(DIRECTORY, '.env')
            if os.path.exists(env_path):
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                
                # Read and send the .env file
                with open(env_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                # If .env doesn't exist, try to use .env.example
                example_path = os.path.join(DIRECTORY, '.env.example')
                if os.path.exists(example_path):
                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain')
                    self.end_headers()
                    
                    # Read and send the .env.example file
                    with open(example_path, 'rb') as f:
                        self.wfile.write(f.read())
                else:
                    # If neither exists, return 404
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b'Environment file not found')
        else:
            # Handle all other requests normally
            super().do_GET()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        print(f"To use the application, create a .env file with your API token")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
            httpd.server_close() 