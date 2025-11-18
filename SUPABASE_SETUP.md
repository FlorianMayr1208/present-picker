# Supabase + Vercel Deployment Guide

## 1. Supabase Projekt erstellen

1. Gehe zu [supabase.com](https://supabase.com) und erstelle einen Account
2. Erstelle ein neues Projekt
3. Warte bis das Projekt vollständig eingerichtet ist (~2 Minuten)

## 2. Connection String finden

1. In deinem Supabase Dashboard, gehe zu **Settings** → **Database**
2. Scrolle zu **Connection String** → **URI**
3. Wähle **Connection pooling** mit **Transaction Mode**
4. Kopiere den Connection String (sieht so aus):
   ```
   postgresql://postgres.xxxxxxxxxxxxx:[YOUR-PASSWORD]@aws-0-eu-central-1.pooler.supabase.com:6543/postgres
   ```
5. Ersetze `[YOUR-PASSWORD]` mit deinem Datenbank-Passwort

## 3. Lokale Datenbank-Initialisierung

```bash
# Navigiere zum Projekt-Verzeichnis
cd /Users/flo/Desktop/pp

# Aktiviere Virtual Environment
source .venv/bin/activate

# Installiere Dependencies (falls noch nicht gemacht)
pip install -r requirements.txt

# Setze die DATABASE_URL Umgebungsvariable
export DATABASE_URL="postgresql://postgres.xxxxx:[YOUR-PASSWORD]@...pooler.supabase.com:6543/postgres"

# Führe das Setup-Skript aus
python setup_supabase.py
```

Das Skript wird:
- Die Verbindung testen
- Tabellen erstellen (`destinations` und `activities`)
- Testdaten hinzufügen (3 Destinationen mit je 5 Aktivitäten)

## 4. Vercel Deployment

### Option A: Via GitHub (Empfohlen)

1. **Pushe dein Projekt zu GitHub:**
   ```bash
   git add .
   git commit -m "Add Supabase support"
   git push
   ```

2. **Importiere in Vercel:**
   - Gehe zu [vercel.com/new](https://vercel.com/new)
   - Wähle dein GitHub Repository
   - Klicke auf "Import"

3. **Setze Environment Variables in Vercel:**
   - Während des Imports oder später unter **Settings** → **Environment Variables**
   - Füge hinzu:
     ```
     DATABASE_URL = postgresql://postgres.xxx:[PASSWORD]@...pooler.supabase.com:6543/postgres
     SECRET_KEY = [generiere einen mit: python -c "import secrets; print(secrets.token_hex(32))"]
     ```

4. **Deploye:**
   - Klicke auf "Deploy"
   - Warte auf das Deployment (~1-2 Minuten)

### Option B: Via Vercel CLI

```bash
# Installiere Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploye
vercel

# Folge den Prompts und setze die Environment Variables wenn gefragt
```

## 5. Troubleshooting

### Problem: "Invalid DSN" Fehler

**Symptom:** `sqlalchemy.exc.ProgrammingError: invalid dsn: invalid connection option "supa"`

**Lösung:** Stelle sicher, dass du den **Connection Pooling** URI verwendest, nicht den direkten Connection String. Der Pooling-URI sieht so aus:
```
postgresql://postgres.xxxxx:[PASSWORD]@aws-0-region.pooler.supabase.com:6543/postgres
```

**NICHT den Direct Connection String verwenden:**
```
postgresql://postgres:[PASSWORD]@db.xxxxx.supabase.co:5432/postgres?pgbouncer=true&...
```

### Problem: Connection Timeout

**Lösung:**
1. Stelle sicher, dass du **Transaction Mode** verwendest (nicht Session Mode)
2. Überprüfe, dass Port 6543 verwendet wird (nicht 5432)

### Problem: "Relation does not exist"

**Lösung:** Die Tabellen wurden nicht erstellt. Führe `python setup_supabase.py` lokal aus.

### Problem: Bilder werden nicht angezeigt

**Wichtig:** Vercel Serverless Functions haben **kein persistentes Dateisystem**. Hochgeladene Bilder gehen verloren.

**Lösungen:**
1. **Supabase Storage** (Empfohlen für Produktion):
   - Nutze Supabase Storage für Image Uploads
   - Siehe: [supabase.com/docs/guides/storage](https://supabase.com/docs/guides/storage)

2. **Für Demo/Test:**
   - Committe Beispielbilder direkt ins Git Repository unter `app/static/images/`
   - Diese werden mit deployed

## 6. Lokale Entwicklung

### Mit Supabase (wie Produktion):
```bash
export DATABASE_URL="postgresql://..."
python run.py
```

### Mit SQLite (einfacher für lokale Tests):
```bash
# Keine DATABASE_URL setzen
python init_db.py
python run.py
```

## 7. Database Management

### Datenbank zurücksetzen (VORSICHT!):
```sql
-- In Supabase SQL Editor
DROP TABLE IF EXISTS activities CASCADE;
DROP TABLE IF EXISTS destinations CASCADE;
```

Dann führe `python setup_supabase.py` erneut aus.

### Neue Daten hinzufügen:
Nutze den Admin-Bereich der App:
```
https://deine-app.vercel.app/admin
```

## 8. Nächste Schritte

- [ ] Custom Domain einrichten (optional)
- [ ] Supabase Storage für Bilder konfigurieren
- [ ] Analytics einrichten
- [ ] Monitoring/Logging konfigurieren

## Hilfreiche Links

- [Supabase Docs](https://supabase.com/docs)
- [Vercel Docs](https://vercel.com/docs)
- [SQLAlchemy mit PostgreSQL](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html)
