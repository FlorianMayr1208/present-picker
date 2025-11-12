from app.models import db


class Destination(db.Model):
    """Reiseziel-Modell"""
    __tablename__ = 'destinations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description_short = db.Column(db.Text, nullable=True)
    image_cover = db.Column(db.String(200), nullable=True)

    # Beziehung zu Aktivitäten
    activities = db.relationship('Activity', backref='destination', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Destination {self.name}>'
