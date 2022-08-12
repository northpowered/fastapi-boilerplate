from .model import Configuration
from os import environ
config = Configuration()
config.load(environ['X_FA_CONF_FILE'])