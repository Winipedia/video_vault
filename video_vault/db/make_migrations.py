"""Script to create migrations for the video_vault.db app."""

from django.core.management import call_command
from winipedia_utils.utils.logging.logger import get_logger

from video_vault import db

logger = get_logger(__name__)

if __name__ == "__main__":
    # Configure Django settings
    logger.info(
        "Importing %s creates the setup automatically via its __init__.py", db.__name__
    )

    # Create migrations
    call_command("makemigrations", "db")
