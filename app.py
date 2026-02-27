from flask import Flask, jsonify, render_template
import random
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

LOG_FILE = "health_log.csv"

# Create CSV if not exists
if not os.path.exists(LOG_FILE):
    df = pd.DataFrame(columns=["time", "heart_rate", "spo2", "temperature", "risk"])
    df.to_csv(LOG_FILE, index=False)


# 🧠 AI-Based Risk Detection
def detect_risk(hr, spo2, temp):
    risk = "Normal"

    if hr < 50 or hr > 120:
        risk = "High Heart Risk"
    elif spo2 < 92:
        risk = "Low Oxygen Risk"
    elif temp > 38:
        risk = "Fever Risk"

    return risk


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/health")
def health_data():
    # Simulated wearable data
    heart_rate = random.randint(55, 130)
    spo2 = random.randint(88, 100)
    temperature = round(random.uniform(36.0, 39.5), 1)

    risk = detect_risk(heart_rate, spo2, temperature)

    # Log Data
    new_data = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "heart_rate": heart_rate,
        "spo2": spo2,
        "temperature": temperature,
        "risk": risk
    }

    df = pd.read_csv(LOG_FILE)
    df = pd.concat([df, pd.DataFrame([new_data])])
    df.to_csv(LOG_FILE, index=False)

    return jsonify(new_data)


if __name__ == "__main__":
    app.run(debug=True)