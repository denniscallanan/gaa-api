import os
import pathlib


class EnvVars:
    PORT = "PORT"
    TOKEN = "TOKEN"
    ENVIRONMENT = "ENVIRONMENT"
    DATABASE_URL = "DATABASE_URL"


class Environments:
    DEV = "dev"
    INTEGRATION = "integration"
    PROD = "prod"


class ServerConfig:
    DATABASE_URL = os.environ.get(EnvVars.DATABASE_URL)
    PORT = int(os.environ.get(EnvVars.PORT, '5000'))
    ENVIRONMENT = os.environ.get(EnvVars.ENVIRONMENT, 'dev')


class Files:
    CONFIG_FOLDER = "config"
    CURRENT_DIR = pathlib.Path(__file__).parent.absolute()
    BASE_CONFIG = f"{CURRENT_DIR}/{CONFIG_FOLDER}/base_config.json"
    INTG_CONFIG = f"{CURRENT_DIR}/{CONFIG_FOLDER}/intg_config.json"
    PROD_CONFIG = f"{CURRENT_DIR}/{CONFIG_FOLDER}/prod_config.json"
    LOG_FILE = "/var/log/main.log" if ServerConfig.ENVIRONMENT == Environments.PROD else "main.log"


class ErrorValues:
    IDENTIFIER = "ApplicationError"
