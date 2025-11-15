"""Build script.

All subclasses of Builder in the builds package are automatically called.
"""

from pathlib import Path

import winipedia_utils
from winipedia_utils.dev.artifacts.builder.base.base import PyInstallerBuilder
from winipedia_utils.utils.modules.module import make_obj_importpath, to_path
from winipedia_utils.utils.resources import svgs

import video_vault
from video_vault.app.db import migrations


class VideoVaultBuilder(PyInstallerBuilder):
    """Build class for video_vault."""

    @classmethod
    def get_add_datas(cls) -> list[tuple[Path, Path]]:
        """Get the artifacts."""
        # Resolve important paths
        project_root = Path(video_vault.__file__).parent.parent

        winipedia_utils_path = Path(winipedia_utils.__file__).parent.parent

        migrations_path_relative = to_path(
            make_obj_importpath(migrations), is_package=True
        )
        migrations_path = project_root / migrations_path_relative

        svgs_path_relative = to_path(make_obj_importpath(svgs), is_package=True)
        svgs_path = winipedia_utils_path / svgs_path_relative

        return [
            (migrations_path, migrations_path_relative),
            (svgs_path, svgs_path_relative),
        ]
