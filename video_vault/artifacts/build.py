"""Build script for video_vault without spec file."""

import os
import platform
import tempfile
from pathlib import Path

import winipedia_utils
from PyInstaller.__main__ import run
from winipedia_utils.artifacts.build import Build

import video_vault
from video_vault.core.consts import APP_NAME


class VideoVaultBuild(Build):
    """Build class for video_vault."""

    @classmethod
    def get_artifacts(cls) -> list[Path]:
        """Get the artifacts."""
        # Resolve important paths
        project_root = Path(video_vault.__file__).parent.parent

        winipedia_utils_path = Path(winipedia_utils.__file__).parent
        main_script = project_root / "video_vault" / "main.py"

        # --- Temporary build dir ---
        with tempfile.TemporaryDirectory() as temp_build_dir:
            options = [
                str(main_script),
                "--name",
                APP_NAME,
                "--clean",
                "--noconfirm",
                "--onefile",
                "--noconsole",
                "--workpath",
                temp_build_dir,
                "--distpath",
                str(cls.ARTIFACTS_PATH),
                "--icon",
                str(project_root / "video_vault" / "artifacts" / "app_icon.ico"),
                # --- Add data folders ---
                "--add-data",
                f"{project_root / 'video_vault' / 'db' / 'migrations'}{os.pathsep}video_vault/db/migrations",  # noqa: E501
                "--add-data",
                f"{winipedia_utils_path / 'resources' / 'svgs'}{os.pathsep}winipedia_utils/resources/svgs",  # noqa: E501
            ]

            run(options)

        # Return built binary path
        binary_path = cls.ARTIFACTS_PATH / APP_NAME
        if platform.system() == "Windows":
            binary_path = binary_path.with_suffix(".exe")

        return [binary_path]


if __name__ == "__main__":
    VideoVaultBuild()
