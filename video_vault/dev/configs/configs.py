"""Configs for pyrig.

All subclasses of ConfigFile in the configs package are automatically called.
"""

from winidjango.dev.configs.configs import (
    PyprojectConfigFile as WiniDjangoPyprojectConfigFile,
)
from winipyside.dev.configs.configs import (
    PyprojectConfigFile as WiniPySidePyprojectConfigFile,
)


class PyprojectConfigFile(WiniDjangoPyprojectConfigFile, WiniPySidePyprojectConfigFile):
    """Config file for pyproject.toml."""

    @classmethod
    def get_standard_dev_dependencies(cls) -> list[str]:
        """Get the standard dev dependencies."""
        standard_dev_dependencies = super().get_standard_dev_dependencies()
        standard_dev_dependencies.extend(
            [
                "yt-dlp-types",
            ]
        )
        return standard_dev_dependencies
