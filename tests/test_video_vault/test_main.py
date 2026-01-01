"""test module."""

import os
import platform
import shutil
from contextlib import chdir
from pathlib import Path

import pytest
from pyrig.src.processes import run_subprocess

import video_vault


def test_main(main_test_fixture: None) -> None:
    """Test func for main."""
    assert main_test_fixture is None


@pytest.mark.skipif(
    platform.system() == "Windows",
    reason="Test fails on Windows due to windows paths in gitub ci",
)
def test_run(tmp_path: Path) -> None:
    """Test func for main."""
    # copy the video_vault folder to a temp directory
    # run main.py from that directory

    video_vault_path = Path(video_vault.__path__[0])

    temp_video_vault_path = tmp_path / video_vault.__name__

    # shutil video_vault_path to tmp_path
    shutil.copytree(video_vault_path, temp_video_vault_path)

    files = [
        "pyproject.toml",
        "uv.lock",
        "README.md",
        "LICENSE",
    ]

    for file in files:
        shutil.copy(file, temp_video_vault_path.parent)

    env = os.environ.copy()
    with chdir(tmp_path):
        # install deps
        run_subprocess(["uv", "sync", "--no-dev"])

        # delete pyproject.toml and uv.lock and readme.md
        for file in files:
            Path(file).unlink()
        # python -m video_vault.main

        run_subprocess(["uv", "run", "-m", "video_vault.main"], env=env)
