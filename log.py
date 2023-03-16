import yaml
import logging.config
import os

LOGG_FILE_NAME = "config/logging.yaml"

class PlatformLog:
    def __init__(self, default_path=LOGG_FILE_NAME, default_level=logging.INFO, env_key="LOG_CFG"):
        path = default_path
        value = os.getenv(env_key, None)
        if value:
            path = value
        if os.path.exists(path):
            with open(path, "r") as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
                logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=default_level)

    @staticmethod
    def setup_logging(default_path=LOGG_FILE_NAME, default_level=logging.INFO, env_key="LOG_CFG"):
        path = default_path
        value = os.getenv(env_key, None)
        if value:
            path = value
        if os.path.exists(path):
            with open(path, "r") as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
                logging.config.dictConfig(config)
        else:
            logging.basicConfig(filename='info.log',level=default_level,force=True)

    @staticmethod
    def info(msg,*arg1):
        logging.info(msg % arg1)

    @staticmethod
    def error(msg,*arg1):
        logging.error(msg % arg1)

    @staticmethod
    def debug(msg,*arg1):
        logging.debug(msg % arg1)

# if __name__ == "__main__":
#     PlatformLog.setup_logging(default_path=LOGG_FILE_NAME)
#     PlatformLog.func("hello")
# PlatformLog().func("hello")

PlatformLog.setup_logging(default_path=LOGG_FILE_NAME)