"""Build script for video_vault."""

import tempfile
from pathlib import Path

from PyInstaller.__main__ import run

from video_vault import build_project


def do_build() -> None:
    """Build the app."""
    # Create temporary directory for build files
    with tempfile.TemporaryDirectory() as temp_build_dir:
        spec_file = Path(build_project.__file__).parent / "build.spec"

        options = [
            # Path to spec file
            str(spec_file),
            # Clean build files beforehand
            "--clean",
            # Set work and dist path to temp dir
            "--workpath",
            temp_build_dir,
            # Set dist path to current dir
            "--distpath",
            ".",
        ]
        run(options)


if __name__ == "__main__":
    do_build()
