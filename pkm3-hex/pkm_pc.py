from pathlib import Path

import typer

app = typer.Typer()


@app.command()
def dump(save_file: Path, box: int, slot: int):
    pass


@app.command()
def show(box: int, slot: int):
    pass
