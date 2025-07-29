"""module."""

from pytest_mock import MockerFixture

from video_vault.ui.pages.add_downloads import AddDownloads


class TestAddDownloads:
    """Test class for AddDownloads."""

    def test_pre_setup(self, mocker: MockerFixture) -> None:
        """Test method for pre_setup."""
        # Mock the add_download_button method to verify it's called
        mock_add_download_button = mocker.patch.object(
            AddDownloads, "add_download_button"
        )

        # Create a mock instance and call pre_setup
        page = AddDownloads.__new__(AddDownloads)  # Create without calling __init__
        page.pre_setup()

        # Verify add_download_button was called
        mock_add_download_button.assert_called_once()

    def test_post_setup(self) -> None:
        """Test method for post_setup."""
        # Create a mock instance and call post_setup
        page = AddDownloads.__new__(AddDownloads)  # Create without calling __init__
        page.post_setup()

        # Since post_setup is empty, just verify it completed without error

    def test_add_download_button(self, mocker: MockerFixture) -> None:
        """Test method for add_download_button."""
        # Mock the UI methods to avoid Qt widget creation
        mocker.patch.object(AddDownloads, "get_svg_icon")
        mock_get_display_name = mocker.patch.object(AddDownloads, "get_display_name")
        mock_get_display_name.return_value = "AddDownloads"

        # Mock the layout and button creation
        mock_h_layout = mocker.Mock()
        mock_button = mocker.Mock()

        # Create a mock instance
        page = AddDownloads.__new__(AddDownloads)
        page.h_layout = mock_h_layout

        # Mock QPushButton creation
        mocker.patch(
            "video_vault.ui.pages.add_downloads.QPushButton", return_value=mock_button
        )
        page.add_download_button()

        # Verify button was configured correctly
        mock_button.setIcon.assert_called_once()
        mock_button.setSizePolicy.assert_called_once()
        mock_button.clicked.connect.assert_called_once()
        mock_h_layout.addWidget.assert_called_once_with(mock_button)
        mock_h_layout.setAlignment.assert_called_once()

    def test_on_add_download(self, mocker: MockerFixture) -> None:
        """Test method for on_add_download."""
        # Mock the DownloadWorker to avoid actual downloads
        mock_download_worker = mocker.patch(
            "video_vault.ui.pages.add_downloads.DownloadWorker"
        )
        mock_worker_instance = mocker.Mock()
        mock_download_worker.return_value = mock_worker_instance

        # Create a mock instance
        page = AddDownloads.__new__(AddDownloads)

        # Mock the browser
        mock_browser = mocker.Mock()
        page.browser = mock_browser

        # Set up mock URL and cookies
        mock_url = mocker.Mock()
        mock_url.host.return_value = "www.youtube.com"
        mock_url.toString.return_value = "https://www.youtube.com/watch?v=805SIqgDZIE"
        mock_browser.url.return_value = mock_url
        mock_browser.get_domain_http_cookies.return_value = []

        # Call on_add_download
        page.on_add_download()

        # Verify DownloadWorker was created with correct parameters
        mock_download_worker.assert_called_once_with(
            url="https://www.youtube.com/watch?v=805SIqgDZIE", cookies=[]
        )

        # Verify worker was started
        mock_worker_instance.start.assert_called_once()
