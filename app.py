# app.py
from flask import Flask, render_template, jsonify
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os

app = Flask(__name__)

# -------------------
# Create / Load Model
# -------------------
MODEL_PATH = "models/isolation_model.pkl"
if not os.path.exists("models"):
    os.makedirs("models")

# Generate synthetic normal data for multi-signal training
normal_data = np.random.normal(loc=[75,97,36.8,16], scale=[5,1,0.3,2], size=(1000,4))

if not os.path.exists(MODEL_PATH):
    model = IsolationForest(contamination=0.01, random_state=42)
    model.fit(normal_data)
    joblib.dump(model, MODEL_PATH)
else:
    model = joblib.load(MODEL_PATH)

# -------------------
# Simulate Real-time Sensor Data
# -------------------
def get_sensor_data():
    hr = np.random.normal(75, 5)
    spo2 = np.random.normal(97, 1)
    temp = np.random.normal(36.8, 0.3)
    rr = np.random.normal(16, 2)
    return [round(hr,1), round(spo2,1), round(temp,1), round(rr,1)]

# -------------------
# Flask Routes
# -------------------
@app.route("/")
def dashboard():
    return render_template("index.html")

@app.route("/api/data")
def api_data():
    data = np.array(get_sensor_data()).reshape(1, -1)
    score = model.decision_function(data)[0]
    risk = round(max(min(1 - ((score + 0.5)),1),0),2)
    return jsonify({
        "heart_rate": data[0][0],
        "spo2": data[0][1],
        "temperature": data[0][2],
        "respiratory_rate": data[0][3],
        "risk_score": risk
    })

if __name__ == "__main__":
    app.run(debug=True)