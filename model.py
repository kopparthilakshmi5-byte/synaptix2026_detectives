import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

MODEL_PATH = "models/isolation_model.pkl"

def train_model():
    # Online dataset (no manual download)
    url = "https://raw.githubusercontent.com/ashishpatel26/IoT-Dataset/master/healthcare-dataset-stroke-data.csv"
    
    df = pd.read_csv(url)

    # Create simulated wearable-style features
    df["heart_rate"] = np.random.normal(75, 10, len(df))
    df["spo2"] = np.random.normal(97, 2, len(df))
    df["temperature"] = np.random.normal(36.8, 0.5, len(df))
    df["respiration"] = np.random.normal(16, 3, len(df))

    X = df[["heart_rate", "spo2", "temperature", "respiration"]].values

    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(X)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    return model

def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    else:
        return train_model()

def predict_risk(model, values):
    arr = np.array(values).reshape(1, -1)
    score = model.decision_function(arr)[0]
    return round(max(min(1 - ((score + 0.5)), 1), 0), 2)