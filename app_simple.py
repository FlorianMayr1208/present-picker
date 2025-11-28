"""
Vereinfachte Flask App ohne Datenbank
Nutzt JSON-Dateien für Datenspeicherung
"""
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from functools import wraps

# Load environment variables
load_dotenv()

app = Flask(__name__,
            template_folder='app/templates',
            static_folder='app/static')

# Konfiguration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['ADMIN_PASSWORD'] = os.environ.get('ADMIN_PASSWORD', 'admin123')
app.config['SLIDER_MIN'] = 0
app.config['SLIDER_MAX'] = 5

# Admin authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

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
        # Filter categories by slider level
        filtered = [
            a for a in filtered
            if 'slider_level_min' in a and 'slider_level_max' in a
            and a['slider_level_min'] <= slider_value <= a['slider_level_max']
        ]

        # Also filter sub-items by their slider level
        for activity in filtered:
            if 'sub_items' in activity and activity['sub_items']:
                activity['sub_items'] = [
                    sub for sub in activity['sub_items']
                    if 'slider_level_min' in sub and 'slider_level_max' in sub
                    and sub['slider_level_min'] <= slider_value <= sub['slider_level_max']
                ]

    # Filter out sub-items with from_parents=true or from_friends=true (they should only appear in special gift sections)
    for activity in filtered:
        if 'sub_items' in activity and activity['sub_items']:
            activity['sub_items'] = [
                sub for sub in activity['sub_items']
                if not sub.get('from_parents', False) and not sub.get('from_friends', False)
            ]

    # Remove activities with no sub-items (empty categories)
    filtered = [a for a in filtered if a.get('sub_items')]

    # Sortiere nach min level (nur für Slider-Aktivitäten)
    # Für Checkbox-Aktivitäten behalte die ID-Reihenfolge
    if filtered and 'slider_level_min' in filtered[0]:
        filtered.sort(key=lambda x: x['slider_level_min'])
    else:
        filtered.sort(key=lambda x: x['id'])

    return filtered


def get_parents_activities_by_destination(dest_id):
    """Hole alle Aktivitäten, die von den Eltern übernommen werden"""
    activities = load_activities()
    all_activities = [a for a in activities if a['destination_id'] == dest_id]

    parents_activities = []

    for activity in all_activities:
        if 'sub_items' in activity and activity['sub_items']:
            for sub_item in activity['sub_items']:
                if sub_item.get('from_parents', False):
                    parents_activities.append({
                        'activity_id': activity['id'],
                        'activity_title': activity['title'],
                        'sub_item': sub_item
                    })

    return parents_activities


def get_friends_activities_by_destination(dest_id):
    """Hole alle Aktivitäten, die von Freunden übernommen werden"""
    activities = load_activities()
    all_activities = [a for a in activities if a['destination_id'] == dest_id]

    friends_activities = []

    for activity in all_activities:
        if 'sub_items' in activity and activity['sub_items']:
            for sub_item in activity['sub_items']:
                if sub_item.get('from_friends', False):
                    friends_activities.append({
                        'activity_id': activity['id'],
                        'activity_title': activity['title'],
                        'sub_item': sub_item
                    })

    return friends_activities


@app.route('/')
def index():
    """Startseite mit allen Destinationen"""
    destinations = load_destinations()
    return render_template('index.html', destinations=destinations)


@app.route('/destination/<int:id>')
def show_destination(id):
    """Detailansicht einer Destination mit Slider oder Checkboxen"""
    destination = get_destination_by_id(id)

    if not destination:
        return "Destination nicht gefunden", 404

    selection_mode = destination.get('selection_mode', 'slider')

    if selection_mode == 'checkboxes':
        # Checkbox-Modus: Alle Aktivitäten laden
        activities = get_activities_by_destination(id, slider_value=None)
    else:
        # Slider-Modus: Aktivitäten nach Slider-Level filtern
        slider_value = request.args.get('slider', 0, type=int)
        activities = get_activities_by_destination(id, slider_value)

    # Hole Eltern-Aktivitäten und Freunde-Aktivitäten
    parents_activities = get_parents_activities_by_destination(id)
    friends_activities = get_friends_activities_by_destination(id)

    return render_template(
        'destination.html',
        destination=destination,
        activities=activities,
        slider_value=request.args.get('slider', 0, type=int),
        slider_max=app.config['SLIDER_MAX'],
        selection_mode=selection_mode,
        points_budget=destination.get('points_budget', 0),
        parents_activities=parents_activities,
        friends_activities=friends_activities
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


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin-Login"""
    if request.method == 'POST':
        password = request.form.get('password')
        if password == app.config['ADMIN_PASSWORD']:
            session['admin_logged_in'] = True
            flash('Erfolgreich eingeloggt!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Falsches Passwort!', 'danger')

    return render_template('admin_login.html')


@app.route('/admin/logout')
def admin_logout():
    """Admin-Logout"""
    session.pop('admin_logged_in', None)
    flash('Erfolgreich ausgeloggt.', 'info')
    return redirect(url_for('admin_login'))


@app.route('/admin')
@admin_required
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
@admin_required
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


@app.route('/destination/<int:id>/export-pdf', methods=['POST'])
def export_pdf(id):
    """PDF-Export der ausgewählten Aktivitäten (Browser-basiert)"""
    destination = get_destination_by_id(id)

    if not destination:
        return "Destination nicht gefunden", 404

    # Parse selected items from frontend
    selected_items_json = request.form.get('selected_items', '[]')
    selected_items = json.loads(selected_items_json)

    # Load all activities
    all_activities = load_activities()

    # Build selected activities structure
    selected_activities_data = []

    for item in selected_items:
        activity_id = int(item['activity_id'])
        sub_id = item['sub_id']
        from_parents = item.get('from_parents', False)

        # Find the activity
        activity = next((a for a in all_activities if a['id'] == activity_id and a['destination_id'] == id), None)

        if activity and 'sub_items' in activity:
            # Find the sub-item
            sub_item = next((s for s in activity['sub_items'] if s['id'] == sub_id), None)

            if sub_item:
                selected_activities_data.append({
                    'category': activity['title'],
                    'title': sub_item['title'],
                    'description': sub_item.get('description', ''),
                    'points': sub_item.get('points', 0),
                    'image_url': sub_item.get('image_filename', ''),
                    'from_parents': from_parents
                })

    # Calculate total points
    total_points = sum(item['points'] for item in selected_activities_data)

    # Render print-optimized HTML
    return render_template(
        'pdf_export.html',
        destination=destination,
        selected_activities=selected_activities_data,
        total_points=total_points,
        points_budget=destination.get('points_budget', 0),
        export_date=datetime.now().strftime('%d.%m.%Y')
    )


if __name__ == '__main__':
    print("\n" + "="*60)
    print("  Reise-Auswahl-App gestartet! (Simplified Version)")
    print("  URL: http://localhost:5001")
    print("  Daten werden aus JSON-Dateien geladen")
    print("="*60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5001)
