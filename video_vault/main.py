"""Main entrypoint for the project."""

import logging
import os
import sys

from PySide6.QtWidgets import QApplication

from video_vault.src.db.setup import setup_django
from video_vault.src.ui.stylesheet import STYLESHEET
from video_vault.src.ui.windows.main import VideoVault as VideoVaultWindow

logger = logging.getLogger(__name__)


def main() -> None:
    """Main entrypoint for the project."""
    run()


def run() -> None:
    """Main function to run the application."""
    setup_django()
    # Create QApplication - this manages the entire app
    app = QApplication(sys.argv)

    # set global style sheet
    app.setStyleSheet(STYLESHEET)

    # Create and show the main window
    window = VideoVaultWindow()
    window.showMaximized()
    # Start the event loop (keeps the app running)
    # This will block until the user closes the window
    # if pytest is running exit with 0
    if "PYTEST_CURRENT_TEST" in os.environ:
        return
    logger.info("Starting event loop")
    app.exec()


if __name__ == "__main__":
    main()
