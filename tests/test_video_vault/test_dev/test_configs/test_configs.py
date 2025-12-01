"""module."""

from video_vault.dev.configs.configs import PyprojectConfigFile


class TestPyprojectConfigFile:
    """Test class."""

    def test_get_standard_dev_dependencies(self) -> None:
        """Test method."""
        standard_dev_dependencies = PyprojectConfigFile.get_standard_dev_dependencies()
        assert isinstance(standard_dev_dependencies, list)
        assert "yt-dlp-types" in standard_dev_dependencies
