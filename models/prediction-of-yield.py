# %%
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np
import joblib
import os

# Load dataset
df = pd.read_csv("data/crop_yield.csv")
df = df.dropna()

# %%
# Create a dictionary of encoders for multiple categorical columns
encoders = {}
for col in ["Crop", "Season", "State"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le   # store separately

# %%
X = df[["Crop","Crop_Year","Season","State","Area","Production","Annual_Rainfall","Fertilizer","Pesticide"]]
y = df["Yield"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# %%
# Train Random Forest
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# %%
# Evaluate
rf_preds = model.predict(X_test)
rf_r2 = r2_score(y_test, rf_preds)
rf_rmse = np.sqrt(mean_squared_error(y_test, rf_preds))

print("🌲 Random Forest Results:")
print(f"R² Score: {rf_r2:.4f}")
print(f"RMSE: {rf_rmse:.2f}")

# %%
# Save model + all encoders
os.makedirs("trained_model", exist_ok=True)
joblib.dump(model, "trained_model/crop_yield_model.pkl")
joblib.dump(encoders, "trained_model/label_encoders.pkl")
