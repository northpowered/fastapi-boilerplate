from rich import print as _print

cli_prefix = "[magenta bold]CLI:>[/magenta bold]"

def print(string: str):
    _print(f"{cli_prefix} {string}")

def info(string: str):
    print(f":blue_circle: [blue]{string}[/ blue]")

def success(string: str):
    print(f":green_circle: [green]{string}[/ green]")

def warning(string: str):
    print(f":yellow_circle: [yellow]{string}[/ yellow]")

def error(string: str):
    print(f":red_circle: [red bold]{string}[/ red bold]")