"""Build script.

All subclasses of Builder in the builds package are automatically called.
"""

from types import ModuleType

from pyrig.dev.artifacts.builders.base.base import PyInstallerBuilder

from video_vault.src.db import migrations


class VideoVaultBuilder(PyInstallerBuilder):
    """Build class for video_vault."""

    @classmethod
    def get_additional_resource_pkgs(cls) -> list[ModuleType]:
        """Get additional resource packages."""
        return [migrations]
