"""module."""

from pytest_mock import MockerFixture
from winipedia_utils.utils.testing.assertions import assert_with_msg

from video_vault.ui.pages.downloads import Downloads as DownloadsPage
from video_vault.ui.windows.main import VideoVault


class TestVideoVault:
    """Test class for VideoVault."""

    def test_get_all_page_classes(self, mocker: MockerFixture) -> None:
        """Test method for get_all_page_classes."""
        # Mock the BasePage.get_subclasses method
        mock_page1 = mocker.Mock()
        mock_page2 = mocker.Mock()
        mock_page3 = mocker.Mock()
        expected_pages = [mock_page1, mock_page2, mock_page3]

        mock_get_subclasses = mocker.patch(
            "video_vault.ui.windows.main.BasePage.get_subclasses"
        )
        mock_get_subclasses.return_value = expected_pages

        # Call the class method
        result = VideoVault.get_all_page_classes()

        # Verify BasePage.get_subclasses was called with pages package
        mock_get_subclasses.assert_called_once()
        call_args = mock_get_subclasses.call_args[1]  # Get keyword arguments
        assert_with_msg("package" in call_args, "Should pass package parameter")

        # Verify the result
        assert_with_msg(
            result == expected_pages,
            "Should return the page classes from BasePage.get_subclasses",
        )

    def test_get_start_page_cls(self) -> None:
        """Test method for get_start_page_cls."""
        # Call the class method
        result = VideoVault.get_start_page_cls()

        # Verify it returns the DownloadsPage class
        assert_with_msg(
            result == DownloadsPage, "Should return DownloadsPage as start page class"
        )

    def test_pre_setup(self, mocker: MockerFixture) -> None:
        """Test method for pre_setup."""
        # Create a mock instance and call pre_setup
        window = VideoVault.__new__(VideoVault)  # Create without calling __init__

        # Mock the methods that pre_setup calls
        mock_get_svg_icon = mocker.patch.object(window, "get_svg_icon")
        mock_set_window_icon = mocker.patch.object(window, "setWindowIcon")
        mock_play_icon = mocker.Mock()
        mock_get_svg_icon.return_value = mock_play_icon

        # Call pre_setup
        window.pre_setup()

        # Verify the methods were called correctly
        mock_get_svg_icon.assert_called_once_with("play_icon")
        mock_set_window_icon.assert_called_once_with(mock_play_icon)

    def test_setup(self) -> None:
        """Test method for setup."""
        # Create a mock instance and call setup
        window = VideoVault.__new__(VideoVault)  # Create without calling __init__
        window.setup()

        # Since setup is empty, just verify it completed without error

    def test_post_setup(self) -> None:
        """Test method for post_setup."""
        # Create a mock instance and call post_setup
        window = VideoVault.__new__(VideoVault)  # Create without calling __init__
        window.post_setup()

        # Since post_setup is empty, just verify it completed without error
