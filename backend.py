from flask import Flask, render_template, jsonify, request
import numpy as np
from sklearn.ensemble import IsolationForest

app = Flask(__name__)

# ML Model (Anomaly Detection)
model = IsolationForest(contamination=0.1)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        features = np.array([[
            float(data["HeartRate"]),
            float(data["SpO2"]),
            float(data["Temperature"]),
            float(data["Respiration"]),
            float(data["BP_Systolic"]),
            float(data["BP_Diastolic"]),
            float(data["Glucose"]),
            float(data["ActivityLevel"])
        ]])

        anomaly = model.fit_predict(features)[0]

        risk = "High Risk ⚠️" if anomaly == -1 else "Normal ✅"

        return jsonify({"Risk": risk})

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)