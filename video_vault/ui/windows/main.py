"""Main window module.

This module contains the main window class for the VideoVault application.
"""

from winipedia_utils.pyside.ui.pages.base.base import Base as BasePage
from winipedia_utils.pyside.ui.windows.base.base import Base as BaseWindow

from video_vault.ui import pages
from video_vault.ui.pages.downloads import Downloads as DownloadsPage


class VideoVault(BaseWindow):
    """Main window for the VideoVault application."""

    @classmethod
    def get_all_page_classes(cls) -> list[type[BasePage]]:
        """Get all page classes."""
        return BasePage.get_subclasses(package=pages)

    @classmethod
    def get_start_page_cls(cls) -> type[DownloadsPage]:
        """Get the start page class."""
        return DownloadsPage

    def pre_setup(self) -> None:
        """Setup the UI."""

    def setup(self) -> None:
        """Setup the UI."""

    def post_setup(self) -> None:
        """Setup the UI."""
