# Dateien zum Aufräumen

## ❌ Können gelöscht werden (Datenbank-Version - nicht mehr benötigt)

### Python Files
- `run.py` - Alter Einstiegspunkt mit Datenbank
- `init_db.py` - SQLite Datenbank Initialisierung
- `migrate_to_postgres.py` - PostgreSQL Migration
- `setup_supabase.py` - Supabase Setup
- `app/app.py` - Alte App mit Datenbank
- `app/config.py` - Config mit Datenbank-Settings
- `app/models/` - SQLAlchemy Models (kompletter Ordner)

### Dokumentation (veraltet)
- `VERCEL_DEPLOYMENT.md` - Vercel mit Datenbank
- `SUPABASE_SETUP.md` - Supabase Anleitung
- `requirements.md` - Alte Projekt-Requirements

### Admin Templates (Datenbank-Version)
- `app/templates/admin.html`
- `app/templates/admin_destination_form.html`
- `app/templates/admin_activities.html`
- `app/templates/admin_activity_form.html`
- `app/templates/admin_import.html`

## ✅ Behalten (Simplified Version - wird verwendet)

### Python Files
- `app_simple.py` ✓ Hauptanwendung
- `api/index.py` ✓ Vercel Entry Point
- `requirements.txt` ✓ Dependencies (vereinfacht)

### Daten
- `data/destinations.json` ✓
- `data/activities.json` ✓

### Templates (werden verwendet)
- `app/templates/base.html` ✓
- `app/templates/index.html` ✓
- `app/templates/destination.html` ✓
- `app/templates/admin_simple.html` ✓
- `app/templates/admin_activities_simple.html` ✓

### Dokumentation
- `README_SIMPLE.md` ✓ Aktuelle Anleitung
- `.vercelignore` ✓
- `vercel.json` ✓

### Static Files
- `app/static/css/style.css` ✓
- `app/static/images/` ✓ (optional, aktuell leer)

## 🗑️ Automatisches Cleanup

Führe aus:
```bash
python cleanup.py
```

Oder manuell:
```bash
# Lösche Datenbank-bezogene Files
rm run.py init_db.py migrate_to_postgres.py setup_supabase.py
rm VERCEL_DEPLOYMENT.md SUPABASE_SETUP.md requirements.md
rm -rf app/models app/__pycache__

# Lösche alte Admin-Templates
rm app/templates/admin.html
rm app/templates/admin_destination_form.html
rm app/templates/admin_activities.html
rm app/templates/admin_activity_form.html
rm app/templates/admin_import.html

# Lösche alte App
rm app/app.py app/config.py

# Optional: Lösche .DS_Store Files (macOS)
find . -name ".DS_Store" -delete
```
