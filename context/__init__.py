from contextvars import ContextVar

DEFAULT_CONFIG_FILENAME: str = 'config.toml'
config_file: ContextVar[str] = ContextVar('config_file', default=DEFAULT_CONFIG_FILENAME)