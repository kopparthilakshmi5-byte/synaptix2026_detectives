import numpy as np
import joblib
from sklearn.ensemble import IsolationForest

MODEL_FILE = "model.pkl"

# Generate synthetic normal health data
# Columns: heart_rate, spo2, temperature
# Normal ranges: heart_rate ~ 75, spo2 ~ 97, temperature ~ 36.8
normal_data = np.random.normal(
    loc=[75, 97, 36.8],      # mean values
    scale=[10, 1, 0.3],      # standard deviations
    size=(500, 3)            # 500 samples, 3 features
)

# Create IsolationForest model
model = IsolationForest(
    contamination=0.05,  # 5% of data treated as anomalies
    random_state=42
)

# Train model
model.fit(normal_data)

# Save model to disk
joblib.dump(model, MODEL_FILE)

print(f"Model trained and saved as {MODEL_FILE}")