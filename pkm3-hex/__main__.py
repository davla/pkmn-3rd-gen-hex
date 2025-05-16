import typer

from .mail_glitch import app as mail_app
from .pkm_pc import app as pc_app

cli = typer.Typer()
cli.add_typer(pc_app, name="pkm-pc")
cli.add_typer(mail_app, name="mail-glitch")

if __name__ == "__main__":
    cli()
