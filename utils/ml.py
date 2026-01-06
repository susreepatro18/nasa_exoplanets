import os
import joblib
import pandas as pd

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "habitability_xgb_model.joblib"
)

model = joblib.load(MODEL_PATH)

def predict_habitability(data):
    input_df = pd.DataFrame([{
        "pl_rade": data["radius"],
        "pl_density": data["density"],
        "pl_eqt": data["temperature"],
        "pl_orbsmax": data["orbit"],
        "pl_insol": data["insolation"],
        "pl_bmasse": data["planet_mass"],
        "st_mass": data["star_mass"],
        "st_rad": data["star_radius"],
        "st_luminosity": data["star_luminosity"],
        "st_spectype": data["star_type"]
    }])

    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]

    return int(prediction), round(float(probability), 3)
