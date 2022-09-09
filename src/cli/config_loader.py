import typer
from context import DEFAULT_CONFIG_FILENAME
import os


def set_config(config_filename: str, remove_logger: bool = True) -> None:
    from context import config_file
    if remove_logger:
        from loguru import logger
        logger.remove()  # Logger supression to beauty CLI output
    os.environ['X_FA_CONFIG_FILENAME'] = config_filename
    config_file.set(config_filename)


config_default: str = typer.Option(
    default=DEFAULT_CONFIG_FILENAME,
    help='Path to CONFIG file'
)
