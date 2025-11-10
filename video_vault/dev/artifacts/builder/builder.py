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
from winipedia_utils.utils.modules.module import make_obj_importpath, to_path
from winipedia_utils.utils.resources import svgs

import video_vault
from video_vault.app import main
from video_vault.app.core.consts import APP_NAME
from video_vault.app.db import migrations
from video_vault.dev import artifacts


class VideoVaultBuilder(Builder):
    """Build class for video_vault."""

    @classmethod
    def create_artifacts(cls) -> None:
        """Get the artifacts."""
        # Resolve important paths
        project_root = Path(video_vault.__file__).parent.parent

        winipedia_utils_path = Path(winipedia_utils.__file__).parent
        main_script = project_root / to_path(make_obj_importpath(main), is_package=True)

        app_icon_path = project_root / (
            to_path(make_obj_importpath(artifacts), is_package=True) / "app_icon.ico"
        )

        migrations_path_relative = to_path(
            make_obj_importpath(migrations), is_package=True
        )
        migrations_path = project_root / migrations_path_relative

        svgs_path_relative = to_path(make_obj_importpath(svgs), is_package=True)
        svgs_path = winipedia_utils_path / svgs_path_relative

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
                str(app_icon_path),
                # --- Add data folders ---
                "--add-data",
                f"{migrations_path}{os.pathsep}{migrations_path_relative}",
                "--add-data",
                f"{svgs_path}{os.pathsep}{svgs_path_relative}",
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
