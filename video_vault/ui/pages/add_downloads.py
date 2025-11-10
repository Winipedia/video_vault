"""Add downloads page module.

This module contains the add downloads page class for the VideoVault application.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QPushButton,
    QSizePolicy,
)
from winipedia_pyside.utils.ui.pages.browser import Browser as BrowserPage

from video_vault.core.downloads import DownloadWorker


class AddDownloads(BrowserPage):
    """Add downloads page for the VideoVault application."""

    def pre_setup(self) -> None:
        """Setup the UI."""
        # add a download button in the top right
        self.add_download_button()

    def post_setup(self) -> None:
        """Setup the UI."""

    def add_download_button(self) -> None:
        """Add a download button."""
        download_arrow_icon = self.get_svg_icon("download_arrow")
        button = QPushButton(self.get_display_name().removesuffix("s"))
        button.setIcon(download_arrow_icon)
        # we need the button to be small
        button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        # connect to add download
        button.clicked.connect(self.on_add_download)
        # add button to layout
        self.h_layout.addWidget(button)
        # align the button to the right
        self.h_layout.setAlignment(
            button, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop
        )

    def on_add_download(self) -> None:
        """Add a download."""
        url = self.browser.url()
        domain = url.host()
        http_cookies = self.browser.get_domain_http_cookies(domain)
        worker = DownloadWorker(url=url.toString(), cookies=http_cookies)
        worker.start()
