from contextvars import ContextVar
config_file: ContextVar[str] = ContextVar('config_file', default='config.toml')