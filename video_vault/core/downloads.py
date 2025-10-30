"""Downloads module.

This module contains functions to add downloads.
"""

import tempfile
from http.cookiejar import Cookie
from pathlib import Path
from typing import ClassVar

import yt_dlp
from PySide6.QtCore import QThread
from winipedia_pyside.ui.widgets.notification import Notification
from winipedia_utils.logging.logger import get_logger
from yt_dlp.utils import DownloadError

from video_vault.db.models import File
from video_vault.externals.ffmpeg import get_ffmpeg_path

logger = get_logger(__name__)


class DownloadWorker(QThread):
    """Worker to download a video."""

    ALL_WORKERS: ClassVar[list["DownloadWorker"]] = []

    def __init__(self, url: str, cookies: list[Cookie]) -> None:
        """Initialize the worker."""
        super().__init__()
        self.ALL_WORKERS.append(self)  # must be inplace
        self.url = url
        self.cookies = cookies
        self.finished.connect(self.on_finished)

    def run(self) -> None:
        """Run the worker."""
        try:
            self.file = add_download(self.url, self.cookies)
            self.name = self.file.display_name
            self.successful = True
            self.error = None
        except DownloadError as e:
            self.name = self.url
            self.successful = False
            self.error = e

    def on_finished(self) -> None:
        """Handle the result of the download."""
        self.show_notification()
        self.ALL_WORKERS.remove(self)
        self.update_downloads_page()

    def show_notification(self) -> None:
        """Show a popup with the result of the download."""
        notification = Notification(
            title=(
                f"Download {'succeeded' if self.successful else 'failed'}: {self.name}"
            ),
            text=f"Error: {self.error}",
        )
        notification.show()

    def update_downloads_page(self) -> None:
        """Update the downloads page."""
        from video_vault.ui.pages.downloads import (  # noqa: PLC0415
            Downloads as DownloadsPage,  # avoid circular import
        )

        if not self.successful:
            return

        downloads_page = DownloadsPage.get_page_static(DownloadsPage)
        downloads_page.add_download_button(self.file)


def add_download(url: str, cookies: list[Cookie]) -> File:
    """Add a download."""
    with tempfile.TemporaryDirectory() as tempdir:
        path = do_download(tempdir, url, cookies)
        return save_download(path)


def do_download(tempdir: str, url: str, cookies: list[Cookie]) -> Path:
    """Add a download."""
    logger.info("Adding download: %s", url)

    # make ydl options so we don not write to file
    ffmpeg_path = get_ffmpeg_path()
    ydl_opts: yt_dlp._Params = {
        "paths": {"home": tempdir},  # type: ignore[typeddict-item]
        "cookies": cookies,
        "ffmpeg_location": str(ffmpeg_path) if ffmpeg_path is not None else None,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
    except Exception as e:
        msg = f"Download failed: {e}"
        raise DownloadError(msg) from e

    return Path(ydl.prepare_filename(info))


def save_download(path: Path) -> File:
    """Save a download encryped to disk."""
    return File.create_encrypted(path)
