# Reise-Auswahl-App - Simplified Version (Ohne Datenbank)

Diese Version nutzt **JSON-Dateien** statt einer Datenbank und funktioniert perfekt auf **Vercel** und lokal!

## ✨ Features

- ✅ Keine Datenbank nötig
- ✅ Daten in einfachen JSON-Dateien
- ✅ Bilder von externen URLs (Unsplash, OneDrive, etc.)
- ✅ Funktioniert auf Vercel ohne zusätzliche Services
- ✅ Einfach zu bearbeiten
- ✅ Funktioniert lokal und in Production identisch

## 📁 Projektstruktur

```
pp/
├── app_simple.py           # Hauptanwendung (OHNE Datenbank)
├── data/
│   ├── destinations.json   # Alle Destinationen
│   └── activities.json     # Alle Aktivitäten
├── app/
│   ├── templates/          # HTML Templates
│   └── static/             # CSS, JS
└── api/
    └── index.py           # Vercel Entry Point
```

## 🚀 Lokale Entwicklung

```bash
# Stoppe alte Server
lsof -ti:5001 | xargs kill -9

# Starte die vereinfachte App
python app_simple.py
```

Öffne: http://localhost:5001

## 📝 Daten bearbeiten

### Destinations hinzufügen/bearbeiten

Öffne `data/destinations.json`:

```json
[
  {
    "id": 1,
    "name": "Spanien - Barcelona & Costa Brava",
    "description_short": "Entdecke die lebendige Kultur...",
    "image_cover": "https://images.unsplash.com/photo-xxx?w=800"
  }
]
```

### Aktivitäten hinzufügen/bearbeiten

Öffne `data/activities.json`:

```json
[
  {
    "id": 1,
    "destination_id": 1,
    "title": "Flug nach Barcelona",
    "description": "Direktflug nach Barcelona...",
    "slider_level_min": 0,
    "slider_level_max": 5,
    "image_filename": "https://images.unsplash.com/photo-xxx?w=800"
  }
]
```

**Wichtig:**
- `id`: Eindeutige Nummer für jede Aktivität
- `destination_id`: Muss mit einer Destination-ID übereinstimmen
- `slider_level_min`: Bei welchem Level wird die Aktivität sichtbar (0-5)
- `slider_level_max`: Bei welchem Level verschwindet die Aktivität (0-5)

## 🖼️ Bilder verwenden

### Option 1: Unsplash (Empfohlen für Demo)

Verwende Unsplash URLs direkt:
```
https://images.unsplash.com/photo-1583422409516-2895a77efded?w=800
```

### Option 2: OneDrive Share Links

1. Lade Bilder in OneDrive hoch
2. Rechtsklick → Teilen → Link kopieren
3. Konvertiere zu Direct Link:
   ```
   Original: https://1drv.ms/i/s!xxxxx
   Direct:   https://onedrive.live.com/download?cid=xxx&resid=xxx&authkey=xxx
   ```

### Option 3: Andere Cloud Storage

- Google Drive (mit Public Access)
- Dropbox Public Links
- Cloudinary
- ImgBB

**Tipp:** Für beste Performance, verwende Bilder mit ~800px Breite (nicht größer).

## 🌐 Vercel Deployment

### 1. Pushe zu GitHub

```bash
git add .
git commit -m "Simplified version without database"
git push
```

### 2. Deploye auf Vercel

1. Gehe zu [vercel.com/new](https://vercel.com/new)
2. Importiere dein GitHub Repository
3. **Keine Environment Variables nötig!**
4. Klicke auf "Deploy"

### 3. Fertig! 🎉

Die App funktioniert sofort ohne zusätzliche Konfiguration.

## 🔧 Troubleshooting

### Problem: Bilder werden nicht angezeigt

**Lösung:**
- Stelle sicher, dass die Bild-URLs mit `http://` oder `https://` beginnen
- Teste die URL in einem Browser - sie sollte das Bild direkt anzeigen
- Für OneDrive: Verwende den Direct Download Link, nicht den Share Link

### Problem: Änderungen werden nicht angezeigt

**Lösung:**
- Speichere die JSON-Datei
- Lade die Browser-Seite neu (F5)
- Für Vercel: Pushe die Änderungen zu GitHub, Vercel deployt automatisch neu

### Problem: JSON Syntax Error

**Lösung:**
- Prüfe ob alle Kommas richtig gesetzt sind
- Verwende einen JSON Validator: [jsonlint.com](https://jsonlint.com)
- Achte auf doppelte Anführungszeichen (`"` nicht `'`)

## 📊 Admin-Bereich

Öffne `/admin` um eine Übersicht aller Destinationen und Aktivitäten zu sehen.

**Hinweis:** Der Admin-Bereich ist Read-Only. Zum Bearbeiten öffne die JSON-Dateien direkt.

## 🆚 Unterschied zur DB-Version

| Feature | DB Version | Simple Version |
|---------|-----------|----------------|
| Datenbank | PostgreSQL/SQLite | JSON-Dateien |
| Vercel Setup | Kompliziert | Einfach |
| Bilder | Upload nötig | Externe URLs |
| Bearbeiten | Web UI | Text Editor |
| Performance | Gut | Sehr gut |
| Skalierung | Unbegrenzt | Bis ~100 Einträge |

## 💡 Best Practices

### JSON-Dateien bearbeiten

1. **Backup erstellen** vor großen Änderungen
2. **JSON Validator** verwenden um Fehler zu vermeiden
3. **IDs nicht wiederverwenden** - immer neue IDs für neue Einträge
4. **Konsistente Formatierung** - verwende einen Code-Editor mit JSON-Support

### Bild-URLs

1. **Optimierte Größe**: ~800px Breite ist ideal
2. **HTTPS verwenden**: Nicht HTTP (viele Browser blockieren gemischten Content)
3. **Stabile URLs**: Verwende permanente Links, keine temporären Share-Links
4. **Backup**: Speichere Bilder auch lokal als Backup

## 🔄 Zurück zur DB-Version

Falls du später doch eine Datenbank verwenden möchtest:

```bash
python run.py  # Startet die originale Version mit DB
```

## 📞 Support

Bei Fragen oder Problemen:
1. Prüfe diese README
2. Validiere deine JSON-Dateien
3. Schaue in die Browser-Konsole für Fehler (F12)

---

**Viel Erfolg mit deiner Reise-App! 🌍✈️**
