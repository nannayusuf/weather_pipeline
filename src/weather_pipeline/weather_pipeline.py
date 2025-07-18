import json
import os
import sys
from datetime import datetime, timezone
from typing import Any, cast

import requests

API_KEY = os.getenv("WEATHER_API_KEY", "")
BASE_URL = "https://api.openweathermap.org/data/2.5"


def fetch_weather_data(lat: float, lon: float, api_key: str) -> dict[str, Any]:
    url = f"{BASE_URL}/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = cast(dict[str, Any], response.json())
    return data


def transform_data(raw_data: dict[str, Any]) -> dict[str, Any]:
    main_data = raw_data.get("main", {})
    weather_info = raw_data.get("weather", [{}])[0]
    return {
       "city": raw_data.get("name"),
       "country": raw_data.get("sys", {}).get("country"),
       "temperature": main_data.get("temp"),
       "humidity": main_data.get("humidity"),
       "description": weather_info.get("description"),
       "timestamp": datetime.now(timezone.utc).isoformat(),
   }


def save_data(data: dict[str, Any], file_path: str) -> None:
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(json.dumps(data, ensure_ascii=False) + "\n")


def run_pipeline(lat: float, lon: float, output_file: str) -> None:
    raw_data = fetch_weather_data(lat, lon, API_KEY)
    transformed_data = transform_data(raw_data)
    save_data(transformed_data, output_file)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python weather_pipeline.py <lat> <lon> <output_file>")
        sys.exit(1)

    lat = float(sys.argv[1])
    lon = float(sys.argv[2])
    output_file = sys.argv[3]

    run_pipeline(lat, lon, output_file)
