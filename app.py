from flask import Flask, render_template, jsonify, request
import numpy as np
import os
import joblib

app = Flask(__name__)

MODEL_PATH = "models/isolation_model.pkl"

def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None

def predict_risk(model, values):
    arr = np.array(values).reshape(1, -1)
    score = model.decision_function(arr)[0]
    return round(max(min(1 - ((score + 0.5)), 1), 0), 2)

def generate_alert(data, risk):
    hr, spo2, temp, rr = data
    alert = "Normal"
    message = "Vitals are stable."
    level = "low"

    if risk > 0.7:
        alert = "Critical"
        message = "High health risk!"
        level = "high"
    elif risk > 0.4:
        alert = "Warning"
        message = "Moderate risk."
        level = "medium"

    if spo2 < 92:
        alert = "Critical"
        message = "Low SpO2!"
        level = "high"

    return alert, message, level

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/data")
def api_data():
    # Auto generate changing data
    hr = np.random.normal(75, 8)
    spo2 = np.random.normal(97, 2)
    temp = np.random.normal(36.8, 0.5)
    rr = np.random.normal(16, 3)

    values = [hr, spo2, temp, rr]

    model = load_model()
    risk = predict_risk(model, values) if model else 0.0

    alert, message, level = generate_alert(values, risk)

    return jsonify({
        "heart_rate": round(hr,1),
        "spo2": round(spo2,1),
        "temperature": round(temp,1),
        "respiratory_rate": round(rr,1),
        "risk_score": risk,
        "alert": alert,
        "alert_message": message,
        "alert_level": level
    })

if __name__ == "__main__":
    app.run(debug=True)