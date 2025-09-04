# tips.py

def generate_tips(crop: str, season: str, fertilizer: str, temp: float, humidity: float, rainfall: float):
    """
    Generate actionable tips for a farmer based on crop, season, fertilizer, and weather.
    
    Args:
        crop (str): Crop name
        season (str): Season (e.g., Rabi, Kharif)
        fertilizer (str): Recommended fertilizer
        temp (float): Current temperature in Celsius
        humidity (float): Current humidity percentage
        rainfall (float): Predicted annual rainfall in mm
    
    Returns:
        List[str]: List of tips
    """
    tips = []

    # -------- Weather-based tips --------
    if temp > 35:
        tips.append("High temperature detected. Consider mulching to reduce soil moisture loss.")
    elif temp < 15:
        tips.append("Low temperature detected. Protect seedlings from cold stress.")

    if humidity < 40:
        tips.append("Low humidity. Foliar spray may help prevent moisture stress.")
    elif humidity > 80:
        tips.append("High humidity. Ensure proper aeration to reduce fungal risk.")

    if rainfall < 50:
        tips.append("Low rainfall expected. Plan supplementary irrigation.")
    elif rainfall > 200:
        tips.append("High rainfall expected. Ensure proper drainage to avoid waterlogging.")

    # -------- Fertilizer-based tips --------
    if fertilizer.lower() == "14-35-14":
        tips.append("Apply 1/3 dose before sowing and the remaining in two splits during growth.")
    elif fertilizer.lower() == "urea":
        tips.append("Apply in small splits to avoid nitrogen loss and optimize absorption.")
    else:
        tips.append(f"Follow recommended guidelines for {fertilizer} application.")

    # -------- Crop-specific tips --------
    crop_lower = crop.lower()
    season_lower = season.lower()
    
    if crop_lower == "wheat" and season_lower == "rabi":
        tips.append("Maintain ~20 cm row spacing for optimal growth.")
        tips.append("Check for pest infestation early and apply protective measures.")
    elif crop_lower == "rice" and season_lower == "kharif":
        tips.append("Ensure flooded fields for better growth during initial stages.")
        tips.append("Split nitrogen application to improve yield.")
    else:
        tips.append(f"Follow standard cultivation practices for {crop} in {season} season.")

    return tips
