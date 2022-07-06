from .loader import Configuration
from os import environ
config = Configuration()
config.load(environ['X-FA-CONF-FILE'])