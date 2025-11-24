# 🌍 Reise-Auswahl-App

Eine interaktive Flask-Webanwendung zur Reiseplanung als Geschenk. Die App unterstützt zwei verschiedene Auswahlmodi: einen **Slider-Modus** für lineare Reiseplanungen und einen **Checkbox-Modus mit Punktesystem** für modulare Destinationen.

---

## 📋 Inhaltsverzeichnis

- [Features](#-features)
- [Technologie-Stack](#-technologie-stack)
- [Architektur & Aufbau](#-architektur--aufbau)
- [Installation & Setup](#-installation--setup)
- [Funktionsweise](#-funktionsweise)
- [Datenstruktur](#-datenstruktur)
- [Admin-Bereich](#-admin-bereich)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)

---

## ✨ Features

### Duale Interaktionsmodi
- **🎚️ Slider-Modus** (0-5 Level): Für lineare Reiseplanungen (z.B. Südspanien mit Flug → Auto → Strand)
- **☑️ Checkbox-Modus**: Für modulare Destinationen mit vielen Auswahlmöglichkeiten (z.B. Marrakesch)

### Checkbox-Modus Features
- **💯 Punktesystem**: Jede Destination hat ein Punkte-Budget, das verhindert, dass alles ausgewählt wird
- **🎲 "Den Rest spontan"**: Dynamische Option, die automatisch alle verbleibenden Punkte nutzt
- **📊 Live-Punktezähler**: Zeigt in Echtzeit, wie viele Punkte noch verfügbar sind
- **🚫 Auto-Deaktivierung**: Optionen werden automatisch deaktiviert, wenn Budget erschöpft ist

### Allgemeine Features
- **🔄 Live-Updates**: Keine Seitenreloads dank AJAX (Slider-Modus) und JavaScript (Checkbox-Modus)
- **📄 PDF-Export**: Ausgewählte Aktivitäten mit Bildern und Beschreibungen als PDF exportieren
- **🔐 Admin-Bereich**: Passwortgeschützte Übersicht mit umfassender Dokumentation
- **📱 Responsive Design**: Funktioniert auf Desktop, Tablet und Smartphone
- **🎨 Modernes UI**: Bootstrap 5 mit ansprechendem Design
- **📊 JSON-basiert**: Keine Datenbank erforderlich - alles in JSON-Dateien
- **☁️ Vercel-Ready**: Einfaches Deployment möglich

---

## 🛠 Technologie-Stack

### Backend
- **Flask 3.0** - Python Web Framework
  - Routing und Template-Rendering mit Jinja2
  - Session-basierte Authentifizierung
  - RESTful API-Endpunkte für dynamische Inhalte
- **python-dotenv** - Environment Variables Management

### Frontend
- **HTML5/CSS3** - Struktur und Styling
- **Bootstrap 5.3** - UI Framework
  - Grid-System für responsives Layout
  - Komponenten (Cards, Badges, Progress Bars, Alerts)
  - Modal-Dialoge und Form-Controls
- **Vanilla JavaScript** - Client-seitige Logik
  - AJAX-Requests für Slider-Updates
  - Dynamische Punkteberechnung
  - Checkbox-Zustandsverwaltung
  - PDF-Export-Funktionalität

### Datenspeicherung
- **JSON-Dateien** - Strukturierte Datenspeicherung
  - `data/destinations.json` - Reiseziele
  - `data/activities.json` - Aktivitäten und Optionen

### Deployment
- **Vercel Serverless Functions** - Cloud-Hosting (optional)
- **Gunicorn** - Production WSGI Server (optional)

### Sicherheit
- **Session-basierte Auth** - Flask Sessions mit Secret Key
- **Environment Variables** - Sensible Daten in `.env`-Datei
- **Password Protection** - Admin-Bereich geschützt

---

## 📐 Architektur & Aufbau

### Projektstruktur

```
pp/
├── app_simple.py                    # 🎯 Hauptanwendung (Flask App)
│
├── data/                            # 📊 Datenbank-Ersatz
│   ├── destinations.json            # Reiseziele mit Metadaten
│   └── activities.json              # Aktivitäten mit Sub-Items
│
├── app/
│   ├── templates/                   # 🖼️ Jinja2 Templates
│   │   ├── base.html               # Basis-Template (Header, Footer)
│   │   ├── index.html              # Startseite (Destinationsübersicht)
│   │   ├── destination.html        # Detailansicht (Slider/Checkboxen)
│   │   ├── admin_login.html        # Login-Seite für Admin
│   │   ├── admin_simple.html       # Admin-Übersicht mit Guide
│   │   ├── admin_activities_simple.html  # Aktivitätendetails
│   │   └── pdf_export.html         # Print-optimiertes PDF-Template
│   │
│   └── static/
│       ├── css/
│       │   └── style.css           # 🎨 Custom Styles
│       └── images/                  # 🖼️ Lokale Bilder (optional)
│
├── .env                             # 🔐 Environment Variables
├── .gitignore                       # Git Ignore Rules
├── requirements.txt                 # Python Dependencies
├── api/
│   └── index.py                    # Vercel Entry Point
├── vercel.json                     # Vercel Konfiguration
└── README.md                       # 📖 Diese Datei
```

### Backend-Architektur (app_simple.py)

#### 1. Initialisierung & Konfiguration
```python
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['ADMIN_PASSWORD'] = os.environ.get('ADMIN_PASSWORD')
```

#### 2. Hilfsfunktionen
- `load_destinations()` - Lädt destinations.json
- `load_activities()` - Lädt activities.json
- `get_destination_by_id(dest_id)` - Findet Destination
- `get_activities_by_destination(dest_id, slider_value)` - Filtert Aktivitäten

#### 3. Routes (Endpunkte)

**Öffentliche Routes:**
- `GET /` - Startseite mit Destination-Cards
- `GET /destination/<id>` - Detailansicht (erkennt automatisch Slider/Checkbox-Modus)
- `GET /api/destination/<id>/activities` - API für Live-Slider-Updates (AJAX)
- `POST /destination/<id>/export-pdf` - Generiert PDF-Export

**Admin-Routes (Passwortgeschützt):**
- `GET /admin/login` - Login-Formular
- `POST /admin/login` - Login-Verarbeitung
- `GET /admin/logout` - Session-Logout
- `GET /admin` - Admin-Dashboard mit Dokumentation (mit @admin_required)
- `GET /admin/destination/<id>/activities` - Aktivitäten-Details (mit @admin_required)

#### 4. Authentifizierung
```python
@admin_required
def decorated_function():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
```

### Frontend-Architektur

#### 1. Template-Hierarchie
```
base.html (Navigation, Bootstrap-Includes)
  ├─ index.html (Destination-Grid)
  ├─ destination.html (Slider ODER Checkboxen)
  ├─ admin_login.html (Login-Form)
  ├─ admin_simple.html (Tab-Navigation, Guide)
  └─ pdf_export.html (Print-CSS)
```

#### 2. JavaScript-Logik

**Slider-Modus** (destination.html):
```javascript
// AJAX-Request bei Slider-Änderung
slider.addEventListener('input', function() {
    fetch(`/api/destination/${destinationId}/activities?slider=${value}`)
        .then(response => response.json())
        .then(data => updateActivities(data.activities));
});
```

**Checkbox-Modus** (destination.html):
```javascript
// Punkteberechnung bei jeder Checkbox-Änderung
function calculateTotalPoints() {
    let total = 0;
    document.querySelectorAll('.sub-checkbox:checked').forEach(checkbox => {
        total += parseInt(checkbox.dataset.points);
    });
    return total;
}

// Spontan-Option: Dynamische Punkteanzeige
function updateSpontaneousOption() {
    const remainingPoints = pointsBudget - calculateTotalPoints();
    spontaneousBadge.textContent = remainingPoints + ' Pkt';
    spontaneousCheckbox.dataset.points = remainingPoints;
}
```

#### 3. PDF-Export
```javascript
// Sammelt ausgewählte Items und sendet POST-Request
fetch(`/destination/${id}/export-pdf`, {
    method: 'POST',
    body: formData
}).then(response => {
    // Öffnet neue Seite mit window.print() Button
    window.open(response.url);
});
```

---

## 🚀 Installation & Setup

### Voraussetzungen
- Python 3.8 oder höher
- pip (Python Package Manager)

### Schritt 1: Repository klonen oder herunterladen
```bash
cd /dein/projekt/ordner
```

### Schritt 2: Virtual Environment erstellen (empfohlen)
```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# oder
.venv\Scripts\activate     # Windows
```

### Schritt 3: Dependencies installieren
```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
Flask==3.0.0
python-dotenv==1.0.0
```

### Schritt 4: Environment Variables konfigurieren
Erstelle eine `.env`-Datei im Projektroot:
```env
# Admin-Passwort für den Admin-Bereich
ADMIN_PASSWORD=admin123

# Flask Secret Key für Sessions (ändere dies für Production!)
SECRET_KEY=your-secret-key-change-this-in-production
```

### Schritt 5: App starten
```bash
python3 app_simple.py
```

Die App läuft jetzt auf: **http://localhost:5001**

---

## ⚙️ Funktionsweise

### 1. Slider-Modus (z.B. Portugal, Spanien)

**Konzept:** Linearer Reiseplan mit steigendem Detaillierungsgrad

**Slider-Levels:**
| Level | Beschreibung | Beispiel |
|-------|--------------|----------|
| **0** | Nur Ziel | "Flug nach Lissabon" |
| **1** | Basis | + Mietauto |
| **2** | Mehr Details | + Strand |
| **3** | Zusätzliches | + Sehenswürdigkeiten |
| **4** | Strukturiert | Flug + Geführte Tour (ersetzt Auto!) |
| **5** | Komplett | + Fado-Show + Spezialessen |

**Besonderheit:** Aktivitäten können **erscheinen UND verschwinden** (nicht-additiv)

**Technischer Ablauf:**
1. User bewegt Slider → JavaScript Event
2. AJAX-Request an `/api/destination/{id}/activities?slider={value}`
3. Backend filtert `activities.json`:
   ```python
   filtered = [a for a in activities
               if a['slider_level_min'] <= value <= a['slider_level_max']]
   ```
4. JSON-Response mit gefilterten Aktivitäten
5. Frontend updated DOM ohne Reload

### 2. Checkbox-Modus (z.B. Marrakesch)

**Konzept:** Modularer Baukasten mit Punkte-Budget

**Struktur:**
- **Hauptkategorien:** Anreise, Unterkunft, Aktivitäten, Essen, etc.
- **Sub-Items:** Einzelne auswählbare Optionen
- **Pflichtoptionen:** Vorab ausgewählt (z.B. Flug)
- **Punktebudget:** Begrenzt die Auswahl (z.B. 100 Punkte)

**Punkteverteilung:**
- **0 Punkte:** Pflicht-Items (Flug, Basis-Unterkunft)
- **5-15 Punkte:** Einfache Aktivitäten (Stadtbesichtigung)
- **20-30 Punkte:** Premium-Aktivitäten (Ballonfahrt)
- **40+ Punkte:** Luxus-Optionen (Private Tour)

**Technischer Ablauf:**
1. User klickt Checkbox → JavaScript Event
2. `calculateTotalPoints()` summiert alle `data-points`-Attribute
3. Prüfung: `totalPoints <= pointsBudget`
4. Falls Budget überschritten: Checkbox automatisch deaktiviert
5. Progress Bar & Counter werden live aktualisiert

**Special: "Den Rest spontan"**
```javascript
// Berechnet verbleibende Punkte dynamisch
remainingPoints = pointsBudget - totalPoints;
spontaneousOption.points = remainingPoints;

// Wenn ausgewählt: Alle anderen Checkboxen deaktivieren
if (spontaneous.checked) {
    allCheckboxes.forEach(cb => cb.disabled = true);
}
```

### 3. PDF-Export

**Prozess:**
1. User klickt "Als PDF exportieren"
2. JavaScript sammelt alle ausgewählten Sub-Items
3. POST-Request mit JSON-Array:
   ```javascript
   [{activity_id: 1, sub_id: "1a"}, {activity_id: 2, sub_id: "2b"}]
   ```
4. Backend generiert HTML-Seite (`pdf_export.html`) mit:
   - Destination-Info
   - Ausgewählte Aktivitäten mit Bildern
   - Punkteübersicht
   - Print-optimiertes CSS
5. Neue Seite öffnet mit "Als PDF speichern" Button
6. User nutzt `window.print()` → Browser PDF-Dialog

---

## 📊 Datenstruktur

### destinations.json

```json
[
  {
    "id": 1,
    "name": "Marrakesch - Marokko",
    "description_short": "Die rote Stadt voller Leben und Kultur",
    "description_long": "Ausführliche Beschreibung...",
    "image_cover": "https://images.unsplash.com/photo-xxx?w=800",
    "selection_mode": "checkboxes",
    "points_budget": 100
  },
  {
    "id": 2,
    "name": "Portugal - Lissabon & Algarve",
    "description_short": "Sonne, Strand und Geschichte",
    "image_cover": "https://images.unsplash.com/photo-yyy?w=800",
    "selection_mode": "slider"
  }
]
```

**Felder:**
- `id` - Eindeutige ID
- `name` - Name der Destination
- `description_short` - Kurzbeschreibung für Cards
- `description_long` - Lange Beschreibung für Detailseite
- `image_cover` - Cover-Bild URL
- `selection_mode` - "slider" oder "checkboxes"
- `points_budget` - Nur für Checkbox-Modus (z.B. 100)

### activities.json

#### Slider-Modus Format:
```json
{
  "id": 1,
  "destination_id": 2,
  "title": "Mietauto & flexible Erkundung",
  "description": "7 Tage Mietauto, Vollkasko...",
  "slider_level_min": 1,
  "slider_level_max": 3,
  "image_filename": "https://images.unsplash.com/photo-zzz?w=800"
}
```

#### Checkbox-Modus Format:
```json
{
  "id": 1,
  "destination_id": 1,
  "title": "Anreise & Unterkunft",
  "sub_items": [
    {
      "id": "1a",
      "title": "Direktflug nach Marrakesch",
      "description": "Hin- und Rückflug ab Deutschland",
      "points": 0,
      "mandatory": true,
      "default_selected": true,
      "image_filename": "https://images.unsplash.com/photo-aaa?w=400"
    },
    {
      "id": "1b",
      "title": "Riad im Herzen der Medina",
      "description": "4 Nächte in traditionellem Riad",
      "points": 30,
      "mandatory": false,
      "image_filename": "https://images.unsplash.com/photo-bbb?w=400"
    }
  ]
}
```

**Special: Spontan-Option**
```json
{
  "id": "flex1",
  "title": "Den Rest spontan",
  "description": "Die verbleibenden Punkte flexibel vor Ort verwenden",
  "points": 0,
  "is_spontaneous": true,
  "image_filename": "https://images.unsplash.com/photo-ddd?w=400"
}
```

---

## 👨‍💼 Admin-Bereich

### Zugang
**URL:** http://localhost:5001/admin
**Passwort:** Definiert in `.env` (Standard: `admin123`)

### Features
1. **Dashboard:** Übersicht aller Destinationen mit Statistiken
2. **Aktivitäten-Details:** Klick auf Destination zeigt alle Aktivitäten
3. **Umfassende Dokumentation:** 3-Tab-Guide erklärt JSON-Struktur
   - Tab 1: destinations.json Struktur
   - Tab 2: activities.json mit Beispielen
   - Tab 3: Punktesystem Best Practices

### Passwort ändern
```env
# In .env Datei:
ADMIN_PASSWORD=dein-neues-passwort
```
Danach App neu starten.

---

## ☁️ Deployment

### Vercel (Empfohlen)

1. **GitHub Repository erstellen** und Code pushen
2. **Vercel-Account** erstellen (vercel.com)
3. **Repository importieren** in Vercel
4. **Environment Variables** setzen:
   - `ADMIN_PASSWORD=dein-passwort`
   - `SECRET_KEY=zufällige-lange-zeichenfolge`
5. **Deploy** - Fertig!

**Wichtig:** Die `vercel.json` und `api/index.py` sind bereits konfiguriert.

### Heroku

```bash
# Procfile erstellen:
echo "web: gunicorn app_simple:app" > Procfile

# Deployment:
heroku create deine-app-name
git push heroku main
heroku config:set ADMIN_PASSWORD=dein-passwort
heroku config:set SECRET_KEY=zufälliger-key
```

### Lokaler Production-Server

```bash
# Gunicorn installieren:
pip install gunicorn

# Server starten:
gunicorn -w 4 -b 0.0.0.0:8000 app_simple:app
```

---

## 🐛 Troubleshooting

### Problem: Port bereits belegt
```bash
# Prüfe welcher Prozess Port 5001 nutzt:
lsof -ti:5001

# Töte den Prozess:
lsof -ti:5001 | xargs kill -9

# Starte App neu:
python3 app_simple.py
```

### Problem: JSON Syntax Error
- Validiere JSON auf [JSONLint.com](https://jsonlint.com)
- In VS Code: `Shift+Alt+F` (Format Document)
- Achte auf:
  - Fehlende Kommas zwischen Objekten
  - Falsche Klammern `{}` vs `[]`
  - Trailing Commas (letztes Element darf kein Komma haben)

### Problem: Admin-Login funktioniert nicht
```bash
# Prüfe .env Datei:
cat .env

# Stelle sicher, dass python-dotenv installiert ist:
pip install python-dotenv

# App neu starten (um .env zu laden):
python3 app_simple.py
```

### Problem: Bilder werden nicht angezeigt
- URLs müssen mit `http://` oder `https://` beginnen
- Teste URL direkt im Browser
- Für Unsplash: Nutze `?w=800` für optimale Größe
- CORS-Fehler? Nutze CDN-URLs oder Unsplash

### Problem: PDF-Export zeigt keine Bilder
- Bilder müssen von öffentlichen URLs erreichbar sein
- Teste im Browser: Inkognito-Modus → Bild-URL aufrufen
- OneDrive/Dropbox: Nutze Direct Download Links

### Problem: Punkte-Counter funktioniert nicht
- Öffne Browser Developer Tools (F12)
- Schaue in Console nach JavaScript-Fehlern
- Prüfe ob `data-points` Attribute in HTML vorhanden sind

### Problem: Vercel Deployment schlägt fehl
```bash
# Prüfe vercel.json:
cat vercel.json

# Prüfe api/index.py:
cat api/index.py

# Lokaler Test der Vercel-Funktion:
vercel dev
```

---

## 📚 Weiterführende Links

- **Flask Dokumentation:** https://flask.palletsprojects.com/
- **Bootstrap 5 Docs:** https://getbootstrap.com/docs/5.3/
- **Jinja2 Template Guide:** https://jinja.palletsprojects.com/
- **Vercel Deployment:** https://vercel.com/docs
- **Unsplash API:** https://unsplash.com/developers

---

## 🔒 Sicherheitshinweise

### Production Deployment
1. **Ändere SECRET_KEY:** Nutze einen zufälligen, langen String
   ```python
   # Generiere mit:
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
2. **Ändere ADMIN_PASSWORD:** Nutze ein starkes, einzigartiges Passwort
3. **Debug Mode deaktivieren:** In Production `debug=False` setzen
4. **HTTPS erzwingen:** Stelle sicher, dass Hosting-Provider HTTPS nutzt
5. **Rate Limiting:** Für Login-Route implementieren (z.B. Flask-Limiter)

### Best Practices
- `.env` niemals in Git committen (steht in `.gitignore`)
- Regelmäßige Backups der JSON-Dateien erstellen
- Admin-Passwort regelmäßig ändern
- Bei Vercel: Environment Variables im Dashboard setzen
