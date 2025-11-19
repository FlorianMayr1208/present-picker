# 🌍 Reise-Auswahl-App

Eine interaktive Flask-Webanwendung zur Reiseplanung mit dynamischem Slider-System.

## ✨ Features

- 🎚️ **Dynamischer Slider** (0-5 Level) zur Steuerung der Reise-Details
- 🔄 **Live-Updates** ohne Seitenreload (AJAX)
- 📊 **JSON-basierte Datenspeicherung** - Keine Datenbank nötig!
- 🖼️ **Externe Bilder** von Unsplash, OneDrive, etc.
- 🎨 **Modernes, farbenfrohes Design** mit Gradients
- 📱 **Responsive** - Funktioniert auf Desktop und Mobile
- ☁️ **Vercel-Ready** - Deployt in Sekunden

## 🚀 Quick Start

### Lokal starten

```bash
# Aktiviere Virtual Environment
source .venv/bin/activate

# Starte die App
python app_simple.py
```

Öffne: **http://localhost:5001**

### Vercel Deployment

```bash
# Pushe zu GitHub
git add .
git commit -m "Deploy to Vercel"
git push

# Vercel erkennt automatisch die Konfiguration
# Gehe zu vercel.com und importiere dein Repository
```

**Keine Environment Variables oder Datenbank nötig!** ✅

## 📁 Projektstruktur

```
pp/
├── app_simple.py              # 🎯 Hauptanwendung
├── data/
│   ├── destinations.json      # 📍 Reiseziele
│   └── activities.json        # 🎭 Aktivitäten
├── app/
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html         # Startseite
│   │   ├── destination.html   # Detail-Ansicht mit Slider
│   │   ├── admin_simple.html  # Admin-Übersicht
│   │   └── admin_activities_simple.html
│   └── static/
│       └── css/
│           └── style.css      # 🎨 Farbenfrohes Design
├── api/
│   └── index.py              # Vercel Entry Point
├── requirements.txt          # Python Dependencies
├── vercel.json              # Vercel Config
└── README.md                # 📖 Diese Datei
```

## 📝 Daten bearbeiten

### Destinationen (`data/destinations.json`)

```json
{
  "id": 1,
  "name": "Spanien - Barcelona & Costa Brava",
  "description_short": "Entdecke die lebendige Kultur...",
  "image_cover": "https://images.unsplash.com/photo-xxx?w=800"
}
```

### Aktivitäten (`data/activities.json`)

```json
{
  "id": 1,
  "destination_id": 1,
  "title": "Flug nach Barcelona",
  "description": "Direktflug nach Barcelona...",
  "slider_level_min": 0,
  "slider_level_max": 5,
  "image_filename": "https://images.unsplash.com/photo-xxx?w=800"
}
```

**Wichtig:**
- `slider_level_min`: Ab welchem Level ist die Aktivität sichtbar (0-5)
- `slider_level_max`: Bis zu welchem Level ist die Aktivität sichtbar (0-5)

### Beispiel: Nicht-additives Slider-System

```json
// Mietauto - Nur bei Level 1-3 (flexibel)
{
  "id": 2,
  "title": "Mietauto & flexibles Erkunden",
  "slider_level_min": 1,
  "slider_level_max": 3
}

// Geführte Tour - Nur bei Level 4-5 (strukturiert)
// Ersetzt das Mietauto!
{
  "id": 3,
  "title": "Barcelona City Tour (geführt)",
  "slider_level_min": 4,
  "slider_level_max": 5
}
```

## 🖼️ Bilder verwenden

### Option 1: Unsplash (kostenlos)
```
https://images.unsplash.com/photo-xxxxxxx?w=800
```

### Option 2: OneDrive
1. Lade Bilder in OneDrive hoch
2. Rechtsklick → Teilen → "Jeder mit diesem Link"
3. Konvertiere zu Direct Link:
   - Tool: [OneDrive Direct Link Generator](https://onedrive.live.com/about/en-us/download/)

### Option 3: Andere Services
- Google Drive (Public Access)
- Dropbox Public Links
- Cloudinary
- ImgBB

**Tipp:** Verwende Bilder mit ~800px Breite für optimale Performance.

## 🎯 Slider-System erklärt

Der Slider steuert, welche Aktivitäten angezeigt werden:

| Level | Beschreibung | Beispiel |
|-------|--------------|----------|
| **0** | Nur Ziel | "Flug nach Barcelona" |
| **1** | Basis | Flug + Mietauto |
| **2** | Mehr Details | + Strand |
| **3** | Zusätzliches | + Sehenswürdigkeiten |
| **4** | Strukturiert | Flug + Geführte Tour (kein Auto mehr!) |
| **5** | Komplett | + Flamenco Show |

Das Besondere: Aktivitäten können **erscheinen UND verschwinden**!

## 👨‍💼 Admin-Bereich

Öffne `/admin` für eine Übersicht aller Destinationen und Aktivitäten.

**Hinweis:** Der Admin-Bereich ist Read-Only. Zum Bearbeiten öffne die JSON-Dateien direkt in einem Text-Editor.

## 🛠️ Technologie

- **Backend:** Flask 3.0
- **Frontend:** Bootstrap 5, Vanilla JavaScript
- **Daten:** JSON Files (kein Setup nötig!)
- **Bilder:** Externe URLs
- **Deployment:** Vercel Serverless Functions
- **Design:** CSS3 mit Gradients & Animationen

## 🔧 Entwicklung

### Dependencies installieren

```bash
pip install -r requirements.txt
```

### Port ändern

In `app_simple.py` Zeile am Ende:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Ändere 5001
```

### Debug Mode

Debug Mode ist standardmäßig aktiviert (`debug=True`). Für Production:
```python
app.run(debug=False, host='0.0.0.0', port=5001)
```

## 📊 Datengrenzen

Diese JSON-basierte Lösung eignet sich perfekt für:
- ✅ Bis zu **50 Destinationen**
- ✅ Bis zu **500 Aktivitäten** gesamt
- ✅ **Schnelle Performance** (alles im RAM)
- ✅ **Einfache Backups** (einfach JSON-Files kopieren)

Für größere Projekte (> 1000 Einträge) empfiehlt sich eine Datenbank.

## 🐛 Troubleshooting

### Problem: Seite lädt nicht

```bash
# Prüfe ob Port bereits belegt ist
lsof -ti:5001 | xargs kill -9

# Starte neu
python app_simple.py
```

### Problem: JSON Syntax Error

Validiere deine JSON-Dateien:
- [JSONLint](https://jsonlint.com)
- VS Code: Rechtsklick → "Format Document"

### Problem: Bilder werden nicht angezeigt

- URLs müssen mit `http://` oder `https://` beginnen
- Teste URLs direkt im Browser
- Für OneDrive: Nutze Direct Download Links

### Problem: Änderungen werden nicht angezeigt (Vercel)

```bash
# Pushe Änderungen
git add .
git commit -m "Update data"
git push

# Vercel deployt automatisch neu (~30 Sekunden)
```

## 📖 Weitere Dokumentation

- [README_SIMPLE.md](README_SIMPLE.md) - Ausführliche Dokumentation
- [CLEANUP.md](CLEANUP.md) - Was wurde aufgeräumt

## 🎉 Credits

- Bilder: [Unsplash](https://unsplash.com)
- Icons: Bootstrap Icons
- Framework: Flask & Bootstrap

---

**Entwickelt mit ❤️ und Claude Code**

Viel Erfolg mit deiner Reise-App! 🌍✈️
