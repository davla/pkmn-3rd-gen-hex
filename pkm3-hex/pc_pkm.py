import typer

from . import std_stream_default_arg
from .utils import GameSaveBlock, pretty_print

app = typer.Typer()


@app.command()
def dump(
    box: int,
    row: int,
    col: int,
    decrypt: bool = True,
    save_file: typer.FileBinaryRead = std_stream_default_arg,
    output_file: typer.FileBinaryWrite = std_stream_default_arg,
):
    save_block = GameSaveBlock.from_bytes(save_file.read())
    box_data = save_block.pc.boxes[box - 1]
    row_index, col_index = row - 1, col - 1
    pkm_bytes = (
        box_data[row_index, col_index].data
        if decrypt
        else box_data.raw_pkm_bytes(row_index, col_index)
    )
    output_file.write(pkm_bytes)


@app.command()
def show(
    box: int,
    row: int,
    col: int,
    save_file: typer.FileBinaryRead = std_stream_default_arg,
    output_file: typer.FileTextWrite = std_stream_default_arg,
):
    save_block = GameSaveBlock.from_bytes(save_file.read())
    pkm = save_block.pc.boxes[box - 1][row - 1, col - 1]
    pretty_print.pkm(pkm, output_file)
