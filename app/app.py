from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app.config import Config
from app.models import db
from app.models.destination import Destination
from app.models.activity import Activity
import os


def create_app(config_class=Config):
    """Application Factory Pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialisiere Extensions
    db.init_app(app)

    # Erstelle Datenbank-Tabellen
    with app.app_context():
        db.create_all()

    # Registriere Routen
    register_routes(app)

    return app


def register_routes(app):
    """Registriere alle Routes"""

    @app.route('/')
    def index():
        """Startseite mit allen Destinationen"""
        destinations = Destination.query.all()
        return render_template('index.html', destinations=destinations)

    @app.route('/destination/<int:id>')
    def show_destination(id):
        """Detailansicht einer Destination mit Slider"""
        slider_value = request.args.get('slider', 0, type=int)
        destination = Destination.query.get_or_404(id)

        # Filtere Aktivitäten basierend auf Slider-Level
        activities = Activity.query.filter(
            Activity.destination_id == id,
            Activity.slider_level <= slider_value
        ).order_by(Activity.slider_level).all()

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
        from flask import jsonify

        slider_value = request.args.get('slider', 0, type=int)
        destination = Destination.query.get_or_404(id)

        # Filtere Aktivitäten basierend auf Slider-Level
        activities = Activity.query.filter(
            Activity.destination_id == id,
            Activity.slider_level <= slider_value
        ).order_by(Activity.slider_level).all()

        # Konvertiere zu JSON
        activities_data = [{
            'id': activity.id,
            'title': activity.title,
            'description': activity.description,
            'slider_level': activity.slider_level,
            'image_filename': activity.image_filename
        } for activity in activities]

        return jsonify({
            'activities': activities_data,
            'count': len(activities_data)
        })

    @app.route('/admin')
    def admin():
        """Admin-Übersicht"""
        destinations = Destination.query.all()
        return render_template('admin.html', destinations=destinations)

    # ========== DESTINATION ADMIN ROUTES ==========

    @app.route('/admin/destination/new', methods=['GET', 'POST'])
    def admin_destination_new():
        """Neue Destination erstellen"""
        if request.method == 'POST':
            name = request.form.get('name')
            description_short = request.form.get('description_short')
            image_file = request.files.get('image_cover')

            # Validierung
            if not name:
                flash('Name ist erforderlich!', 'danger')
                return render_template('admin_destination_form.html', destination=None)

            # Bild-Upload verarbeiten
            image_filename = None
            if image_file and image_file.filename:
                image_filename = save_uploaded_file(image_file, 'general')

            # Destination erstellen
            destination = Destination(
                name=name,
                description_short=description_short,
                image_cover=image_filename
            )
            db.session.add(destination)
            db.session.commit()

            flash(f'Destination "{name}" wurde erfolgreich erstellt!', 'success')
            return redirect(url_for('admin'))

        return render_template('admin_destination_form.html', destination=None)

    @app.route('/admin/destination/<int:id>/edit', methods=['GET', 'POST'])
    def admin_destination_edit(id):
        """Destination bearbeiten"""
        destination = Destination.query.get_or_404(id)

        if request.method == 'POST':
            destination.name = request.form.get('name')
            destination.description_short = request.form.get('description_short')
            image_file = request.files.get('image_cover')

            # Validierung
            if not destination.name:
                flash('Name ist erforderlich!', 'danger')
                return render_template('admin_destination_form.html', destination=destination)

            # Neues Bild hochladen (optional)
            if image_file and image_file.filename:
                destination.image_cover = save_uploaded_file(image_file, 'general')

            db.session.commit()
            flash(f'Destination "{destination.name}" wurde aktualisiert!', 'success')
            return redirect(url_for('admin'))

        return render_template('admin_destination_form.html', destination=destination)

    @app.route('/admin/destination/<int:id>/delete', methods=['POST'])
    def admin_destination_delete(id):
        """Destination löschen"""
        destination = Destination.query.get_or_404(id)
        name = destination.name
        db.session.delete(destination)
        db.session.commit()
        flash(f'Destination "{name}" wurde gelöscht!', 'warning')
        return redirect(url_for('admin'))

    # ========== ACTIVITY ADMIN ROUTES ==========

    @app.route('/admin/destination/<int:destination_id>/activities')
    def admin_activities(destination_id):
        """Aktivitäten einer Destination verwalten"""
        destination = Destination.query.get_or_404(destination_id)
        activities = Activity.query.filter_by(destination_id=destination_id).order_by(Activity.slider_level).all()
        return render_template('admin_activities.html', destination=destination, activities=activities)

    @app.route('/admin/destination/<int:destination_id>/activity/new', methods=['GET', 'POST'])
    def admin_activity_new(destination_id):
        """Neue Aktivität erstellen"""
        destination = Destination.query.get_or_404(destination_id)

        if request.method == 'POST':
            title = request.form.get('title')
            description = request.form.get('description')
            slider_level = request.form.get('slider_level', type=int)
            image_file = request.files.get('image_filename')

            # Validierung
            if not title:
                flash('Titel ist erforderlich!', 'danger')
                return render_template('admin_activity_form.html',
                                     destination=destination,
                                     activity=None,
                                     slider_max=app.config['SLIDER_MAX'])

            if slider_level is None or slider_level < 0 or slider_level > app.config['SLIDER_MAX']:
                flash(f'Slider-Level muss zwischen 0 und {app.config["SLIDER_MAX"]} liegen!', 'danger')
                return render_template('admin_activity_form.html',
                                     destination=destination,
                                     activity=None,
                                     slider_max=app.config['SLIDER_MAX'])

            # Bild-Upload verarbeiten
            image_filename = None
            if image_file and image_file.filename:
                # Erstelle Ordner für diese Destination falls nicht vorhanden
                dest_folder = sanitize_folder_name(destination.name)
                image_filename = save_uploaded_file(image_file, dest_folder)

            # Aktivität erstellen
            activity = Activity(
                destination_id=destination_id,
                title=title,
                description=description,
                slider_level=slider_level,
                image_filename=image_filename
            )
            db.session.add(activity)
            db.session.commit()

            flash(f'Aktivität "{title}" wurde erstellt!', 'success')
            return redirect(url_for('admin_activities', destination_id=destination_id))

        return render_template('admin_activity_form.html',
                             destination=destination,
                             activity=None,
                             slider_max=app.config['SLIDER_MAX'])

    @app.route('/admin/activity/<int:id>/edit', methods=['GET', 'POST'])
    def admin_activity_edit(id):
        """Aktivität bearbeiten"""
        activity = Activity.query.get_or_404(id)
        destination = activity.destination

        if request.method == 'POST':
            activity.title = request.form.get('title')
            activity.description = request.form.get('description')
            slider_level = request.form.get('slider_level', type=int)
            image_file = request.files.get('image_filename')

            # Validierung
            if not activity.title:
                flash('Titel ist erforderlich!', 'danger')
                return render_template('admin_activity_form.html',
                                     destination=destination,
                                     activity=activity,
                                     slider_max=app.config['SLIDER_MAX'])

            if slider_level is None or slider_level < 0 or slider_level > app.config['SLIDER_MAX']:
                flash(f'Slider-Level muss zwischen 0 und {app.config["SLIDER_MAX"]} liegen!', 'danger')
                return render_template('admin_activity_form.html',
                                     destination=destination,
                                     activity=activity,
                                     slider_max=app.config['SLIDER_MAX'])

            activity.slider_level = slider_level

            # Neues Bild hochladen (optional)
            if image_file and image_file.filename:
                dest_folder = sanitize_folder_name(destination.name)
                activity.image_filename = save_uploaded_file(image_file, dest_folder)

            db.session.commit()
            flash(f'Aktivität "{activity.title}" wurde aktualisiert!', 'success')
            return redirect(url_for('admin_activities', destination_id=destination.id))

        return render_template('admin_activity_form.html',
                             destination=destination,
                             activity=activity,
                             slider_max=app.config['SLIDER_MAX'])

    @app.route('/admin/activity/<int:id>/delete', methods=['POST'])
    def admin_activity_delete(id):
        """Aktivität löschen"""
        activity = Activity.query.get_or_404(id)
        destination_id = activity.destination_id
        title = activity.title
        db.session.delete(activity)
        db.session.commit()
        flash(f'Aktivität "{title}" wurde gelöscht!', 'warning')
        return redirect(url_for('admin_activities', destination_id=destination_id))


# ========== HELPER FUNCTIONS ==========

def allowed_file(filename):
    """Prüfe ob Dateiendung erlaubt ist"""
    from app.config import Config
    if '.' not in filename:
        return False
    return filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def sanitize_folder_name(name):
    """Erstelle sicheren Ordnernamen aus Destination-Name"""
    import re
    # Ersetze Umlaute
    replacements = {'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss',
                   'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue'}
    for old, new in replacements.items():
        name = name.replace(old, new)
    # Entferne alle Zeichen außer Buchstaben, Zahlen, Bindestriche und Unterstriche
    name = re.sub(r'[^\w\s-]', '', name)
    # Ersetze Leerzeichen durch Unterstriche
    name = re.sub(r'[-\s]+', '_', name)
    return name.lower()


def save_uploaded_file(file, subfolder='general'):
    """Speichere hochgeladene Datei"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # Erstelle Zielordner falls nicht vorhanden
        upload_path = os.path.join(Config.UPLOAD_FOLDER, subfolder)
        os.makedirs(upload_path, exist_ok=True)

        # Speichere Datei
        file_path = os.path.join(upload_path, filename)
        file.save(file_path)

        # Gib relativen Pfad zurück (für Datenbank)
        return os.path.join(subfolder, filename)

    return None


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
