# Vercel Deployment Anleitung

## Voraussetzungen

1. **Vercel Account** - Erstelle einen Account auf [vercel.com](https://vercel.com)
2. **Vercel Postgres** - Datenbank für deine App

## Schritt-für-Schritt Anleitung

### 1. Vercel Postgres Datenbank erstellen

1. Gehe zu deinem Vercel Dashboard
2. Wähle "Storage" → "Create Database"
3. Wähle "Postgres" aus
4. Erstelle die Datenbank
5. Nach der Erstellung erhältst du die `POSTGRES_URL` Connection String

### 2. Projekt zu Vercel deployen

#### Option A: Via Vercel CLI

```bash
# Installiere Vercel CLI (falls noch nicht installiert)
npm i -g vercel

# Login bei Vercel
vercel login

# Deploye das Projekt
vercel
```

#### Option B: Via GitHub

1. Pushe dein Projekt zu GitHub
2. Gehe zu [vercel.com/new](https://vercel.com/new)
3. Importiere dein GitHub Repository
4. Vercel erkennt automatisch die Python-App

### 3. Umgebungsvariablen setzen

In deinem Vercel Projekt:

1. Gehe zu "Settings" → "Environment Variables"
2. Füge folgende Variablen hinzu:

```
DATABASE_URL = [Deine Vercel Postgres Connection String]
SECRET_KEY = [Generiere einen sicheren Secret Key]
```

**Secret Key generieren:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Datenbank initialisieren

Nachdem das Deployment erfolgreich war:

```bash
# Setze die DATABASE_URL lokal als Umgebungsvariable
export DATABASE_URL="postgresql://..."

# Führe das Migrations-Skript aus
python migrate_to_postgres.py
```

**Alternativ:** Nutze Vercel CLI um das Skript auf Vercel auszuführen:

```bash
vercel env pull .env.local
source .env.local
python migrate_to_postgres.py
```

## Wichtige Hinweise

### File Uploads funktionieren nicht auf Vercel

Vercel Serverless Functions haben ein **temporäres Dateisystem**. Hochgeladene Bilder gehen bei jedem Deployment verloren.

**Lösungen:**

1. **Vercel Blob Storage** (empfohlen)
   - Nutze [@vercel/blob](https://vercel.com/docs/storage/vercel-blob)
   - Bilder werden in Cloud Storage gespeichert

2. **Cloudinary** oder **AWS S3**
   - Externe Image Hosting Services

3. **Für Demo/Test:**
   - Verwende Placeholder URLs (z.B. placeholder.com)
   - Oder committe Beispielbilder direkt ins Repository unter `app/static/images/`

### Cold Starts

Die erste Anfrage nach längerer Inaktivität kann 1-3 Sekunden dauern. Das ist normal für Serverless Functions.

### Debugging

Logs einsehen:
```bash
vercel logs [deployment-url]
```

Oder im Vercel Dashboard unter "Deployments" → [Dein Deployment] → "Logs"

## Troubleshooting

### Error: "Module not found"
- Stelle sicher, dass alle Dependencies in `requirements.txt` aufgeführt sind
- Versuche ein neues Deployment: `vercel --prod`

### Error: "Database connection failed"
- Überprüfe die `DATABASE_URL` Umgebungsvariable
- Stelle sicher, dass die Postgres-Datenbank läuft
- Vercel Postgres URLs beginnen mit `postgres://` - die App konvertiert sie automatisch zu `postgresql://`

### Error: "Function exceeded timeout"
- Vercel Free Plan: 10 Sekunden Timeout
- Vercel Pro Plan: 60 Sekunden Timeout
- Optimiere langsame Datenbankabfragen

## Lokale Entwicklung mit PostgreSQL

Wenn du lokal mit PostgreSQL entwickeln möchtest:

```bash
# Installiere PostgreSQL lokal
brew install postgresql  # macOS
# oder
sudo apt-get install postgresql  # Linux

# Erstelle eine Datenbank
createdb reiseplanung

# Setze DATABASE_URL
export DATABASE_URL="postgresql://localhost/reiseplanung"

# Initialisiere die Datenbank
python migrate_to_postgres.py

# Starte die App
python run.py
```

## Alternative: SQLite für lokale Entwicklung

Die App nutzt automatisch SQLite, wenn keine `DATABASE_URL` gesetzt ist:

```bash
# Keine DATABASE_URL setzen
python init_db.py
python run.py
```

**Wichtig:** SQLite funktioniert **nicht** auf Vercel!
