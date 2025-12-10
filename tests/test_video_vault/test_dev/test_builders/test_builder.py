"""module."""

from video_vault.dev.builders.builder import VideoVaultBuilder
from video_vault.src.db import migrations


class TestVideoVaultBuilder:
    """Test class."""

    def test_get_additional_resource_pkgs(self) -> None:
        """Test method."""
        assert VideoVaultBuilder.get_additional_resource_pkgs() == [migrations]
