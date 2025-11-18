"""
Vereinfachte Flask App ohne Datenbank
Nutzt JSON-Dateien für Datenspeicherung
"""
from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__,
            template_folder='app/templates',
            static_folder='app/static')

# Konfiguration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SLIDER_MIN'] = 0
app.config['SLIDER_MAX'] = 5

# Pfade zu JSON-Dateien
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DESTINATIONS_FILE = os.path.join(BASE_DIR, 'data', 'destinations.json')
ACTIVITIES_FILE = os.path.join(BASE_DIR, 'data', 'activities.json')


def load_destinations():
    """Lade Destinationen aus JSON"""
    with open(DESTINATIONS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_activities():
    """Lade Aktivitäten aus JSON"""
    with open(ACTIVITIES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_destination_by_id(dest_id):
    """Hole eine Destination anhand der ID"""
    destinations = load_destinations()
    for dest in destinations:
        if dest['id'] == dest_id:
            return dest
    return None


def get_activities_by_destination(dest_id, slider_value=None):
    """Hole Aktivitäten für eine Destination, optional gefiltert nach Slider-Level"""
    activities = load_activities()
    filtered = [a for a in activities if a['destination_id'] == dest_id]

    if slider_value is not None:
        filtered = [
            a for a in filtered
            if a['slider_level_min'] <= slider_value <= a['slider_level_max']
        ]

    # Sortiere nach min level
    filtered.sort(key=lambda x: x['slider_level_min'])
    return filtered


@app.route('/')
def index():
    """Startseite mit allen Destinationen"""
    destinations = load_destinations()
    return render_template('index.html', destinations=destinations)


@app.route('/destination/<int:id>')
def show_destination(id):
    """Detailansicht einer Destination mit Slider"""
    slider_value = request.args.get('slider', 0, type=int)
    destination = get_destination_by_id(id)

    if not destination:
        return "Destination nicht gefunden", 404

    activities = get_activities_by_destination(id, slider_value)

    return render_template(
        'destination.html',
        destination=destination,
        activities=activities,
        slider_value=slider_value,
        slider_max=app.config['SLIDER_MAX']
    )


@app.route('/api/destination/<int:id>/activities')
def api_get_activities(id):
    """API-Endpunkt: Hole Aktivitäten basierend auf Slider-Level"""
    slider_value = request.args.get('slider', 0, type=int)
    destination = get_destination_by_id(id)

    if not destination:
        return jsonify({'error': 'Destination not found'}), 404

    activities = get_activities_by_destination(id, slider_value)

    return jsonify({
        'activities': activities,
        'count': len(activities)
    })


@app.route('/admin')
def admin():
    """Admin-Übersicht (Read-Only)"""
    destinations = load_destinations()
    all_activities = load_activities()

    return render_template(
        'admin_simple.html',
        destinations=destinations,
        total_activities=len(all_activities)
    )


@app.route('/admin/destination/<int:destination_id>/activities')
def admin_activities(destination_id):
    """Aktivitäten einer Destination anzeigen (Read-Only)"""
    destination = get_destination_by_id(destination_id)

    if not destination:
        return "Destination nicht gefunden", 404

    activities = get_activities_by_destination(destination_id)

    return render_template(
        'admin_activities_simple.html',
        destination=destination,
        activities=activities
    )


if __name__ == '__main__':
    print("\n" + "="*60)
    print("  Reise-Auswahl-App gestartet! (Simplified Version)")
    print("  URL: http://localhost:5001")
    print("  Daten werden aus JSON-Dateien geladen")
    print("="*60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5001)
