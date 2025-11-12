from app.models import db


class Activity(db.Model):
    """Aktivitäts-Modell für Reiseziele"""
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    slider_level_min = db.Column(db.Integer, nullable=False, default=0)
    slider_level_max = db.Column(db.Integer, nullable=False, default=5)
    image_filename = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Activity {self.title} (Level {self.slider_level_min}-{self.slider_level_max})>'
