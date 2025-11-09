"""module."""

from pathlib import Path

from pytest_mock import MockerFixture
from winipedia_utils.utils.testing.assertions import assert_with_msg

from video_vault.ui.pages.player import Player


class TestPlayer:
    """Test class for Player."""

    def test_pre_setup(self) -> None:
        """Test method for pre_setup."""
        # Create a mock instance and call pre_setup
        player = Player.__new__(Player)  # Create without calling __init__
        player.pre_setup()

        # Since pre_setup is empty, just verify it completed without error

    def test_post_setup(self) -> None:
        """Test method for post_setup."""
        # Create a mock instance and call post_setup
        player = Player.__new__(Player)  # Create without calling __init__
        player.post_setup()

        # Verify current_file was set to None
        assert_with_msg(
            player.current_file is None, "current_file should be set to None"
        )

    def test_play_download(self, mocker: MockerFixture) -> None:
        """Test method for play_download."""
        # Create a mock instance
        player = Player.__new__(Player)
        player.current_file = None

        # Mock the media player and start_playback method
        mock_media_player = mocker.Mock()
        mock_media_player.position.return_value = 2500
        player.media_player = mock_media_player
        mock_start_playback = mocker.patch.object(player, "start_playback")

        # Create a mock download file
        mock_download = mocker.Mock()
        mock_download.file.path = "/fake/path/video.mp4"
        mock_download.last_position = 1500

        # Call play_download
        player.play_download(mock_download)

        # Verify download was refreshed from database
        mock_download.refresh_from_db.assert_called_once()

        # Verify current_file was set
        assert_with_msg(
            player.current_file == mock_download,
            "current_file should be set to download",
        )

        # Verify start_playback was called with correct parameters
        mock_start_playback.assert_called_once_with(Path("/fake/path/video.mp4"), 1500)

    def test_play_download_with_existing_file(self, mocker: MockerFixture) -> None:
        """Test method for play_download when there's already a current file."""
        # Create a mock instance with existing current file
        player = Player.__new__(Player)

        # Mock existing current file
        mock_existing_file = mocker.Mock()
        mock_existing_file.last_position = 0
        player.current_file = mock_existing_file

        # Mock the media player
        mock_media_player = mocker.Mock()
        mock_media_player.position.return_value = 2500
        player.media_player = mock_media_player
        mock_start_playback = mocker.patch.object(player, "start_playback")

        # Create a mock new download file
        mock_download = mocker.Mock()
        mock_download.file.path = "/fake/path/new_video.mp4"
        mock_download.last_position = 1000

        # Call play_download
        player.play_download(mock_download)

        # Verify existing file position was saved
        expected_position = 2500
        assert_with_msg(
            mock_existing_file.last_position == expected_position,
            "Existing file position should be saved",
        )
        mock_existing_file.save.assert_called_once()

        # Verify new file was set as current
        assert_with_msg(
            player.current_file == mock_download,
            "current_file should be set to new download",
        )

        # Verify start_playback was called with new file parameters
        mock_start_playback.assert_called_once_with(
            Path("/fake/path/new_video.mp4"), 1000
        )

    def test_start_playback(self, mocker: MockerFixture) -> None:
        """Test method for start_playback."""
        # Mock the security function and play_encrypted_file method
        mock_aes_gcm = mocker.Mock()
        mock_get_or_create_app_aes_gcm = mocker.patch(
            "video_vault.ui.pages.player.get_or_create_app_aes_gcm"
        )
        mock_get_or_create_app_aes_gcm.return_value = mock_aes_gcm

        # Create a mock instance
        player = Player.__new__(Player)
        mock_play_encrypted_file = mocker.patch.object(player, "play_encrypted_file")

        # Test parameters
        test_path = Path("/fake/path/video.mp4")
        test_position = 1500

        # Call start_playback
        player.start_playback(test_path, test_position)

        # Verify AES GCM was retrieved
        mock_get_or_create_app_aes_gcm.assert_called_once()

        # Verify play_encrypted_file was called with correct parameters
        mock_play_encrypted_file.assert_called_once_with(
            test_path, mock_aes_gcm, test_position
        )

    def test_start_playback_default_position(self, mocker: MockerFixture) -> None:
        """Test method for start_playback with default position."""
        # Mock the security function and play_encrypted_file method
        mock_aes_gcm = mocker.Mock()
        mock_get_or_create_app_aes_gcm = mocker.patch(
            "video_vault.ui.pages.player.get_or_create_app_aes_gcm"
        )
        mock_get_or_create_app_aes_gcm.return_value = mock_aes_gcm

        # Create a mock instance
        player = Player.__new__(Player)
        mock_play_encrypted_file = mocker.patch.object(player, "play_encrypted_file")

        # Test parameters (no position provided, should default to 0)
        test_path = Path("/fake/path/video.mp4")

        # Call start_playback without position
        player.start_playback(test_path)

        # Verify play_encrypted_file was called with default position 0
        mock_play_encrypted_file.assert_called_once_with(test_path, mock_aes_gcm, 0)

    def test_stop_playback(self, mocker: MockerFixture) -> None:
        """Test method for stop_playback."""
        # Create a mock instance
        player = Player.__new__(Player)

        # Mock the media player
        mock_media_player = mocker.Mock()
        expected_position = 3000
        mock_media_player.position.return_value = expected_position
        player.media_player = mock_media_player

        # Mock current file
        mock_current_file = mocker.Mock()
        mock_current_file.last_position = 0
        player.current_file = mock_current_file

        # Call stop_playback
        player.stop_playback()

        # Verify position was saved
        assert_with_msg(
            mock_current_file.last_position == expected_position,
            "Current file position should be saved",
        )
        mock_current_file.save.assert_called_once()

        # Verify current_file was set to None
        assert_with_msg(
            player.current_file is None, "current_file should be set to None"
        )

        # Verify media player was stopped
        mock_media_player.stop_and_close_io_device.assert_called_once()
