from .model import Configuration
from context import config_file
config = Configuration()
config.load(config_file.get())