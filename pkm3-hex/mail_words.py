import json
import os
import textwrap
from enum import StrEnum
from pathlib import Path
from typing import IO, Optional, cast

import typer
from rich.columns import Columns
from rich.console import Console
from rich.table import Table

from . import std_stream_default_opt
from .data import easy_chat
from .utils import (
    GameSaveBlock,
    MailWords,
    PcPkm,
    PkmJSONSerializer,
    PkmSubstructuresOrder,
    format_hex,
    pretty_print,
)

app = typer.Typer()


class WordsOutputFormat(StrEnum):
    JSON = "json"
    PRETTY = "pretty"


class PkmOutputFormat(StrEnum):
    BINARY = "binary"
    PRETTY = "pretty"


@app.command()
def apply(
    pkm_bytes_file: Optional[typer.FileBinaryRead] = None,
    save_file: Optional[typer.FileBinaryRead] = None,
    box_pos: Optional[tuple[int, int, int]] = None,
    words_file: Optional[typer.FileText] = None,
    output_file: Path = Path("-"),
    output_format: Optional[PkmOutputFormat] = PkmOutputFormat.PRETTY,
) -> None:
    (pkm_bytes, is_encrypted) = get_pkm_bytes(pkm_bytes_file, save_file, box_pos)
    words = cast(MailWords, json.load(words_file, cls=PkmJSONSerializer))
    pkm = words.apply_to_pkm(pkm_bytes, is_encrypted=is_encrypted)

    write_mode = "wb" if output_format == PkmOutputFormat.BINARY else "w"
    with typer.open_file(output_file, mode=write_mode) as output:
        if output_format == PkmOutputFormat.BINARY:
            output.write(pkm.data)
        else:
            pretty_print.pkm(pkm, output)


@app.command()
def check(
    pkm_bytes_file: Optional[typer.FileBinaryRead] = None,
    save_file: Optional[typer.FileBinaryRead] = None,
    box_pos: Optional[tuple[int, int, int]] = None,
    output_file: typer.FileTextWrite = std_stream_default_opt,
):
    (pkm_bytes, is_encrypted) = get_pkm_bytes(pkm_bytes_file, save_file, box_pos)
    pkm = PcPkm.from_bytes(pkm_bytes, xor_substructures=is_encrypted)
    mail_words = list(MailWords.find_for_pkm(pkm))

    if not mail_words:
        print(
            textwrap.dedent(
                f"""
                😭😭😭 You're out of luck. 😭😭😭
                There are no easy chat words that can change this Pokémon's
                substructure order without transforming it into a Bad Egg
                """
            ).strip()
        )
        raise typer.Exit(63)

    print_words(mail_words, output_file, with_substructure_order=True)


@app.command()
def order(
    order: PkmSubstructuresOrder,
    pkm_bytes_file: Optional[typer.FileBinaryRead] = None,
    save_file: Optional[typer.FileBinaryRead] = None,
    box_pos: Optional[tuple[int, int, int]] = None,
    output_file: typer.FileTextWrite = std_stream_default_opt,
    output_format: WordsOutputFormat = WordsOutputFormat.PRETTY,
    limit: Optional[int] = None,
):
    (pkm_bytes, is_encrypted) = get_pkm_bytes(pkm_bytes_file, save_file, box_pos)
    pkm = PcPkm.from_bytes(pkm_bytes, xor_substructures=is_encrypted)
    mail_words = sorted(
        MailWords.find_for_substructure_order(pkm, order),
        key=lambda w: w.scroll_distance,
    )[:limit]

    if output_format == WordsOutputFormat.JSON:
        json.dump(mail_words, output_file, cls=PkmJSONSerializer)
    else:
        if not mail_words:
            print(
                textwrap.dedent(
                    f"""
                    😢😢😢 This can't be done. 😢😢😢
                    There are no easy chat words that can set this Pokémon's
                    substructure order to {order.name.upper()} without transforming it
                    into a Bad Egg
                    """
                ).strip()
            )
            raise typer.Exit(62)

        print_words(mail_words, output_file, with_substructure_order=False)


def get_pkm_bytes(
    pkm_bytes_file: Optional[typer.FileBinaryRead],
    save_file: Optional[typer.FileBinaryRead],
    box_pos: Optional[tuple[int, int, int]],
) -> tuple[bytes, bool]:
    match (pkm_bytes_file, save_file):
        case (None, None):
            raise typer.BadParameter(
                f"no Pokémon bytes input given.{os.linesep}"
                "Use either the --pkm-bytes-file option or "
                "the --save-file and --box-pos options.",
                param_hint=["--pkm-bytes-file", "--save-file"],
            )

        case (pkm_bytes, None):
            return (pkm_bytes.read(), False)

        case (None, save):
            if box_pos is None:
                raise typer.BadParameter(
                    f"missing option --box-pos.{os.linesep}"
                    "Option --box-pos is mandatory with --save-file.",
                    param_hint=["--save-file", "--box-pos"],
                )
            box, row, col = box_pos
            save_block = GameSaveBlock.from_bytes(save.read())
            return (save_block.pc.boxes[box - 1].raw_pkm_bytes(row - 1, col - 1), True)

        case (_, _):
            raise typer.BadParameter(
                f"too many Pokémon input bytes options.{os.linesep}"
                "Only one of the --pkm-bytes-file or --save-file options can be given.",
                param_hint=["--pkm-bytes-file", "--save-file"],
            )


def print_words(
    mail_words: list[MailWords], output: IO[str], *, with_substructure_order: bool
):
    mail_word_tables = (
        make_mail_words_table(words, with_substructure_order) for words in mail_words
    )
    console = Console(file=output)
    console.print(Columns(mail_word_tables, padding=(1, 1)))


def make_mail_words_table(words: MailWords, with_substructure_order: bool) -> Table:
    title = words.substructures_order.name if with_substructure_order else None
    table = Table(title=title, show_header=False, show_lines=True)
    table.add_row(word_str(words.top_left), word_str(words.top_right))
    table.add_row(word_str(words.bottom_left), word_str(words.bottom_right))
    return table


def word_str(word: easy_chat.Word | int) -> str:
    return (
        f"{word.text} ({word.category.value}, {format_hex(word.index, byte_size=2)})"
        if isinstance(word, easy_chat.Word)
        else "???"
    )
