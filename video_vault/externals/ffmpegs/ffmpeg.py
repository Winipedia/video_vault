"""module to interact with ffmpeg."""

import platform
from pathlib import Path

from winipedia_utils.logging.logger import get_logger

from video_vault.externals import ffmpegs

logger = get_logger(__name__)


def get_ffmpeg_path() -> Path | None:
    """Get the path to ffmpeg."""
    current_os = platform.system().lower()

    # lets use importlib.resources to get the path to the ffmpeg folder
    base_path = Path(ffmpegs.__file__).parent

    ffmpeg_folder = base_path / current_os

    # if folder does not exist, raise error
    if not ffmpeg_folder.exists():
        logger.warning("FFmpeg folder does not exist: %s", ffmpeg_folder)
        return None

    binary_name = "ffmpeg.exe" if current_os == "windows" else "ffmpeg"

    # use rglop to find the binary
    for path in ffmpeg_folder.rglob(binary_name):
        if path.is_file():
            return path

    logger.warning("Could not find ffmpeg in %s", ffmpeg_folder)
    return None
