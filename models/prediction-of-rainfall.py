import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import joblib
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np

# Load data
df = pd.read_csv("data/rainfall in india 1901-2015.csv")

df = df.dropna(subset=["ANNUAL"])
# Encode categorical subdivision
le = LabelEncoder()
df["SUBDIVISION"] = le.fit_transform(df["SUBDIVISION"])

# Features and target
X = df[["SUBDIVISION", "YEAR"]]
y = df["ANNUAL"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

rf_preds = model.predict(X_test)
rf_r2 = r2_score(y_test, rf_preds)
rf_rmse = np.sqrt(mean_squared_error(y_test, rf_preds))

print("🌲 Random Forest Results:")
print(f"R² Score: {rf_r2:.4f}")
print(f"RMSE: {rf_rmse:.2f}")

# Save encoder + model
joblib.dump(model, "trained_model/rain_model.pkl")
joblib.dump(le, "trained_model/state_label_encoder.pkl")
