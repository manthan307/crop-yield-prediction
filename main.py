import fastapi
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import time
import pandas as pd
from geopy.geocoders import Nominatim
import requests
from tips import generate_tips

app = fastapi.FastAPI()
api_key = "27387d7111fa0bc3a1dc14fc8aa8a592"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CropYieldRequest(BaseModel):
    crop: str
    location: str
    season: str
    production: str
    farmArea: str
    fertilizer: str
    pesticide: str
    soilType: str
    year: str
    moisture: str
    nitrogen: str
    phosphorous: str
    potassium: str

geolocator = Nominatim(user_agent="geoapi")

def get_cordinates(district):
    loc = geolocator.geocode(f"{district}, India")
    return (loc.latitude, loc.longitude)

def fetch_weather_data(lat, lon):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={lat}&lon={lon}&appid={api_key}&units=metric"
    )
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["main"]
    else:
        print("Error:", response.status_code, response.text)
        return None

# ------------------ Load models ------------------ #
rain_model = joblib.load("trained_model/rain_model.pkl")
rain_le = joblib.load("trained_model/state_label_encoder.pkl")
yield_model = joblib.load("trained_model/crop_yield_model.pkl")
yield_encoders = joblib.load("trained_model/label_encoders.pkl")

fert_model = joblib.load("trained_model/fertilizer_model.pkl")
fert_feature_encoders = joblib.load("trained_model/feature_label_encoders.pkl")
fert_label_encoder = joblib.load("trained_model/fertilizer_label_encoder.pkl")

# ------------------ API Route ------------------ #
@app.post("/predict")
async def read_root(request: CropYieldRequest):

    state = request.location.split(",")[1].strip().upper()
    year = time.localtime().tm_year

    # ---------------- Yield Prediction ---------------- #
    try:
        state_enc = rain_le.transform([state])[0]
    except:
        return {"error": f"State '{state}' not found"}
    
    pred_rainfall = rain_model.predict([[state_enc, year]])[0]

    yield_data = {
        "Crop": request.crop.capitalize(),
        "Crop_Year": year,
        "Season": request.season.capitalize(),
        "State": state.capitalize(),
        "Area": float(request.farmArea),
        "Production": float(request.production),
        "Annual_Rainfall": pred_rainfall,
        "Fertilizer": float(request.fertilizer),
        "Pesticide": float(request.pesticide)
    }

    for col in ["Crop", "Season", "State"]:
        le = yield_encoders[col]
        if yield_data[col] in le.classes_:
            yield_data[col] = le.transform([yield_data[col]])[0]
        else:
            yield_data[col] = -1  

    X_yield = pd.DataFrame([yield_data])
    prediction = yield_model.predict(X_yield)[0]

    # ---------------- Weather ---------------- #
    latitude, longitude = get_cordinates(request.location.split(",")[0].strip())
    weather_data = fetch_weather_data(latitude, longitude)
    temp, humidity = weather_data["temp"], weather_data["humidity"]

    # ---------------- Fertilizer Prediction ---------------- #
    # ---------------- Fertilizer Prediction ---------------- #
    fert_data = {
    "Temparature": temp,
    "Humidity": humidity,
    "Moisture": float(request.moisture),
    "SoilType": request.soilType.capitalize(),
    "CropType": request.crop.capitalize(),
    "Nitrogen": float(request.nitrogen),
    "Potassium": float(request.potassium),
    "Phosphorous": float(request.phosphorous)
    }

# encode categorical features
    for col in ["CropType", "SoilType"]:
        le = fert_feature_encoders[col]
        if fert_data[col] in le.classes_:
            fert_data[col] = le.transform([fert_data[col]])[0]
        else:
                fert_data[col] = -1  

    # Ensure correct column order as used in training
    cols_order = ["Temparature", "Moisture", "CropType", "SoilType",
              "Nitrogen", "Phosphorous", "Potassium", "Humidity"]

    X_fert = pd.DataFrame([fert_data], columns=cols_order)

    # Predict fertilizer
    fert_pred = fert_model.predict(X_fert)[0]
    fert_name = fert_label_encoder.inverse_transform([int(fert_pred)])[0]

    #----------------Generate tips ---------------------#
    tips = generate_tips(
    crop=request.crop,
    season=request.season,
    fertilizer=fert_name,
    temp=temp,
    humidity=humidity,
    rainfall=pred_rainfall
    )


    # ---------------- Response ---------------- #
    return {
        "yield": f"{prediction:.2f}",
        "rainfall": f"{pred_rainfall} mm",
        "fertilizer": fert_name,
        "weather": {"temp": temp, "humidity": humidity},
        "tips": tips
    }
