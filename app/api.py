import requests

BASE_URL = "https://api.openweathermap.org/data/2.5"


class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_current_weather(self, city_name=None, lat=None, lon=None):
        params = {"appid": self.api_key, "units": "metric", "lang": "zh_cn"}
        if lat is not None and lon is not None:
            params["lat"] = lat
            params["lon"] = lon
        elif city_name:
            params["q"] = city_name
        else:
            return None

        try:
            resp = requests.get(f"{BASE_URL}/weather", params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException:
            return None

    def get_forecast(self, city_name=None, lat=None, lon=None):
        params = {"appid": self.api_key, "units": "metric", "lang": "zh_cn"}
        if lat is not None and lon is not None:
            params["lat"] = lat
            params["lon"] = lon
        elif city_name:
            params["q"] = city_name
        else:
            return None

        try:
            resp = requests.get(f"{BASE_URL}/forecast", params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException:
            return None

    @staticmethod
    def parse_current(data):
        if not data or "main" not in data:
            return None
        weather = data["weather"][0] if data.get("weather") else {}
        return {
            "city": data.get("name", ""),
            "temp": data["main"].get("temp", 0),
            "feels_like": data["main"].get("feels_like", 0),
            "humidity": data["main"].get("humidity", 0),
            "wind_speed": data.get("wind", {}).get("speed", 0),
            "description": weather.get("description", ""),
            "icon": weather.get("icon", "01d"),
            "main": weather.get("main", ""),
        }

    @staticmethod
    def parse_forecast(data):
        if not data or "list" not in data:
            return []
        results = []
        for item in data["list"][:20]:
            weather = item["weather"][0] if item.get("weather") else {}
            results.append({
                "dt_txt": item.get("dt_txt", ""),
                "temp": item["main"].get("temp", 0),
                "temp_min": item["main"].get("temp_min", 0),
                "temp_max": item["main"].get("temp_max", 0),
                "humidity": item["main"].get("humidity", 0),
                "wind_speed": item.get("wind", {}).get("speed", 0),
                "pop": item.get("pop", 0),
                "description": weather.get("description", ""),
                "icon": weather.get("icon", "01d"),
                "main": weather.get("main", ""),
            })
        return results
