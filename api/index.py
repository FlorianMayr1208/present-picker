"""
Vercel Serverless Function Entry Point
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.app import create_app

# Create Flask app
app = create_app()

# Vercel expects a handler function
def handler(environ, start_response):
    return app(environ, start_response)

# For direct WSGI compatibility
application = app
