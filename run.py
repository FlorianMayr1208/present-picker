"""
Startskript für die Reise-Auswahl-App
"""
import sys
import os

# Füge das Projektverzeichnis zum Python-Pfad hinzu
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.app import create_app

if __name__ == '__main__':
    app = create_app()
    print("\n" + "="*60)
    print("  Reise-Auswahl-App gestartet!")
    print("  URL: http://localhost:5001")
    print("="*60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5001)
