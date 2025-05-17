import sys
from pathlib import Path
from typing import Annotated

import typer

from . import FILE_STD_STREAM_ARG
from .utils import GameSaveBlock

app = typer.Typer()


@app.command()
def dump(
    save_file: Path,
    box: int,
    row: int,
    col: int,
    decrypt: bool = True,
    output_file: Annotated[Path, typer.Argument()] = FILE_STD_STREAM_ARG,
) -> None:
    with open(save_file, "rb") as save:
        save_bytes = bytearray(save.read())

    save_block = GameSaveBlock.from_bytes(save_bytes)
    box_data = save_block.pc.boxes[box - 1]

    row_index, col_index = row - 1, col - 1
    pkm_bytes = (
        box_data[row_index, col_index].data
        if decrypt
        else box_data.raw_pkm_bytes(row_index, col_index)
    )

    if output_file == FILE_STD_STREAM_ARG:
        sys.stdout.buffer.write(pkm_bytes)
    else:
        with open(output_file, "wb") as output:
            output.write(pkm_bytes)


@app.command()
def show(box: int, slot: int):
    pass
