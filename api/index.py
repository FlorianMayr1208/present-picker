"""
Vercel Serverless Function Entry Point
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import app
from app import app

# Export the Flask app directly - Vercel will handle the rest
# The variable name must be 'app'
app = app
