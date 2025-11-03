"""module."""

from pathlib import Path

from pytest_mock import MockerFixture
from winipedia_utils.testing.assertions import assert_with_msg

from video_vault.ui.pages.downloads import Downloads


class TestDownloads:
    """Test class for Downloads."""

    def test_pre_setup(self) -> None:
        """Test method for pre_setup."""
        # Create a mock instance and call pre_setup
        page = Downloads.__new__(Downloads)  # Create without calling __init__
        page.pre_setup()

        # Since pre_setup is empty, just verify it completed without error

    def test_setup(self, mocker: MockerFixture) -> None:
        """Test method for setup."""
        # Mock the methods that setup calls
        mock_add_add_downloads_button = mocker.patch.object(
            Downloads, "add_add_downloads_button"
        )
        mock_add_download_buttons_scroll_area = mocker.patch.object(
            Downloads, "add_download_buttons_scroll_area"
        )
        mock_add_delete_all_downloads_button = mocker.patch.object(
            Downloads, "add_delete_all_downloads_button"
        )

        # Create a mock instance and call setup
        page = Downloads.__new__(Downloads)
        page.setup()

        # Verify both methods were called
        mock_add_add_downloads_button.assert_called_once()
        mock_add_download_buttons_scroll_area.assert_called_once()
        mock_add_delete_all_downloads_button.assert_called_once()

    def test_post_setup(self) -> None:
        """Test method for post_setup."""
        # Create a mock instance and call post_setup
        page = Downloads.__new__(Downloads)  # Create without calling __init__
        page.post_setup()

        # Since post_setup is empty, just verify it completed without error

    def test_add_delete_all_downloads_button(self, mocker: MockerFixture) -> None:
        """Test method for add_delete_all_downloads_button."""
        # Mock the UI methods to avoid Qt widget creation
        mock_h_layout = mocker.Mock()
        mock_button = mocker.Mock()
        mocker.patch(
            "video_vault.ui.pages.downloads.QPushButton", return_value=mock_button
        )
        mocker.patch.object(Downloads, "get_svg_icon")

        # Create a mock instance
        page = Downloads.__new__(Downloads)
        page.h_layout = mock_h_layout

        # Call add_delete_all_downloads_button
        page.add_delete_all_downloads_button()

        # Verify button was added to layout
        mock_h_layout.addWidget.assert_called_once_with(mock_button)
        # Verify alignment was set
        mock_h_layout.setAlignment.assert_called_once()
        # Verify button was configured
        mock_button.setIcon.assert_called_once()
        mock_button.setSizePolicy.assert_called_once()

    def test_on_delete_all_downloads(self, mocker: MockerFixture) -> None:
        """Test method for on_delete_all_downloads."""
        # Mock File.objects to get all downloads
        mock_file1 = mocker.Mock()
        mock_file2 = mocker.Mock()
        mock_files = [mock_file1, mock_file2]

        mock_file_objects = mocker.patch("video_vault.ui.pages.downloads.File.objects")
        mock_file_objects.all.return_value = mock_files

        # Mock remove_download_and_button method
        mock_remove = mocker.patch.object(Downloads, "remove_download_and_button")

        # Create a mock instance with button_to_download mapping
        page = Downloads.__new__(Downloads)
        mock_button1 = mocker.Mock()
        mock_button2 = mocker.Mock()
        page.button_to_download = {mock_button1: mock_file1, mock_button2: mock_file2}

        # Call on_delete_all_downloads
        page.on_delete_all_downloads()

        # Verify remove_download_and_button was called for each download
        expected_call_count = 2
        assert_with_msg(
            mock_remove.call_count == expected_call_count,
            "Should call remove_download_and_button for each download",
        )
        mock_remove.assert_any_call(mock_button1)
        mock_remove.assert_any_call(mock_button2)

    def test_add_add_downloads_button(self, mocker: MockerFixture) -> None:
        """Test method for add_add_downloads_button."""
        # Mock the UI methods to avoid Qt widget creation
        mock_add_to_page_button = mocker.patch.object(Downloads, "add_to_page_button")
        mocker.patch.object(Downloads, "get_svg_icon")
        mock_button = mocker.Mock()
        mock_add_to_page_button.return_value = mock_button
        mock_h_layout = mocker.Mock()

        # Create a mock instance
        page = Downloads.__new__(Downloads)
        page.h_layout = mock_h_layout

        # Call add_add_downloads_button
        page.add_add_downloads_button()

        # Verify button was configured correctly
        mock_add_to_page_button.assert_called_once()
        mock_button.setIcon.assert_called_once()
        mock_button.setSizePolicy.assert_called_once()
        mock_h_layout.setAlignment.assert_called_once()

    def test_add_download_buttons_scroll_area(self, mocker: MockerFixture) -> None:
        """Test method for add_download_buttons_scroll_area."""
        # Mock File.objects to avoid database calls
        mock_file1 = mocker.Mock()
        mock_file1.display_name = "Video 1"
        mock_file2 = mocker.Mock()
        mock_file2.display_name = "Video 2"
        mock_files = [mock_file1, mock_file2]

        mock_file_objects = mocker.patch("video_vault.ui.pages.downloads.File.objects")
        mock_file_objects.all.return_value.order_by.return_value = mock_files

        # Mock Qt widgets
        mock_widget = mocker.Mock()
        mock_layout = mocker.Mock()
        mock_scroll_area = mocker.Mock()
        mock_v_layout = mocker.Mock()

        mocker.patch("video_vault.ui.pages.downloads.QWidget", return_value=mock_widget)
        mocker.patch(
            "video_vault.ui.pages.downloads.QVBoxLayout", return_value=mock_layout
        )
        mocker.patch(
            "video_vault.ui.pages.downloads.QScrollArea", return_value=mock_scroll_area
        )

        # Mock the add_download_button method
        mock_add_download_button = mocker.patch.object(Downloads, "add_download_button")

        # Create a mock instance
        page = Downloads.__new__(Downloads)
        page.v_layout = mock_v_layout

        # Call add_download_buttons_scroll_area
        page.add_download_buttons_scroll_area()

        # Verify downloads were fetched and buttons were created
        mock_file_objects.all.assert_called_once()
        mock_file_objects.all.return_value.order_by.assert_called_once_with(
            "-created_at"
        )

        # Verify add_download_button was called for each file
        expected_call_count = 2
        assert_with_msg(
            mock_add_download_button.call_count == expected_call_count,
            "Should call add_download_button for each file",
        )
        mock_add_download_button.assert_any_call(mock_file1)
        mock_add_download_button.assert_any_call(mock_file2)

        # Verify scroll area was set up
        mock_scroll_area.setWidget.assert_called_once_with(mock_widget)
        mock_v_layout.addWidget.assert_called_once_with(mock_scroll_area)

    def test_play_download(self, mocker: MockerFixture) -> None:
        """Test method for play_download."""
        # Mock the Player page and its methods
        mock_player_page = mocker.Mock()
        mock_player_page.current_file = None
        mock_get_page = mocker.patch.object(Downloads, "get_page")
        mock_get_page.return_value = mock_player_page

        # Create a mock download file
        mock_download = mocker.Mock()
        mock_download.file.path = "/fake/path/video.mp4"
        mock_download.last_position = 1500

        # Create a mock instance
        page = Downloads.__new__(Downloads)

        # Call play_download
        page.play_download(mock_download)

        # Verify download was refreshed from database
        mock_download.refresh_from_db.assert_called_once()

        # Verify player page was retrieved and configured
        mock_get_page.assert_called_once()
        assert_with_msg(
            mock_player_page.current_file == mock_download,
            "Player page should have current file set",
        )

        # Verify playback was started with correct parameters
        mock_player_page.start_playback.assert_called_once_with(
            Path("/fake/path/video.mp4"), 1500
        )

    def test_add_download_button(self, mocker: MockerFixture) -> None:
        """Test method for add_download_button."""
        # Mock Qt widgets and methods
        mock_button = mocker.Mock()
        mock_menu = mocker.Mock()
        mock_play_action = mocker.Mock()
        mock_delete_action = mocker.Mock()
        mock_downloads_layout = mocker.Mock()

        mock_qpushbutton = mocker.patch(
            "video_vault.ui.pages.downloads.QPushButton", return_value=mock_button
        )
        mocker.patch("video_vault.ui.pages.downloads.QMenu", return_value=mock_menu)
        mock_menu.addAction.side_effect = [mock_play_action, mock_delete_action]
        mocker.patch.object(Downloads, "get_svg_icon")

        # Create a mock download file
        mock_download = mocker.Mock()
        mock_download.display_name = "Test Video"

        # Create a mock instance
        page = Downloads.__new__(Downloads)
        page.downloads_layout = mock_downloads_layout
        page.button_to_download = {}

        # Call add_download_button
        page.add_download_button(mock_download)

        # Verify button was created with correct text
        mock_qpushbutton.assert_called_once_with("Test Video")

        # Verify button was added to layout and mapping
        mock_downloads_layout.addWidget.assert_called_once_with(mock_button)
        assert_with_msg(
            page.button_to_download[mock_button] == mock_download,
            "Button should be mapped to download",
        )

        # Verify menu was created and configured
        mock_menu.addAction.assert_any_call("Play")
        mock_menu.addAction.assert_any_call("Delete")
        mock_play_action.setIcon.assert_called_once()
        mock_delete_action.setIcon.assert_called_once()
        mock_button.setMenu.assert_called_once_with(mock_menu)

    def test_remove_download_and_button(self, mocker: MockerFixture) -> None:
        """Test method for remove_download_and_button."""
        # Mock the Player page and its methods
        mock_player_page = mocker.Mock()
        mock_player_page.current_file = None
        mock_get_page = mocker.patch.object(Downloads, "get_page")
        mock_get_page.return_value = mock_player_page

        # Mock the download file and its delete method
        mock_file = mocker.Mock()
        mock_downloads_layout = mocker.Mock()
        mock_button = mocker.Mock()

        # Create a mock instance
        page = Downloads.__new__(Downloads)
        page.downloads_layout = mock_downloads_layout
        page.button_to_download = {mock_button: mock_file}

        # Call remove_download_and_button
        page.remove_download_and_button(mock_button)

        # Verify get_page was called to get player page
        mock_get_page.assert_called_once()

        # Verify file was deleted
        mock_file.delete_file.assert_called_once()

        # Verify button was removed from layout and mapping
        mock_downloads_layout.removeWidget.assert_called_once_with(mock_button)
        mock_button.deleteLater.assert_called_once()
        assert_with_msg(
            mock_button not in page.button_to_download,
            "Button should be removed from mapping",
        )
