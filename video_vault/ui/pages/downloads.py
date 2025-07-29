"""Downloads page module.

This module contains the downloads page class for the VideoVault application.
"""

from functools import partial
from pathlib import Path
from typing import final

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMenu,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)
from winipedia_utils.pyside.ui.pages.base.base import Base as BasePage

from video_vault.db.models import File


class Downloads(BasePage):
    """Downloads page for the VideoVault application."""

    @final
    def pre_setup(self) -> None:
        """Setup the UI."""

    @final
    def setup(self) -> None:
        """Setup the UI."""
        # add button in the top right to add a download
        self.add_add_downloads_button()
        self.add_download_buttons_scroll_area()

    @final
    def post_setup(self) -> None:
        """Setup the UI."""

    @final
    def add_add_downloads_button(self) -> None:
        """Add a button to add a download."""
        from video_vault.ui.pages.add_downloads import AddDownloads as AddDownloadsPage

        # now make the button top right in the layout, QV doesn't support this
        # so add a horizontal layout to the top row
        button = self.add_to_page_button(
            to_page_cls=AddDownloadsPage, layout=self.h_layout
        )
        button.setIcon(self.get_svg_icon("plus_icon"))
        # we need the button to be small
        button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        # align the button to the right
        self.h_layout.setAlignment(
            button, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop
        )

    @final
    def add_download_buttons_scroll_area(self) -> None:
        """Add a list of downloads to scroll through and on click the video plays."""
        self.downloads = File.objects.all().order_by("-created_at")

        self.downloads_widget = QWidget()
        self.downloads_layout = QVBoxLayout(self.downloads_widget)
        self.downloads_layout.setSpacing(10)
        self.downloads_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # for each download add a button with the name of the download
        self.button_to_download: dict[QPushButton, File] = {}
        for download in self.downloads:
            self.add_download_button(download)

        # Scroll area setup
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.downloads_widget)

        # Add the scroll area to the main layout
        self.v_layout.addWidget(scroll_area)

    @final
    def play_download(self, download: File) -> None:
        """Play the video."""
        from video_vault.ui.pages.player import Player as PlayerPage

        download.refresh_from_db()

        player_page = self.get_page(PlayerPage)

        # if already a video is playing then save its position
        if player_page.current_file is not None:
            player_page.current_file.last_position = player_page.media_player.position()
            player_page.current_file.save()
        player_page.current_file = download

        player_page.start_playback(Path(download.file.path), download.last_position)

    @final
    def add_download_button(self, download: File) -> None:
        """Add a download to the list."""
        # check if display name
        button = QPushButton(download.display_name)
        self.button_to_download[button] = download
        self.downloads_layout.addWidget(button)
        # give the button a QMenu with play and delete
        menu = QMenu(self)

        play_action = menu.addAction("Play")
        play_action.setIcon(self.get_svg_icon("play_icon"))
        play_action.triggered.connect(partial(self.play_download, download))

        delete_action = menu.addAction("Delete")
        delete_action.setIcon(self.get_svg_icon("delete_garbage_can"))
        delete_action.triggered.connect(
            partial(self.remove_download_and_button, button)
        )

        button.setMenu(menu)

    @final
    def remove_download_and_button(self, download_button: QPushButton) -> None:
        """Remove a download from the list."""
        file = self.button_to_download[download_button]
        file.delete_file()
        self.downloads_layout.removeWidget(download_button)
        download_button.deleteLater()
        del self.button_to_download[download_button]
