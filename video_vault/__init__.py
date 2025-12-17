"""__init__ module."""

import typer

from video_vault.src.db.setup import setup_django

setup_django()

typer.echo("Calling setup_django() from __init__.py")
