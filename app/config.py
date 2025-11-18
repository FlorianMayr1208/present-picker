import os


class Config:
    """Basis-Konfiguration für die Flask-App"""

    # Sicherheit
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Datenbank
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE_URL = os.environ.get('DATABASE_URL') or os.environ.get('POSTGRES_URL')

    # Fix for Vercel/Supabase Postgres URLs
    if DATABASE_URL:
        # Remove query parameters that psycopg2 doesn't understand
        if '?' in DATABASE_URL:
            base_url, params = DATABASE_URL.split('?', 1)
            # Keep only sslmode parameter if present
            if 'sslmode=' in params:
                import re
                sslmode_match = re.search(r'sslmode=([^&]+)', params)
                if sslmode_match:
                    DATABASE_URL = f"{base_url}?sslmode={sslmode_match.group(1)}"
                else:
                    DATABASE_URL = base_url
            else:
                DATABASE_URL = base_url

        # Fix postgres:// -> postgresql://
        if DATABASE_URL.startswith('postgres://'):
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

    SQLALCHEMY_DATABASE_URI = DATABASE_URL or \
        'sqlite:///' + os.path.join(BASE_DIR, '..', 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload-Konfiguration
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'images')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # Slider-Konfiguration
    SLIDER_MIN = 0
    SLIDER_MAX = 5
