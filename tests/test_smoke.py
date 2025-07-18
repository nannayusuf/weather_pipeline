from src.weather_pipeline.config import get_settings


def test_settings_loads():
    settings = get_settings()
    assert settings.weather_api_key
