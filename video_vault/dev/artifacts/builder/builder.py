"""Build script.

All subclasses of Builder in the builds package are automatically called.
"""

from pathlib import Path

import winiutils
from pyrig.dev.artifacts.builder.base.base import PyInstallerBuilder
from pyrig.src.modules.module import make_obj_importpath, to_path
from winiutils.src.resources import svgs

from video_vault.src.db import migrations


class VideoVaultBuilder(PyInstallerBuilder):
    """Build class for video_vault."""

    @classmethod
    def get_add_datas(cls) -> list[tuple[Path, Path]]:
        """Get the artifacts."""
        # Resolve important paths
        project_root = cls.get_root_path()

        winiutils_path = Path(winiutils.__file__).parent.parent

        migrations_path_relative = to_path(
            make_obj_importpath(migrations), is_package=True
        )
        migrations_path = project_root / migrations_path_relative

        svgs_path_relative = to_path(make_obj_importpath(svgs), is_package=True)
        svgs_path = winiutils_path / svgs_path_relative

        return [
            (migrations_path, migrations_path_relative),
            (svgs_path, svgs_path_relative),
        ]
