"""
Production-ready entrypoint for the weather ETL pipeline.
"""

import os
import sys
from pathlib import Path

import structlog

from weather_pipeline.config import get_settings

SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

structlog.configure(
    processors=[
        structlog.dev.ConsoleRenderer(colors=os.isatty(sys.stdout.fileno())),
    ],
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


def main() -> None:
    """Pipeline entrypoint."""
    settings = get_settings()
    logger.info(
        "Weather pipeline started", api_key_length=len(settings.weather_api_key)
    )
    # TODO: integrar extração, transformação e carga
    logger.info("Weather pipeline finished")


if __name__ == "__main__":
    main()
