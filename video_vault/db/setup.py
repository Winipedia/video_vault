"""Database setup module.

This module contains the database settings.
In the init we setup django settings and create the db if not existent.
"""

import sys
from io import StringIO
from pathlib import Path

import django
from django.conf import settings
from django.core.management import call_command
from platformdirs import user_data_dir

from video_vault.core.consts import APP_NAME, AUTHOR
from video_vault.core.security import get_app_key_as_str


def setup_django() -> None:
    """Setup the database."""
    if settings.configured:
        return
    root_dir = Path(user_data_dir(APP_NAME, AUTHOR, ensure_exists=True))
    media_root = root_dir / "media"
    media_root.mkdir(parents=True, exist_ok=True)

    db_path = root_dir / "db" / "db.sqlite3"
    db_path.parent.mkdir(parents=True, exist_ok=True)

    settings.configure(
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": str(db_path),
            }
        },
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "video_vault.db",
        ],
        MEDIA_ROOT=media_root,
        MEDIA_URL="/media/",
        SECRET_KEY=get_app_key_as_str(),
    )

    django.setup()

    if sys.stdout is None:
        sys.stdout = StringIO()
    if sys.stderr is None:
        sys.stderr = StringIO()

    call_command("migrate")
