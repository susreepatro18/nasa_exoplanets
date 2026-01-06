from flask import Flask, request, jsonify
from database.db import db
from database.models import Exoplanet
from utils.ml import predict_habitability
from utils.validators import ExoplanetSchema

app = Flask(__name__)

# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///exoplanets.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
schema = ExoplanetSchema()

# -------- CREATE DB TABLES (FLASK 3 FIX) --------
with app.app_context():
    db.create_all()

# -------- API: Add Exoplanet --------
@app.route("/api/exoplanet", methods=["POST"])
def add_exoplanet():
    data = request.get_json()
    errors = schema.validate(data)

    if errors:
        return jsonify({"status": "error", "errors": errors}), 400

    score = predict_habitability(data)

    planet = Exoplanet(
        name=data["name"],
        mass=data["mass"],
        radius=data["radius"],
        temperature=data["temperature"],
        habitability_score=score
    )

    db.session.add(planet)
    db.session.commit()

    return jsonify({
        "status": "success",
        "habitability_score": score
    }), 201

# -------- API: Ranking --------
@app.route("/api/ranking", methods=["GET"])
def ranking():
    planets = Exoplanet.query.order_by(
        Exoplanet.habitability_score.desc()
    ).all()

    return jsonify([
        {
            "rank": i + 1,
            "name": p.name,
            "score": p.habitability_score
        }
        for i, p in enumerate(planets)
    ])

if __name__ == "__main__":
    app.run(debug=True)
