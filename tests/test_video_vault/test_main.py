"""module."""

import shutil
from contextlib import chdir
from pathlib import Path

from winipedia_utils.utils.os.os import run_subprocess

import video_vault


def test_main(tmp_path: Path) -> None:
    """Test func for main."""
    # copy the video_vault folder to a temp directory
    # run main.py from that directory

    video_vault_path = Path(video_vault.__file__).parent

    temp_video_vault_path = tmp_path / "video_vault"

    # shutil video_vault_path to tmp_path
    shutil.copytree(video_vault_path, temp_video_vault_path)

    # copy pyproject.toml and poetry.lock to tmp_path
    shutil.copy("pyproject.toml", temp_video_vault_path.parent)
    shutil.copy("poetry.lock", temp_video_vault_path.parent)
    # copy readme.md to tmp_path
    shutil.copy("README.md", temp_video_vault_path.parent)

    with chdir(tmp_path):
        # poetry install
        run_subprocess(["poetry", "install"])
        # gte path to python venv
        python_path = (
            run_subprocess(["poetry", "run", "which", "python"])
            .stdout.decode("utf-8")
            .strip()
        )

        # delete pyproject.toml and poetry.lock and readme.md
        Path("pyproject.toml").unlink()
        Path("poetry.lock").unlink()
        Path("README.md").unlink()
        # python -m video_vault.main
        run_subprocess([python_path, "-m", "video_vault.main"])
