from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from typing import Any

import requests

API_KEY: str = os.getenv("WEATHER_API_KEY", "")
BASE_URL = "https://api.openweathermap.org/data/2.5"


def obter_dados(lat: float, lon: float, api_key: str) -> dict[str, Any]:
    url = f"{BASE_URL}/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def transformar_dados(raw: dict[str, Any]) -> dict[str, Any]:
    main = raw.get("main", {})
    sys_info = raw.get("sys", {})
    weather_list = raw.get("weather", [{}])
    weather = weather_list[0] if weather_list else {}

    return {
        "cidade": str(raw.get("name")),
        "pais": str(sys_info.get("country")),
        "temperatura": float(main.get("temp", 0.0)),
        "umidade": int(main.get("humidity", 0)),
        "descricao": str(weather.get("description", "")),
        "timestamp": datetime.utcnow().isoformat(),
    }


def salvar_dados(data: dict[str, Any], caminho: str) -> None:
    with open(caminho, "a", encoding="utf-8") as file:
        file.write(json.dumps(data, ensure_ascii=False) + "\n")


def run_pipeline(lat: float, lon: float, saida: str) -> None:
    raw = obter_dados(lat, lon, API_KEY)
    transformed = transformar_dados(raw)
    salvar_dados(transformed, saida)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python weather_pipeline.py <lat> <lon> <arquivo_saida>")
        sys.exit(1)

    lat = float(sys.argv[1])
    lon = float(sys.argv[2])
    arquivo = sys.argv[3]

    run_pipeline(lat, lon, arquivo)