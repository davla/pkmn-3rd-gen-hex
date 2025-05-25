import json
import os
from enum import StrEnum
from typing import IO, Optional

import typer
from rich.columns import Columns
from rich.console import Console
from rich.table import Table

from . import std_stream_default_opt
from .data import easy_chat
from .utils import (
    GameSaveBlock,
    MailWords,
    PkmJSONSerializer,
    PkmSubstructuresOrder,
    find_mail_words,
    format_hex,
)

app = typer.Typer()


class OutputFormat(StrEnum):
    JSON = "json"
    PRETTY = "pretty"


@app.command()
def words(
    order: PkmSubstructuresOrder,
    pkm_bytes_file: Optional[typer.FileBinaryRead] = None,
    save_file: Optional[typer.FileBinaryRead] = None,
    box_pos: Optional[tuple[int, int, int]] = None,
    output_file: typer.FileTextWrite = std_stream_default_opt,
    output_format: OutputFormat = OutputFormat.PRETTY,
    limit: Optional[int] = None,
):
    pkm_bytes = get_pkm_bytes(pkm_bytes_file, save_file, box_pos)
    mail_words = sorted(
        find_mail_words(pkm_bytes, order), key=MailWords.scroll_distance
    )[:limit]

    if output_format == OutputFormat.JSON:
        json.dump(mail_words, output_file, cls=PkmJSONSerializer)
    else:
        if not mail_words:
            print("No mail glitch words found", file=output_file)
            raise typer.Exit(63)

        print_words(mail_words, output_file)


def get_pkm_bytes(
    pkm_bytes_file: Optional[typer.FileBinaryRead],
    save_file: Optional[typer.FileBinaryRead],
    box_pos: Optional[tuple[int, int, int]],
) -> bytes:
    match (pkm_bytes_file, save_file):
        case (None, None):
            raise typer.BadParameter(
                f"no Pokémon bytes input given.{os.linesep}"
                "Use either the --pkm-bytes-file option or "
                "the --save-file and --box-pos options.",
                param_hint=["--pkm-bytes-file", "--save-file"],
            )

        case (pkm_bytes, None):
            return pkm_bytes.read()

        case (None, save):
            if box_pos is None:
                raise typer.BadParameter(
                    f"missing option --box-pos.{os.linesep}"
                    "Option --box-pos is mandatory with --save-file.",
                    param_hint=["--save-file", "--box-pos"],
                )
            box, row, col = box_pos
            save_block = GameSaveBlock.from_bytes(save.read())
            return save_block.pc.boxes[box - 1][row - 1, col - 1].data

        case (_, _):
            raise typer.BadParameter(
                f"too many Pokémon input bytes options.{os.linesep}"
                "Only one of the --pkm-bytes-file or --save-file options can be given.",
                param_hint=["--pkm-bytes-file", "--save-file"],
            )


def print_words(mail_words: list[MailWords], output: IO[str]):
    mail_word_tables = map(make_mail_words_table, mail_words)
    console = Console(file=output)
    console.print(Columns(mail_word_tables))


def make_mail_words_table(words: MailWords) -> Table:
    table = Table(show_header=False, show_lines=True)
    table.add_row(word_str(words.top_left), word_str(words.top_right))
    table.add_row(word_str(words.bottom_left), word_str(words.bottom_right))
    return table


def word_str(word: Optional[easy_chat.Word]) -> str:
    return (
        "???"
        if word is None
        else f"{word.text} ({word.category.value}, {format_hex(word.index, byte_size=2)})"
    )
