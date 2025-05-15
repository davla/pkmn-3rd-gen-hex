import sys
from pathlib import Path
from typing import IO, Annotated, Optional

import typer
from rich.console import Console
from rich.table import Table

from . import FILE_STD_STREAM_ARG
from .data import easy_chat
from .utils import MailWords, PkmSubstructures, find_mail_words

app = typer.Typer()


@app.command()
def words(
    order: PkmSubstructures.Order,
    pkm_bytes_file: Annotated[Path, typer.Argument()] = FILE_STD_STREAM_ARG,
    output_file: Annotated[Path, typer.Argument()] = FILE_STD_STREAM_ARG,
) -> None:
    if pkm_bytes_file == FILE_STD_STREAM_ARG:
        pkm_bytes = sys.stdin.buffer.read()
    else:
        with open(pkm_bytes_file, "rb") as pkm_input:
            pkm_bytes = pkm_input.read()

    mail_words = list(find_mail_words(pkm_bytes, order))

    if output_file == FILE_STD_STREAM_ARG:
        success = print_words(sys.stdout, mail_words)
    else:
        with open(output_file, "w") as output:
            success = print_words(output, mail_words)

    if not success:
        raise typer.Exit(63)


def print_words(output: IO[str], mail_words: list[MailWords]) -> bool:
    if not mail_words:
        print("No mail glitch words found", file=output)
        return False

    console = Console(file=output)
    for words in sorted(mail_words, key=MailWords.scroll_distance):
        table = Table(show_header=False, show_lines=True)
        table.add_column()
        table.add_column()
        table.add_row(word_str(words.top_left), word_str(words.top_right))
        table.add_row(word_str(words.bottom_left), word_str(words.bottom_right))
        console.print(table)
    return True


def word_str(word: Optional[easy_chat.Word]) -> str:
    return (
        "???" if word is None else f"{word.text} ({word.category}, 0x{word.index:04X})"
    )
