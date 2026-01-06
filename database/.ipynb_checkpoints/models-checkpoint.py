from database.db import db

class Exoplanet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    mass = db.Column(db.Float)
    radius = db.Column(db.Float)
    temperature = db.Column(db.Float)
    habitability_score = db.Column(db.Float)
