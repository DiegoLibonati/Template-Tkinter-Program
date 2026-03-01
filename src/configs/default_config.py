import os

from src.configs.logger_config import setup_logger

logger = setup_logger("tkinter-app - default_config.py")


class DefaultConfig:
    # General
    TZ = os.getenv("TZ", "America/Argentina/Buenos_Aires")
    DEBUG = False
    TESTING = False

    # App
    ENV_NAME = os.getenv("ENV_NAME", "template tkinter python")
