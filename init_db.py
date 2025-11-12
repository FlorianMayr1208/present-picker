"""
Skript zur Initialisierung der Datenbank mit Testdaten
"""
import sys
import os

# Füge app-Verzeichnis zum Python-Pfad hinzu
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.app import create_app
from app.models import db
from app.models.destination import Destination
from app.models.activity import Activity


def init_database():
    """Initialisiere Datenbank mit Testdaten"""
    app = create_app()

    with app.app_context():
        # Lösche alle existierenden Daten
        print("Lösche existierende Daten...")
        db.drop_all()

        # Erstelle Tabellen neu
        print("Erstelle Tabellen...")
        db.create_all()

        # Testdestination 1: Spanien
        spain = Destination(
            name="Spanien - Barcelona & Costa Brava",
            description_short="Entdecke die lebendige Kultur Barcelonas und entspanne an den schönen Stränden der Costa Brava.",
            image_cover="spain/cover.jpg"  # Platzhalter
        )
        db.session.add(spain)
        db.session.flush()  # Um die ID zu erhalten

        # Aktivitäten für Spanien
        spain_activities = [
            Activity(
                destination_id=spain.id,
                title="Barcelona erkunden",
                description="Besuche die Sagrada Familia, spaziere durch das Gotische Viertel und genieße Tapas.",
                slider_level=1,
                image_filename="spain/barcelona.jpg"
            ),
            Activity(
                destination_id=spain.id,
                title="Park Güell & Gaudí-Architektur",
                description="Bewundere die einzigartige Architektur von Antoni Gaudí im Park Güell.",
                slider_level=2,
                image_filename="spain/park_guell.jpg"
            ),
            Activity(
                destination_id=spain.id,
                title="Strandtag an der Costa Brava",
                description="Entspanne an einem der wunderschönen Strände und schwimme im kristallklaren Wasser.",
                slider_level=3,
                image_filename="spain/beach.jpg"
            ),
            Activity(
                destination_id=spain.id,
                title="Tagesausflug nach Girona",
                description="Erkunde die mittelalterliche Stadt Girona mit ihrer beeindruckenden Kathedrale.",
                slider_level=4,
                image_filename="spain/girona.jpg"
            ),
            Activity(
                destination_id=spain.id,
                title="Flamenco-Show und Abendessen",
                description="Genieße eine authentische Flamenco-Vorstellung mit traditionellem spanischen Abendessen.",
                slider_level=5,
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

        # Aktivitäten für Island
        iceland_activities = [
            Activity(
                destination_id=iceland.id,
                title="Reykjavik Stadtbesichtigung",
                description="Erkunde die nördlichste Hauptstadt der Welt mit ihren bunten Häusern und Cafés.",
                slider_level=1,
                image_filename="iceland/reykjavik.jpg"
            ),
            Activity(
                destination_id=iceland.id,
                title="Golden Circle Tour",
                description="Besuche den Þingvellir-Nationalpark, den Gullfoss-Wasserfall und das Geysir-Gebiet.",
                slider_level=2,
                image_filename="iceland/golden_circle.jpg"
            ),
            Activity(
                destination_id=iceland.id,
                title="Blaue Lagune",
                description="Entspanne in den geothermalen Gewässern der weltberühmten Blauen Lagune.",
                slider_level=3,
                image_filename="iceland/blue_lagoon.jpg"
            ),
            Activity(
                destination_id=iceland.id,
                title="Gletscherwanderung",
                description="Unternimm eine geführte Wanderung auf einem echten Gletscher.",
                slider_level=4,
                image_filename="iceland/glacier.jpg"
            ),
            Activity(
                destination_id=iceland.id,
                title="Nordlichter-Jagd",
                description="Erlebe das magische Schauspiel der Aurora Borealis am Nachthimmel.",
                slider_level=5,
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

        # Aktivitäten für Japan
        japan_activities = [
            Activity(
                destination_id=japan.id,
                title="Tokyo Highlights",
                description="Besuche Shibuya, Shinjuku und den Senso-ji Tempel in Asakusa.",
                slider_level=1,
                image_filename="japan/tokyo.jpg"
            ),
            Activity(
                destination_id=japan.id,
                title="Tempel und Schreine in Kyoto",
                description="Erkunde den Goldenen Pavillon und den Fushimi Inari Schrein.",
                slider_level=2,
                image_filename="japan/kyoto_temples.jpg"
            ),
            Activity(
                destination_id=japan.id,
                title="Traditionelle Tee-Zeremonie",
                description="Nimm an einer authentischen japanischen Tee-Zeremonie teil.",
                slider_level=3,
                image_filename="japan/tea_ceremony.jpg"
            ),
            Activity(
                destination_id=japan.id,
                title="Mount Fuji Ausflug",
                description="Besuche den ikonischen Mount Fuji und die umliegenden fünf Seen.",
                slider_level=4,
                image_filename="japan/mount_fuji.jpg"
            ),
            Activity(
                destination_id=japan.id,
                title="Onsen-Erlebnis",
                description="Entspanne in einem traditionellen japanischen Thermalbad (Onsen) in Hakone.",
                slider_level=5,
                image_filename="japan/onsen.jpg"
            )
        ]

        for activity in japan_activities:
            db.session.add(activity)

        # Speichere alle Änderungen
        db.session.commit()

        print("\n✓ Datenbank erfolgreich initialisiert!")
        print(f"✓ {Destination.query.count()} Destinationen erstellt")
        print(f"✓ {Activity.query.count()} Aktivitäten erstellt")
        print("\nDu kannst die App jetzt mit 'python app/app.py' starten.")


if __name__ == '__main__':
    init_database()
