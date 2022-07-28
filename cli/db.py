import typer

app = typer.Typer(no_args_is_help=True)


@app.command()
def init():
    print(f"init!")


@app.command()
def drop():
    print(f"drop!")


if __name__ == "__main__":
    app()