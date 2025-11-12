# Reise-Auswahl-App

Eine interaktive Flask-Webanwendung zur Präsentation von Reisezielen mit einem Slider-System zur Steuerung des Detailgrads der Reiseplanung.

## Features

- Übersicht aller verfügbaren Reiseziele
- Detailansicht mit interaktivem Slider
- Dynamische Anzeige von Aktivitäten basierend auf Slider-Level (0-5)
- Responsive Design mit Bootstrap 5
- SQLite-Datenbank für einfache Datenhaltung
- Admin-Bereich (in Entwicklung)

## Projektstruktur

```
/app
    /static
        /css
            style.css           # Custom Styles
        /images                 # Bilder für Destinationen und Aktivitäten
        /js
    /templates
        base.html              # Basis-Template
        index.html             # Startseite mit Destinationen
        destination.html       # Detailansicht mit Slider
        admin.html             # Admin-Bereich
    /models
        __init__.py
        destination.py         # Destination-Modell
        activity.py            # Activity-Modell
    app.py                     # Hauptanwendung
    config.py                  # Konfiguration

database.db                    # SQLite-Datenbank
init_db.py                    # Datenbank-Initialisierung
requirements.txt              # Python-Dependencies
```

## Installation

1. Repository klonen oder herunterladen

2. Virtuelle Umgebung aktivieren:
```bash
source .venv/bin/activate
```

3. Dependencies sind bereits installiert. Falls nötig:
```bash
pip install -r requirements.txt
```

4. Datenbank initialisieren (erstellt 3 Testdestinationen):
```bash
python init_db.py
```

## Anwendung starten

```bash
python run.py
```

Die App ist dann verfügbar unter: `http://localhost:5001`

**Hinweis:** Falls Port 5001 bereits belegt ist, kannst du den Port in [run.py](run.py) anpassen.

## Verwendung

### Frontend (Benutzerin)

1. **Startseite** (`/`): Zeigt alle verfügbaren Destinationen als Karten
2. **Detailansicht** (`/destination/<id>`):
   - Zeigt Informationen zur Destination
   - Interaktiver Slider (0-5) zur Steuerung des Detailgrads
   - Aktivitäten werden basierend auf Slider-Level angezeigt

### Slider-Levels

- **Level 0**: Nur Ziel angezeigt
- **Level 1**: Erste Basis-Aktivitäten
- **Level 2**: Weitere wichtige Sehenswürdigkeiten
- **Level 3**: Zusätzliche Erlebnisse
- **Level 4**: Detaillierte Tagesausflüge
- **Level 5**: Voll durchgeplant mit allen Details

### Admin-Bereich (`/admin`)

Der Admin-Bereich bietet vollständige CRUD-Funktionalität:

**Destinationen verwalten:**
- Neue Destinationen erstellen
- Bestehende Destinationen bearbeiten
- Destinationen löschen (inkl. aller zugehörigen Aktivitäten)
- Bilder hochladen

**Aktivitäten verwalten:**
- Aktivitäten für jede Destination erstellen
- Aktivitäten bearbeiten (Titel, Beschreibung, Slider-Level, Bild)
- Aktivitäten löschen
- Slider-Level (0-5) festlegen

## Datenbank-Schema

### Destination
- `id`: Primärschlüssel
- `name`: Name der Destination
- `description_short`: Kurzbeschreibung
- `image_cover`: Dateiname des Titelbildes

### Activity
- `id`: Primärschlüssel
- `destination_id`: Fremdschlüssel zu Destination
- `title`: Titel der Aktivität
- `description`: Beschreibung
- `slider_level`: Level (0-5), ab dem die Aktivität sichtbar wird
- `image_filename`: Dateiname des Bildes

## Entwicklungsphasen

- ✅ **Phase 1**: Setup & Grundgerüst
- ✅ **Phase 2**: Datenbank & Modelle
- ✅ **Phase 3**: Detailansicht & Slider
- ✅ **Phase 4**: Admin-Oberfläche
- ⏳ **Phase 5**: UI/UX-Verbesserungen (ausstehend)
- ⏳ **Phase 6**: Deployment (optional)

## Technologie-Stack

- **Backend**: Flask 3.0.0
- **ORM**: SQLAlchemy via Flask-SQLAlchemy
- **Datenbank**: SQLite
- **Frontend**: HTML5, Bootstrap 5, Vanilla JavaScript
- **Templates**: Jinja2

## Testdaten

Die App enthält 3 vorkonfigurierte Destinationen:
1. **Spanien** - Barcelona & Costa Brava (5 Aktivitäten)
2. **Island** - Feuer und Eis (5 Aktivitäten)
3. **Japan** - Tokyo & Kyoto (5 Aktivitäten)

## Nächste Schritte (Phase 5)

1. UI/UX-Verbesserungen:
   - AJAX für Slider (ohne Page-Reload)
   - Animationen optimieren
   - Lightbox für Bilder

3. Zusätzliche Features:
   - Favoritenfunktion
   - PDF-Export der Reiseplanung
   - Passwortschutz für Admin-Bereich

## Lizenz

Privates Projekt
