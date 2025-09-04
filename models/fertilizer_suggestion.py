# %%
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np
import joblib
import os

df = pd.read_csv("data/Fertilizer Prediction.csv")
df = df.dropna()
df.head()

# %%
encoders = {}
for col in ["CropType", "SoilType"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le   # store separately

# %%
X = df[["Temparature", "Moisture","CropType", "SoilType","Nitrogen", "Phosphorous", "Potassium","Humidity"]]
fertilizer_le = LabelEncoder()
y = fertilizer_le.fit_transform(df["Fertilizer Name"])

# %%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# %%
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# %%
rf_preds = model.predict(X_test)
rf_r2 = r2_score(y_test, rf_preds)
rf_rmse = np.sqrt(mean_squared_error(y_test, rf_preds))

print("🌲 Random Forest Results:")
print(f"R² Score: {rf_r2:.4f}")
print(f"RMSE: {rf_rmse:.2f}")

# %%
os.makedirs("trained_model", exist_ok=True)
joblib.dump(model, "trained_model/fertilizer_model.pkl")
joblib.dump(encoders, "trained_model/feature_label_encoders.pkl")
joblib.dump(fertilizer_le, "trained_model/fertilizer_label_encoder.pkl")

print("✅ Model and encoders saved successfully!")


