from flask import Flask, request, jsonify
from utils.ml import predict_habitability

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Habitability API running"})

@app.route("/api/exoplanet", methods=["POST"])
def exoplanet_predict():
    data = request.get_json()

    # REQUIRED FIELDS (must match training features)
    required_fields = [
        "radius",
        "density",
        "temperature",
        "orbit",
        "insolation",
        "planet_mass",
        "star_mass",
        "star_radius",
        "star_luminosity",
        "star_type"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    prediction, probability = predict_habitability(data)

    return jsonify({
        "habitability_class": prediction,
        "habitability_probability": probability
    }), 200

if __name__ == "__main__":
    app.run(debug=True)
