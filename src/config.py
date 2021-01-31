import json
from pathlib import Path
from src.constants import Files, ServerConfig, Environments
from src.logger import logger

DB_HOST = "DatabaseHost"
DB_USER = "DatabaseUser"
DB_PORT = "DatabasePort"
DB_NAME = "DatabaseName"

CONFIG = {}

logger.info(f"Current Dir: {Files.CURRENT_DIR}")


def _extend_config(filename):
    with open(filename, 'r') as child_config:
        CONFIG.update(json.loads(child_config.read()))


with open(Files.BASE_CONFIG, 'r') as base_config:
    CONFIG = json.loads(base_config.read())

if Path(Files.INTG_CONFIG).is_file() and ServerConfig.ENVIRONMENT == Environments.INTEGRATION:
    _extend_config(Files.INTG_CONFIG)

elif Path(Files.PROD_CONFIG).is_file() and ServerConfig.ENVIRONMENT == Environments.PROD:
    _extend_config(Files.PROD_CONFIG)

logger.info(CONFIG)
