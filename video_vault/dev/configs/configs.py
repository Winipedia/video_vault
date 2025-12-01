"""Configs for pyrig.

All subclasses of ConfigFile in the configs package are automatically called.
"""

from pyrig.dev.configs.pyproject import PyprojectConfigFile as PyrigPyprojectConfigFile


class PyprojectConfigFile(PyrigPyprojectConfigFile):
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
