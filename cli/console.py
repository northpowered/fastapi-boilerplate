from rich import print as _print
cli_prefix = "[magenta bold]CLI:>[/magenta bold]"
def print(string: str):
    _print(f"{cli_prefix} {string}")