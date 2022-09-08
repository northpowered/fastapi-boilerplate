from contextvars import ContextVar
import os

DEFAULT_CONFIG_FILENAME: str = os.environ.get(
    'X_FA_CONFIG_FILENAME', 'src/config.toml')
config_file: ContextVar[str] = ContextVar(
    'config_file', default=DEFAULT_CONFIG_FILENAME)
