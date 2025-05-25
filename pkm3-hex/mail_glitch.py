import json
from enum import StrEnum
from typing import IO, Optional

import typer
from rich.columns import Columns
from rich.console import Console
from rich.table import Table

from . import std_stream_default_arg
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
    pkm_bytes_file: typer.FileBinaryRead = std_stream_default_arg,
    output_file: typer.FileTextWrite = std_stream_default_arg,
    output_format: OutputFormat = OutputFormat.PRETTY,
    limit: Optional[int] = None,
) -> None:
    mail_words = sorted(
        find_mail_words(pkm_bytes_file.read(), order), key=MailWords.scroll_distance
    )[:limit]

    if output_format == OutputFormat.JSON:
        json.dump(mail_words, output_file, cls=PkmJSONSerializer)
    else:
        if not mail_words:
            print("No mail glitch words found", file=output_file)
            raise typer.Exit(63)

        print_words(mail_words, output_file)


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
