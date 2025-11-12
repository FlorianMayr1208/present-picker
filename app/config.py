import os


class Config:
    """Basis-Konfiguration für die Flask-App"""

    # Sicherheit
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Datenbank
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, '..', 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload-Konfiguration
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'images')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # Slider-Konfiguration
    SLIDER_MIN = 0
    SLIDER_MAX = 5
