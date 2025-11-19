"""module."""

import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

from pyrig.src.modules.module import make_obj_importpath
from pyrig.src.testing.assertions import assert_with_msg
from pytest_mock import MockerFixture

from video_vault.src.core import downloads as downloads_module
from video_vault.src.core.downloads import (
    DownloadWorker,
    add_download,
    do_download,
    save_download,
)
from video_vault.src.ui.pages import downloads as downloads_page_module

if TYPE_CHECKING:
    from http.cookiejar import Cookie


def test_add_download(mocker: MockerFixture, tmp_path: Path) -> None:
    """Test func for add_download."""
    test_url = "https://www.youtube.com/watch?v=805SIqgDZIE"
    cookies: list[Cookie] = []

    # Create a fake video file for testing
    fake_video_file = tmp_path / "test_video.mp4"
    fake_video_file.write_bytes(b"fake video content for testing")

    # Mock the YoutubeDL instance methods
    mock_ydl_instance = mocker.Mock()
    mock_ydl_instance.extract_info.return_value = {"title": "Test Video"}
    mock_ydl_instance.prepare_filename.return_value = str(fake_video_file)

    # Mock the YoutubeDL constructor to return our mock instance
    mock_ydl_class = mocker.patch(
        make_obj_importpath(downloads_module) + ".yt_dlp.YoutubeDL"
    )
    mock_ydl_class.return_value.__enter__.return_value = mock_ydl_instance

    result = add_download(test_url, cookies)

    assert_with_msg(result.file.name != "", "File should have a name")
    assert_with_msg(result.display_name != "", "File should have a display name")
    mock_ydl_instance.extract_info.assert_called_once_with(test_url, download=True)


def test_do_download(mocker: MockerFixture, tmp_path: Path) -> None:
    """Test func for do_download."""
    test_url = "https://www.youtube.com/watch?v=805SIqgDZIE"
    cookies: list[Cookie] = []

    # Create a fake video file for testing
    fake_video_file = tmp_path / "test_video.mp4"
    fake_video_file.write_bytes(b"fake video content for testing")

    # Mock the YoutubeDL instance methods
    mock_ydl_instance = mocker.Mock()
    mock_ydl_instance.extract_info.return_value = {"title": "Test Video"}
    mock_ydl_instance.prepare_filename.return_value = str(fake_video_file)

    # Mock the YoutubeDL constructor to return our mock instance
    mock_ydl_class = mocker.patch(
        make_obj_importpath(downloads_module) + ".yt_dlp.YoutubeDL"
    )
    mock_ydl_class.return_value.__enter__.return_value = mock_ydl_instance

    with tempfile.TemporaryDirectory() as tempdir:
        result = do_download(tempdir, test_url, cookies)

        assert_with_msg(result.exists(), "Downloaded file should exist")
        assert_with_msg(
            result.stat().st_size > 0, "Downloaded file should not be empty"
        )
        mock_ydl_instance.extract_info.assert_called_once_with(test_url, download=True)
        mock_ydl_instance.prepare_filename.assert_called_once()


def test_save_download(tmp_path: Path) -> None:
    """Test func for save_download."""
    # Create a test file
    test_file = tmp_path / "test_video.mp4"
    test_content = b"fake video content for testing"
    test_file.write_bytes(test_content)

    result = save_download(test_file)

    assert_with_msg(result.file.name != "", "File should have a name")
    assert_with_msg(result.display_name != "", "File should have a display name")


class TestDownloadWorker:
    """Test class for DownloadWorker."""

    def test___init__(self) -> None:
        """Test method for __init__."""
        test_url = "https://www.youtube.com/watch?v=805SIqgDZIE"
        cookies: list[Cookie] = []

        worker = DownloadWorker(test_url, cookies)

        assert_with_msg(worker.url == test_url, "URL should be set correctly")
        assert_with_msg(worker.cookies == cookies, "Cookies should be set correctly")
        assert_with_msg(
            worker in DownloadWorker.ALL_WORKERS,
            "Worker should be added to ALL_WORKERS",
        )

    def test_run(self, mocker: MockerFixture) -> None:
        """Test method for run."""
        test_url = "https://www.youtube.com/watch?v=805SIqgDZIE"
        cookies: list[Cookie] = []

        # Mock only the download function, not Qt components
        mock_add_download = mocker.patch(
            make_obj_importpath(downloads_module) + ".add_download"
        )
        mock_file = mocker.Mock()
        mock_file.display_name = "Test Video"
        mock_add_download.return_value = mock_file

        worker = DownloadWorker(test_url, cookies)
        worker.run()

        assert_with_msg(worker.file == mock_file, "File should be set")
        assert_with_msg(
            worker.name == "Test Video", "Name should be set from file display_name"
        )
        assert_with_msg(worker.successful is True, "Should be marked as successful")
        assert_with_msg(worker.error is None, "Error should be None on success")

    def test_on_finished(self, mocker: MockerFixture) -> None:
        """Test method for on_finished."""
        test_url = "https://www.youtube.com/watch?v=805SIqgDZIE"
        cookies: list[Cookie] = []

        # Mock only the methods, not Qt initialization
        mock_show_notification = mocker.patch.object(
            DownloadWorker, "show_notification"
        )
        mock_update_downloads_page = mocker.patch.object(
            DownloadWorker, "update_downloads_page"
        )

        worker = DownloadWorker(test_url, cookies)
        initial_worker_count = len(DownloadWorker.ALL_WORKERS)

        worker.on_finished()

        mock_show_notification.assert_called_once()
        mock_update_downloads_page.assert_called_once()
        assert_with_msg(
            len(DownloadWorker.ALL_WORKERS) == initial_worker_count - 1,
            "Worker should be removed from ALL_WORKERS",
        )

    def test_show_notification(self, mocker: MockerFixture) -> None:
        """Test method for show_notification."""
        test_url = "https://www.youtube.com/watch?v=805SIqgDZIE"
        cookies: list[Cookie] = []

        # Mock only the notification
        mock_notification = mocker.patch(
            make_obj_importpath(downloads_module) + ".Notification"
        )
        mock_notification_instance = mocker.Mock()
        mock_notification.return_value = mock_notification_instance

        worker = DownloadWorker(test_url, cookies)
        worker.successful = True
        worker.name = "Test Video"
        worker.error = None

        worker.show_notification()

        mock_notification.assert_called_once()
        mock_notification_instance.show.assert_called_once()

    def test_update_downloads_page(self, mocker: MockerFixture) -> None:
        """Test method for update_downloads_page."""
        test_url = "https://www.youtube.com/watch?v=805SIqgDZIE"
        cookies: list[Cookie] = []

        # Mock the Downloads page import inside the method
        mock_downloads_page = mocker.patch(
            make_obj_importpath(downloads_page_module) + ".Downloads"
        )
        mock_page_instance = mocker.Mock()
        mock_downloads_page.get_page_static.return_value = mock_page_instance

        worker = DownloadWorker(test_url, cookies)
        worker.successful = True
        worker.file = mocker.Mock()

        worker.update_downloads_page()

        mock_downloads_page.get_page_static.assert_called_once_with(mock_downloads_page)
        mock_page_instance.add_download_button.assert_called_once_with(worker.file)
