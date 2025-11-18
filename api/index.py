"""
Vercel Serverless Function Entry Point
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import simplified app without database
from app_simple import app

# Vercel expects a handler function
def handler(environ, start_response):
    return app(environ, start_response)

# For direct WSGI compatibility
application = app
