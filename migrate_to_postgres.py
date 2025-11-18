"""
Skript zur Migration/Initialisierung der PostgreSQL-Datenbank für Vercel
Führe dieses Skript aus, nachdem du die DATABASE_URL Umgebungsvariable gesetzt hast
"""
import sys
import os

# Füge app-Verzeichnis zum Python-Pfad hinzu
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.app import create_app
from app.models import db
from app.models.destination import Destination
from app.models.activity import Activity


def migrate_database():
    """Erstelle Tabellen und füge Testdaten hinzu"""
    app = create_app()

    with app.app_context():
        print("Erstelle Tabellen...")
        db.create_all()

        # Prüfe ob bereits Daten vorhanden sind
        if Destination.query.count() > 0:
            print("Datenbank enthält bereits Daten. Überspringe Testdaten.")
            return

        print("Füge Testdaten hinzu...")

        # Testdestination 1: Spanien
        spain = Destination(
            name="Spanien - Barcelona & Costa Brava",
            description_short="Entdecke die lebendige Kultur Barcelonas und entspanne an den schönen Stränden der Costa Brava.",
            image_cover="spain/cover.jpg"
        )
        db.session.add(spain)
        db.session.flush()

        spain_activities = [
            Activity(
                destination_id=spain.id,
                title="Flug nach Barcelona",
                description="Direktflug nach Barcelona. Beinhaltet nur den Transport ohne weitere Services.",
                slider_level_min=0,
                slider_level_max=5,
                image_filename="spain/barcelona.jpg"
            ),
            Activity(
                destination_id=spain.id,
                title="Mietauto & flexibles Erkunden",
                description="Mietauto für maximale Flexibilität. Du entscheidest, wohin die Reise geht.",
                slider_level_min=1,
                slider_level_max=3,
                image_filename="spain/park_guell.jpg"
            ),
            Activity(
                destination_id=spain.id,
                title="Barcelona City Tour (geführt)",
                description="Geführte Tour durch Barcelona: Sagrada Familia, Park Güell und Gotisches Viertel.",
                slider_level_min=4,
                slider_level_max=5,
                image_filename="spain/beach.jpg"
            ),
            Activity(
                destination_id=spain.id,
                title="Strandtag an der Costa Brava",
                description="Entspanne an einem der wunderschönen Strände und schwimme im kristallklaren Wasser.",
                slider_level_min=2,
                slider_level_max=5,
                image_filename="spain/girona.jpg"
            ),
            Activity(
                destination_id=spain.id,
                title="Flamenco-Show und Abendessen",
                description="Genieße eine authentische Flamenco-Vorstellung mit traditionellem spanischen Abendessen.",
                slider_level_min=5,
                slider_level_max=5,
                image_filename="spain/flamenco.jpg"
            )
        ]

        for activity in spain_activities:
            db.session.add(activity)

        # Testdestination 2: Island
        iceland = Destination(
            name="Island - Feuer und Eis",
            description_short="Erlebe die atemberaubende Natur Islands mit Vulkanen, Wasserfällen und Nordlichtern.",
            image_cover="iceland/cover.jpg"
        )
        db.session.add(iceland)
        db.session.flush()

        iceland_activities = [
            Activity(
                destination_id=iceland.id,
                title="Flug nach Reykjavik",
                description="Flug nach Island. Nur Transport, keine weiteren Services inklusive.",
                slider_level_min=0,
                slider_level_max=5,
                image_filename="iceland/reykjavik.jpg"
            ),
            Activity(
                destination_id=iceland.id,
                title="Mietwagen & Roadtrip",
                description="Mietwagen für einen selbstgeplanten Roadtrip durch Island.",
                slider_level_min=1,
                slider_level_max=2,
                image_filename="iceland/golden_circle.jpg"
            ),
            Activity(
                destination_id=iceland.id,
                title="Golden Circle Tagestour (geführt)",
                description="Geführte Tour: Þingvellir-Nationalpark, Gullfoss-Wasserfall und Geysir-Gebiet.",
                slider_level_min=3,
                slider_level_max=5,
                image_filename="iceland/blue_lagoon.jpg"
            ),
            Activity(
                destination_id=iceland.id,
                title="Gletscherwanderung",
                description="Unternimm eine geführte Wanderung auf einem echten Gletscher.",
                slider_level_min=4,
                slider_level_max=5,
                image_filename="iceland/glacier.jpg"
            ),
            Activity(
                destination_id=iceland.id,
                title="Nordlichter-Jagd",
                description="Erlebe das magische Schauspiel der Aurora Borealis am Nachthimmel.",
                slider_level_min=5,
                slider_level_max=5,
                image_filename="iceland/northern_lights.jpg"
            )
        ]

        for activity in iceland_activities:
            db.session.add(activity)

        # Testdestination 3: Japan
        japan = Destination(
            name="Japan - Tokyo & Kyoto",
            description_short="Tauche ein in die faszinierende Mischung aus Tradition und Moderne in Japans Metropolen.",
            image_cover="japan/cover.jpg"
        )
        db.session.add(japan)
        db.session.flush()

        japan_activities = [
            Activity(
                destination_id=japan.id,
                title="Flug nach Tokyo",
                description="Flug nach Tokyo. Nur Transport ohne weitere Leistungen.",
                slider_level_min=0,
                slider_level_max=5,
                image_filename="japan/tokyo.jpg"
            ),
            Activity(
                destination_id=japan.id,
                title="JR Pass & individuelle Erkundung",
                description="Japan Rail Pass für flexible Zugfahrten. Plane deine eigene Route.",
                slider_level_min=1,
                slider_level_max=3,
                image_filename="japan/kyoto_temples.jpg"
            ),
            Activity(
                destination_id=japan.id,
                title="Geführte Tour: Tokyo & Kyoto",
                description="Geführte Tour durch Tokyo (Shibuya, Asakusa) und Kyoto (Goldener Pavillon, Fushimi Inari).",
                slider_level_min=4,
                slider_level_max=5,
                image_filename="japan/tea_ceremony.jpg"
            ),
            Activity(
                destination_id=japan.id,
                title="Mount Fuji Ausflug",
                description="Besuche den ikonischen Mount Fuji und die umliegenden fünf Seen.",
                slider_level_min=3,
                slider_level_max=5,
                image_filename="japan/mount_fuji.jpg"
            ),
            Activity(
                destination_id=japan.id,
                title="Onsen & Kaiseki-Dinner",
                description="Traditionelles Thermalbad und mehrgängiges Kaiseki-Abendessen in Hakone.",
                slider_level_min=5,
                slider_level_max=5,
                image_filename="japan/onsen.jpg"
            )
        ]

        for activity in japan_activities:
            db.session.add(activity)

        db.session.commit()

        print("\n✓ Datenbank erfolgreich initialisiert!")
        print(f"✓ {Destination.query.count()} Destinationen erstellt")
        print(f"✓ {Activity.query.count()} Aktivitäten erstellt")


if __name__ == '__main__':
    migrate_database()
