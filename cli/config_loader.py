import typer

def set_config(config_filename)->None:
    from context import config_file
    config_file.set(config_filename)

config_default: str = typer.Option(
    default='config.toml',
    help='Path to CONFIG file'
    )