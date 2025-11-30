# Punktebasierte Reiseplanung App

Eine Flask-basierte Web-Anwendung zur interaktiven Reiseplanung mit Punktesystem. Wähle deine Destination, erkunde Aktivitäten und plane deine perfekte Reise innerhalb deines Budgets.

## Features

- **Punktebasiertes System**: Jede Aktivität hat einen Punktwert, der deinem Budget entspricht
- **Dynamische Filterung**: Aktivitäten werden je nach Budget-Level sichtbar/unsichtbar
- **Kategorisierung**: Aktivitäten sind in sinnvolle Kategorien gruppiert (Essen, Kultur, Ausflüge, etc.)
- **Geschenke-Tracking**: Aktivitäten können als Geschenke von Eltern oder Freunden markiert werden
- **Spontanitäts-Option**: Flexibilität für ungeplante Aktivitäten vor Ort
- **JSON-basiert**: Einfache Datenverwaltung ohne Datenbank
- **Vercel-ready**: Funktioniert perfekt auf Vercel

## Projektstruktur

```
pp/
├── app.py                  # Hauptanwendung
├── data/
│   ├── destinations.json   # Destinationen
│   └── activities.json     # Aktivitäten mit Kategorien
├── app/
│   ├── templates/          # HTML Templates
│   └── static/             # CSS, JS
└── api/
    └── index.py           # Vercel Entry Point
```

## Datenstruktur

### Destinations

Jede Destination hat:
- `id`: Eindeutige ID
- `name`: Name der Destination
- `description_short`: Kurzbeschreibung
- `image_cover`: Cover-Bild URL
- `total_points`: Gesamtbudget in Punkten

### Activities

Aktivitäten sind in **Kategorien** gruppiert (z.B. "Essen & Kulinarik", "Kultur & Must-Sees", "Ausflüge").

Jede Kategorie (Top-Level Activity) hat:
- `id`: Eindeutige Kategorie-ID
- `destination_id`: Zugehörige Destination
- `title`: Kategorie-Name
- `description`: Kategorie-Beschreibung
- `image_filename`: Kategorie-Bild
- `default_selected`: Ob Kategorie standardmäßig ausgewählt ist
- `sub_items`: Array von einzelnen Aktivitäten

Jede Aktivität (Sub-Item) hat:
- `id`: Eindeutige ID (z.B. "2a", "2b")
- `title`: Name der Aktivität
- `description`: Beschreibung
- `points`: Punktekosten
- `default_selected`: Standard-Auswahl
- `mandatory`: Ob Aktivität verpflichtend ist
- `from_parents`: Als Geschenk von Eltern markiert
- `from_friends`: Als Geschenk von Freunden markiert
- `is_spontaneous`: Für spontane Aktivitäten vor Ort
- `image_filename`: Bild-URL
- `slider_level_min`: Ab welchem Level sichtbar (0-5, optional)
- `slider_level_max`: Bis welchem Level sichtbar (0-5, optional)

## Lokale Entwicklung

### Installation

```bash
# Python Virtual Environment erstellen
python -m venv .venv

# Aktivieren
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Dependencies installieren
pip install -r requirements.txt
```

### Starten

```bash
# Alte Server stoppen (falls nötig)
lsof -ti:5001 | xargs kill -9

# App starten
python app.py
```

Öffne: http://localhost:5001

## Daten bearbeiten

### Neue Destination hinzufügen

Bearbeite `data/destinations.json`:

```json
{
  "id": 4,
  "name": "Paris, Frankreich",
  "description_short": "Die Stadt der Liebe",
  "image_cover": "https://images.unsplash.com/photo-xxx?w=800",
  "total_points": 100
}
```

### Neue Aktivitäts-Kategorie hinzufügen

Bearbeite `data/activities.json`:

```json
{
  "id": 5,
  "destination_id": 1,
  "title": "Wellness & Entspannung",
  "description": "Erholung und Spa",
  "image_filename": "https://images.unsplash.com/photo-xxx?w=800",
  "default_selected": false,
  "sub_items": [
    {
      "id": "5a",
      "title": "Hamam-Besuch",
      "description": "Traditionelles türkisches Bad",
      "points": 30,
      "default_selected": false,
      "mandatory": false,
      "from_parents": false,
      "is_spontaneous": false,
      "image_filename": "https://images.unsplash.com/photo-xxx?w=600"
    }
  ]
}
```

### Aktivität als Geschenk markieren

```json
{
  "id": "2a",
  "title": "Ballonfahrt",
  "points": 35,
  "from_parents": true,    // Geschenk von Eltern
  "from_friends": false,
  ...
}
```

### Budget-Level System

Aktivitäten können je nach Budget-Level ein-/ausgeblendet werden:

```json
{
  "id": "20c",
  "title": "Cocktail auf Rooftop-Bar",
  "points": 15,
  "slider_level_min": 3,  // Sichtbar ab Level 3
  "slider_level_max": 5,  // Sichtbar bis Level 5
  ...
}
```

Wenn `slider_level_min` und `slider_level_max` fehlen, ist die Aktivität immer sichtbar.

## Bilder

### Empfohlene Quellen

1. **Unsplash** (kostenlos, hochqualitativ)
   ```
   https://images.unsplash.com/photo-xxx?w=800
   ```

2. **OneDrive** (eigene Bilder)
   - Datei hochladen → Teilen → Direct Download Link verwenden

3. **Andere Cloud-Dienste**
   - Google Drive (Public Access)
   - Cloudinary
   - ImgBB

**Best Practices:**
- Breite: ~800px für Cover, ~600px für Aktivitäten
- Format: JPEG oder WebP
- HTTPS verwenden (kein HTTP)

## Vercel Deployment

### Vorbereitung

Die App ist bereits für Vercel konfiguriert:
- `vercel.json`: Routing-Konfiguration
- `api/index.py`: Serverless Function Entry Point
- `requirements.txt`: Python Dependencies

### Deployment

1. **GitHub Repository erstellen und pushen**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push
   ```

2. **Auf Vercel deployen**
   - Gehe zu [vercel.com/new](https://vercel.com/new)
   - Importiere dein GitHub Repository
   - Keine Environment Variables nötig
   - Deploy

3. **Fertig!** Die App läuft auf `https://dein-projekt.vercel.app`

### Updates deployen

```bash
git add .
git commit -m "Update activities"
git push
```

Vercel deployed automatisch nach jedem Push.

## Admin-Bereich

Öffne `/admin` für eine Übersicht aller Destinationen und Aktivitäten.

**Hinweis:** Der Admin-Bereich ist Read-Only. Bearbeite die JSON-Dateien direkt.

## API Endpoints

- `GET /` - Startseite mit Destination-Auswahl
- `GET /destination/<id>` - Destination-Detail mit Aktivitäten
- `POST /api/calculate` - Berechne Gesamtpunkte
- `POST /api/generate-pdf` - PDF-Export der Auswahl
- `GET /admin` - Admin-Übersicht

## Troubleshooting

### Bilder werden nicht angezeigt

- Prüfe ob URL mit `https://` beginnt
- Teste URL direkt im Browser
- Bei OneDrive: Direct Download Link verwenden

### JSON Syntax Error

- Verwende [jsonlint.com](https://jsonlint.com) zum Validieren
- Achte auf korrekte Kommas und Anführungszeichen
- IDs in `sub_items` sollten Strings sein (z.B. `"2a"`)

### Port bereits belegt

```bash
lsof -ti:5001 | xargs kill -9
python app.py
```

### Änderungen werden nicht angezeigt

- Speichere JSON-Datei
- Browser neuladen (F5 oder Cmd+R)
- Bei Vercel: Git Push triggert automatisches Deployment

## Best Practices

### JSON-Dateien bearbeiten

1. **Backup erstellen** vor großen Änderungen
2. **JSON Validator** verwenden
3. **Konsistente IDs**: Keine doppelten IDs verwenden
4. **Code-Editor** mit JSON-Support nutzen (VS Code, Sublime, etc.)

### Aktivitäten strukturieren

1. **Kategorien sinnvoll wählen**: Essen, Kultur, Ausflüge, etc.
2. **Punkte realistisch setzen**: Entsprechend der echten Kosten
3. **Beschreibungen**: Ausführlich aber prägnant
4. **Bilder**: Hochqualitativ und thematisch passend

### Geschenke-System

- `from_parents`: Aktivitäten von Eltern finanziert
- `from_friends`: Aktivitäten von Freunden finanziert
- Diese werden im Frontend speziell markiert

## Support

Bei Fragen oder Problemen:
1. Prüfe diese README
2. Validiere JSON-Dateien
3. Schaue Browser-Konsole (F12)

---

**Viel Erfolg mit deiner Reiseplanung! 🌍✈️**
