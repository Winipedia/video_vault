"""module to interact with ffmpeg."""

from pathlib import Path

import imageio_ffmpeg  # type: ignore[import-untyped]
from winipedia_utils.logging.logger import get_logger

logger = get_logger(__name__)


def get_ffmpeg_path() -> Path | None:
    """Get the path to ffmpeg."""
    path = Path(imageio_ffmpeg.get_ffmpeg_exe())
    logger.info("Found ffmpeg at %s", path)
    return path
