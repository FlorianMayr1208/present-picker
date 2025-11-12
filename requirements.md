# Reise-Auswahl-App -- Anforderungen & Entwicklungsplan

## 1. Überblick

Diese App dient dazu, verschiedene Reiseziele und mögliche
Reiseplanungen einer Nutzerin (der Freundin des Erstellers) zu
präsentieren. Die Nutzerin soll über einen interaktiven Slider selbst
bestimmen können, wie detailliert die Anzeige der jeweiligen
Reiseplanung ist (von „nur Ziel anzeigen" bis „voll durchgeplant").

Der Ersteller soll im Backend in der Lage sein, Reiseziele,
Beschreibungen, Bilder sowie Aktivitäten und deren Sichtbarkeitsstufe
(zugeordnete Slider-Stufe) zu konfigurieren.

Die App wird als leichtgewichtige Flask-Webanwendung umgesetzt.

------------------------------------------------------------------------

## 2. Funktionale Anforderungen

### 2.1 Benutzerfunktionen (Frontend)

-   **Zielauswahl**
    -   Anzeige einer Übersicht aller verfügbaren Destinationen.
    -   Jede Destination wird als Karte oder Bildkachel dargestellt
        (Bild + Titel).
    -   Klicken auf eine Karte öffnet die Detailansicht der Destination.
-   **Detailansicht einer Destination**
    -   Anzeige eines Titelbildes und einer kurzen Beschreibung.
    -   Anzeige eines interaktiven Sliders (z. B. 0--100 oder 1--5
        Stufen).
    -   Inhalte werden abhängig vom Slider-Wert dynamisch eingeblendet.
    -   Anzeige von Aktivitäten/Abschnitten, deren `slider_level` \<=
        aktuellem Slider-Wert ist.
    -   Bilder und Texte der Aktivitäten anzeigen (Titel, Beschreibung,
        optional Galerie).
-   **Interaktion**
    -   Slider-Bewegung aktualisiert Inhalte ohne komplette
        Seitenneuladung (AJAX optional).
    -   Optional: Favorisieren/Markieren eines Reiseziels.
    -   Optional: Button zum Bestätigen der finalen Reisauswahl.

------------------------------------------------------------------------

## 2.2 Erstellerfunktionen (Backend/Adminbereich)

-   **Verwaltung von Destinationen**
    -   Anlegen, Bearbeiten und Löschen von Destinationen.
    -   Felder: Name, Kurzbeschreibung, Titelbild.
-   **Verwaltung von Aktivitäten**
    -   Aktivitäten für jede Destination anlegen, bearbeiten und
        löschen.
    -   Felder:
        -   Titel
        -   Beschreibung
        -   Bilddatei
        -   `slider_level` (Integer, definiert ab welcher Slider-Stufe
            sichtbar)
-   **Medienverwaltung**
    -   Upload von Bildern für Destinationen und Aktivitäten.
    -   Automatisches Ablegen in strukturierter Ordnerhierarchie.
-   **Konfigurierbarkeit**
    -   Slider-Stufen frei definierbar (z. B. 0--5).
    -   Pro Stufe können beliebig viele Aktivitäten zugeordnet werden.

------------------------------------------------------------------------

## 3. Nichtfunktionale Anforderungen

-   **Benutzerfreundlichkeit**
    -   Intuitive Bedienung, Fokus auf visuelle Darstellung.
    -   Smooth Animations/Fade-ins bei der Aktivitätseinblendung.
-   **Performance**
    -   Schnelle Ladezeiten durch lokale Medien.
    -   Keine hohen Serveranforderungen.
-   **Skalierbarkeit**
    -   Mögliches späteres Hinzufügen neuer Ziele/Abschnitte ohne
        Codeänderung.
-   **Design**
    -   Responsives Layout für Laptop/Tablet.
    -   Verwendung einer klaren visuellen Struktur (z. B. Bootstrap).
-   **Datenhaltung**
    -   Persistenz in einer SQLite-Datenbank.
    -   Bilder als Dateien in `/static/images/<destination>/`.

------------------------------------------------------------------------

## 4. Technologieauswahl

### 4.1 Backend

-   **Flask**
    -   Leichtgewichtig, flexibel, ideal für Single-User-Projekte.
    -   Template-System: Jinja2.
-   **ORM**
    -   SQLAlchemy für saubere Datenmodellierung.
-   **Datenbank**
    -   SQLite (einfach verwaltbar, ideal für lokale Anwendung).

### 4.2 Frontend

-   **HTML/CSS/JavaScript**
-   **Bootstrap** oder TailwindCSS für schnelleres Styling.
-   **noUiSlider** oder Standard-HTML-Range-Slider für saubere
    Slider-Interaktion.
-   Optional: AJAX (fetch API) für dynamische Aktualisierung ohne
    Reload.

### 4.3 Dateistruktur

Empfohlene Projektstruktur:

    /app
        /static
            /css
            /images
                /spain/
                /iceland/
            /js
        /templates
            base.html
            index.html
            destination.html
            admin.html
        /models
            destination.py
            activity.py
        app.py
        config.py
        database.db

------------------------------------------------------------------------

## 5. Datenmodell

### 5.1 Destination

  ---------------------------------------------------------------------------
  Feld                Typ        Beschreibung
  ------------------- ---------- --------------------------------------------
  id                  Integer    Primärschlüssel

  name                String     Name der Destination

  description_short   Text       Kurzbeschreibung

  image_cover         String     Dateiname des Titelbildes
  ---------------------------------------------------------------------------

------------------------------------------------------------------------

### 5.2 Activity

  ------------------------------------------------------------------------
  Feld             Typ        Beschreibung
  ---------------- ---------- --------------------------------------------
  id               Integer    Primärschlüssel

  destination_id   Integer    Fremdschlüssel auf Destination

  title            String     Titel der Aktivität

  description      Text       Beschreibung

  slider_level     Integer    Stufe des Sliders, ab der sichtbar

  image_filename   String     Bilddateiname
  ------------------------------------------------------------------------

------------------------------------------------------------------------

## 6. Interaktionslogik

### 6.1 Slider-Funktion

Bei Änderung des Slider-Wertes:

``` python
activities = Activity.query.filter(
    Activity.destination_id == id,
    Activity.slider_level <= slider_value
).all()
```

Anschließend werden die Aktivitäten im Template angezeigt oder via AJAX
nachgeladen.

------------------------------------------------------------------------

## 7. Entwicklungsplan

### Phase 1 -- Setup & Grundgerüst

-   Virtuelle Umgebung erstellen.
-   Flask initialisieren.
-   Startseite mit Liste der Destinationen implementieren.
-   Template-Basisstruktur erstellen.

### Phase 2 -- Datenbank & Modelle

-   Datenbanktabellen mit SQLAlchemy erstellen.
-   Initiale Migration oder manuelle DB-Erzeugung.
-   Testdaten einpflegen.

### Phase 3 -- Detailansicht & Slider

-   Slider in die Destinationseite integrieren.
-   Logik zum Filtern der Aktivitäten basierend auf Slider-Level.
-   Anzeigeformat der Aktivitäten implementieren.

### Phase 4 -- Admin-Oberfläche

-   Formulare zum Anlegen und Bearbeiten von Destinationen/Activities.
-   Upload-Mechanismus für Bilder.
-   Validierung der Eingaben.

### Phase 5 -- UI/UX-Verbesserungen

-   Animationen beim Einblenden.
-   Mobile-Optimierung.
-   Bildergalerie/Lightbox optional.

### Phase 6 -- Deployment (optional)

-   Lokal oder online auf Render/PythonAnywhere deployen.

------------------------------------------------------------------------

## 8. Beispiel-Flask-Route (vereinfachte Darstellung)

``` python
@app.route('/destination/<int:id>')
def show_destination(id):
    slider = request.args.get('slider', 0, type=int)
    dest = Destination.query.get_or_404(id)
    activities = Activity.query.filter(
        Activity.destination_id == id,
        Activity.slider_level <= slider
    ).all()

    return render_template(
        'destination.html',
        dest=dest,
        activities=activities,
        slider=slider
    )
```

------------------------------------------------------------------------

## 9. Optional: Erweiterungen

-   Favoritenfunktion
-   PDF-Export der vollständigen Reiseplanung
-   Mehrsprachigkeit
-   Kartendarstellung via Leaflet.js
-   Passwortgeschützter Admin-Bereich

------------------------------------------------------------------------
