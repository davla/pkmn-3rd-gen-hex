import json
import sys
from enum import StrEnum
from pathlib import Path
from typing import IO, Annotated, Optional

import typer
from rich.columns import Columns
from rich.console import Console
from rich.table import Table

from . import FILE_STD_STREAM_ARG
from .data import easy_chat
from .utils import (
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
    pkm_bytes_file: Annotated[Path, typer.Argument()] = FILE_STD_STREAM_ARG,
    output_file: Annotated[Path, typer.Argument()] = FILE_STD_STREAM_ARG,
    output_format: OutputFormat = OutputFormat.PRETTY,
    limit: Optional[int] = None,
) -> None:
    if pkm_bytes_file == FILE_STD_STREAM_ARG:
        pkm_bytes = sys.stdin.buffer.read()
    else:
        with open(pkm_bytes_file, "rb") as pkm_input:
            pkm_bytes = pkm_input.read()

    mail_words = find_mail_words(pkm_bytes, order)
    displayed_mail_words = sorted(mail_words, key=MailWords.scroll_distance)[:limit]

    if output_file == FILE_STD_STREAM_ARG:
        success = print_words(displayed_mail_words, sys.stdout, output_format)
    else:
        with open(output_file, "w") as output:
            success = print_words(displayed_mail_words, output, output_format)

    if not success:
        raise typer.Exit(63)


def print_words(
    mail_words: list[MailWords], output: IO[str], format: OutputFormat
) -> bool:
    if format == OutputFormat.JSON:
        json.dump(mail_words, output, cls=PkmJSONSerializer)
        return True

    if not mail_words:
        print("No mail glitch words found", file=output)
        return False

    mail_word_tables = map(make_mail_words_table, mail_words)
    console = Console(file=output)
    console.print(Columns(mail_word_tables))
    return True


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
