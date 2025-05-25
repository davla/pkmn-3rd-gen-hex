import typer

from . import std_stream_default_arg
from .utils import PcPkm, pretty_print

app = typer.Typer()


@app.command()
def show(
    input_file: typer.FileBinaryRead = std_stream_default_arg,
    output_file: typer.FileTextWrite = std_stream_default_arg,
    encrypted: bool = False,
):
    pkm = PcPkm.from_bytes(input_file.read(), xor_substructures=encrypted)
    pretty_print.pkm(pkm, output_file)
