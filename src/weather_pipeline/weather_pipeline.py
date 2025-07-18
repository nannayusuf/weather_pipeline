import requests
import os
from datetime import datetime
import json
from typing import Dict, Any

API_KEY = os.getenv("WEATHER_API_KEY", "")
BASE_URL = "https://api.openweathermap.org/data/2.5"


def fetch_weather_data(lat: float, lon: float, api_key: str) -> Dict[str, Any]:
    url = f"{BASE_URL}/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def transform_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    main_data = raw_data.get("main", {})
    weather_info = raw_data.get("weather", [{}])[0]
    return {
       "city": raw_data.get("name"),
       "country": raw_data.get("sys", {}).get("country"),
       "temperature": main_data.get("temp"),
       "humidity": main_data.get("humidity"),
       "description": weather_info.get("description"),
       "timestamp": datetime.utcnow().isoformat(),
   }


def save_data(data: Dict[str, Any], file_path: str) -> None:
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(json.dumps(data, ensure_ascii=False) + "\n")


def run_pipeline(lat: float, lon: float, output_file: str) -> None:
    raw_data = fetch_weather_data(lat, lon, API_KEY)
    transformed_data = transform_data(raw_data)
    save_data(transformed_data, output)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python weather_pipeline.py <lat> <lon> <output_file>")
        sys.exit(1)

    lat = float(sys.argv[1])
    lon = float(sys.argv[2])
    output_file = sys.argv[3]

    run_pipeline(lat, lon, output_file)