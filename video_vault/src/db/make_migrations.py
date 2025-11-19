"""Script to create migrations for the video_vault.db app."""

import logging

from django.core.management import call_command

from video_vault.src import db

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Configure Django settings
    logger.info(
        "Importing %s creates the setup automatically via its __init__.py", db.__name__
    )

    # Create migrations
    call_command("makemigrations", "db")
