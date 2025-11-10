"""Build script.

All subclasses of Builder in the builds package are automatically called.
"""

import os
import platform
import shutil
import tempfile
from pathlib import Path

import winipedia_utils
from PyInstaller.__main__ import run
from winipedia_utils.dev.artifacts.builder.base.base import Builder

import video_vault
from video_vault.core.consts import APP_NAME


class VideoVaultBuilder(Builder):
    """Build class for video_vault."""

    @classmethod
    def create_artifacts(cls) -> None:
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
                "--specpath",
                temp_build_dir,
                "--distpath",
                str(cls.ARTIFACTS_PATH),
                "--icon",
                str(
                    project_root / "video_vault" / "dev" / "artifacts" / "app_icon.ico"
                ),
                # --- Add data folders ---
                "--add-data",
                f"{project_root / 'video_vault' / 'db' / 'migrations'}{os.pathsep}video_vault/db/migrations",  # noqa: E501
                "--add-data",
                f"{winipedia_utils_path / 'utils' / 'resources' / 'svgs'}{os.pathsep}winipedia_utils/utils/resources/svgs",  # noqa: E501
            ]

            run(options)

        # Return built binary path
        binary_path = cls.ARTIFACTS_PATH / APP_NAME
        if platform.system() == "Windows":
            binary_path = binary_path.with_suffix(".exe")
        elif platform.system() == "Darwin":
            # On macOS, PyInstaller creates a .app bundle (directory)
            # We need to zip it for GitHub Releases
            app_bundle = cls.ARTIFACTS_PATH / f"{APP_NAME}.app"
            if app_bundle.exists():
                zip_path = cls.ARTIFACTS_PATH / f"{APP_NAME}.zip"
                shutil.make_archive(
                    str(zip_path.with_suffix("")),
                    "zip",
                    cls.ARTIFACTS_PATH,
                    f"{APP_NAME}.app",
                )


if __name__ == "__main__":
    VideoVaultBuilder()
