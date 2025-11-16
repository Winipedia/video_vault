"""The main module.

This module contains the main function to run the application.
"""

import os
import sys

from PySide6.QtWidgets import QApplication

from video_vault.app.db.setup import setup_django
from video_vault.app.ui.stylesheet import STYLESHEET
from video_vault.app.ui.windows.main import VideoVault as VideoVaultWindow


def main() -> None:
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
        sys.exit(0)
    app.exec()
