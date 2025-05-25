import typer

from .mail_glitch import app as mail_app
from .pc_pkm import app as pc_pkm_app
from .pkm import app as pkm_app

cli = typer.Typer()
cli.add_typer(pkm_app, name="pkm")
cli.add_typer(pc_pkm_app, name="pc-pkm")
cli.add_typer(mail_app, name="mail-glitch")

if __name__ == "__main__":
    cli()
