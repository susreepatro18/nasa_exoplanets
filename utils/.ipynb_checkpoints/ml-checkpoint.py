import joblib

model = joblib.load("habitability_xgb_model.pkl")

def predict_habitability(data):
    features = [[
        data["mass"],
        data["radius"],
        data["temperature"]
    ]]
    score = model.predict_proba(features)[0][1]
    return float(score)
