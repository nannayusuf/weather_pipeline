import os
from unittest.mock import patch

from weather_pipeline.main import main


@patch.dict(os.environ, {"WEATHER_API_KEY": "fake_key"})
def test_main_runs_without_error() -> None:
    main()
