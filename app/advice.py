def generate_advice(current, forecast_list=None):
    advice = []
    if not current:
        return [{"icon": "alert-circle", "text": "Unable to fetch weather data, check API Key"}]

    temp = current.get("temp", 0)
    humidity = current.get("humidity", 0)
    wind_speed = current.get("wind_speed", 0)
    main_weather = current.get("main", "").lower()
    description = current.get("description", "")

    rain_keywords = ["rain", "drizzle", "thunderstorm", "shower"]
    if any(k in main_weather for k in rain_keywords):
        advice.append({"icon": "umbrella", "text": "Rain expected, bring an umbrella!"})
    if forecast_list:
        rain_coming = any(
            any(k in f.get("main", "").lower() for k in rain_keywords)
            for f in forecast_list[:4]
        )
        if rain_coming and not any(k in main_weather for k in rain_keywords):
            advice.append({"icon": "umbrella-outline", "text": "Rain expected later, consider bringing an umbrella"})

    if temp >= 35:
        advice.append({"icon": "white-balance-sunny", "text": "Extreme heat! Stay hydrated and use sunscreen"})
    elif temp >= 30:
        advice.append({"icon": "white-balance-sunny", "text": "Hot weather, stay hydrated"})

    if temp < 5:
        advice.append({"icon": "snowflake", "text": "Very cold! Dress warmly, watch for ice"})
    elif temp < 10:
        advice.append({"icon": "weather-windy", "text": "Cold weather, bring a jacket"})

    if wind_speed > 10:
        advice.append({"icon": "weather-windy", "text": "Strong wind! Watch for falling objects"})
    elif wind_speed > 7:
        advice.append({"icon": "weather-windy", "text": "Windy, hold onto your hat"})

    if humidity > 85:
        advice.append({"icon": "water-percent", "text": "Very humid, may feel uncomfortable"})

    if main_weather in ["mist", "fog", "haze", "smoke"]:
        advice.append({"icon": "mask", "text": "Poor visibility, wear a mask if sensitive"})

    if not advice:
        advice.append({"icon": "check-circle", "text": "Weather looks good today, enjoy your day!"})

    return advice


def generate_notification_text(current):
    if not current:
        return "Weather data unavailable"

    temp = current.get("temp", 0)
    desc = current.get("description", "")
    city = current.get("city", "")

    parts = [f"{city} {temp:.0f}C {desc}"]

    advice_list = generate_advice(current)
    for a in advice_list[:2]:
        parts.append(a["text"])

    return " | ".join(parts)
