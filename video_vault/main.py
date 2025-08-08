"""The main module.

This module contains the main function to run the application.
"""

import sys

from PySide6.QtWidgets import QApplication

from video_vault.db.setup import setup_django
from video_vault.ui.stylesheet import STYLESHEET
from video_vault.ui.windows.main import VideoVault as VideoVaultWindow


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
    app.exec()


if __name__ == "__main__":
    main()
