""" Configs """
from pydantic import BaseSettings
from .logging import logger
import json

class Settings(BaseSettings):
    """ Default Basic Setting Configs

    The priority goes:
        environment variable > .env file > defaults in class Settings

    """
    class Config:
        """It will load file in env_file
        """
        env_file = "env/compliance.env"

    # The defaults settings starts here
    LEVERAGE: int = 5
    RUN_AFTER_SECOND: int = 60
    DATA_PATH: str = "backtest-data"
    DATA_TYPE: str = "ETHBUSD"
    DATA_INTERVAL: str = "4h"
    STRATEGY: str = "MartinV1"
    DBFILE_PATH: str = "db"
    MODE: str = "test"
    APIKEY_PATH: str = "api_key_test.json"
configs = Settings()
logger.info("\n****************** The Followings Are The Configs ******************\n")
for k, v in configs.__dict__.items():
    logger.info("%s: %s", k, json.dumps(v))
logger.info("\n******************** The Aboves Are The Configs ********************\n")
