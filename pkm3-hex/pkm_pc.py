import sys
from pathlib import Path
from typing import Annotated

import typer

from . import PAGE_FOOTER_ADDRESS, PAGE_FOOTER_SIZE, PAGE_SIZE, STDOUT_ARG
from .utils import PkmSubstructures

app = typer.Typer()

PC_START_ADDRESS = 0xE004
PC_PKM_LENGTH = 80
PC_BOX_LENGTH = PC_PKM_LENGTH * 30


@app.command()
def dump(
    save_file: Path,
    box: int,
    slot: int,
    decrypt: bool = True,
    output_file: Annotated[Path, typer.Argument()] = STDOUT_ARG,
) -> None:
    with open(save_file, "rb") as save:
        save_bytes = bytearray(save.read())

    pkm_offset = (box - 1) * PC_BOX_LENGTH + (slot - 1) * PC_PKM_LENGTH
    page_footers_in_offset = pkm_offset // PAGE_SIZE + (
        1 if pkm_offset % PAGE_SIZE > PAGE_FOOTER_ADDRESS else 0
    )

    start = PC_START_ADDRESS + pkm_offset + page_footers_in_offset * PAGE_FOOTER_SIZE
    pkm_bytes = save_bytes[start : start + PC_PKM_LENGTH]

    if decrypt:
        pkm_bytes[PkmSubstructures.start : PkmSubstructures.end] = (
            PkmSubstructures.from_bytes(pkm_bytes, decrypt=decrypt).as_bytes()
        )

    if output_file == STDOUT_ARG:
        sys.stdout.buffer.write(pkm_bytes)
    else:
        with open(output_file, "wb") as output:
            output.write(pkm_bytes)


@app.command()
def show(box: int, slot: int):
    pass
