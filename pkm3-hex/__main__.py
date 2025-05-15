import typer

from .pkm_pc import app as pc_app

cli = typer.Typer()
cli.add_typer(pc_app, name="pkm-pc")

if __name__ == "__main__":
    cli()
