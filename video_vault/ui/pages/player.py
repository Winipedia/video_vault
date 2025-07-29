"""Player page module.

This module contains the player page class for the VideoVault application.
"""

from pathlib import Path
from typing import final

from winipedia_utils.pyside.ui.pages.player import Player as PlayerPage

from video_vault.core.security import get_or_create_app_aes_gcm
from video_vault.db.models import File


class Player(PlayerPage):
    """Player page for the VideoVault application."""

    @final
    def pre_setup(self) -> None:
        """Setup the UI."""

    @final
    def post_setup(self) -> None:
        """Setup the UI."""
        self.current_file: File | None = None

    @final
    def play_download(self, download: File) -> None:
        """Play the video."""
        download.refresh_from_db()
        if self.current_file is not None:
            self.current_file.last_position = self.media_player.position()
            self.current_file.save()
        self.current_file = download
        self.start_playback(Path(download.file.path), download.last_position)

    @final
    def start_playback(self, path: Path, position: int = 0) -> None:
        """Start playback."""
        aes_gcm = get_or_create_app_aes_gcm()
        self.play_encrypted_file(path, aes_gcm, position)
