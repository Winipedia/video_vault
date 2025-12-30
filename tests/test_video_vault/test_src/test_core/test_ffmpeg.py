"""module."""

from pathlib import Path

from video_vault.src.core.ffmpeg import get_ffmpeg_path


def test_get_ffmpeg_path() -> None:
    """Test func for get_ffmpeg_path."""
    path = get_ffmpeg_path()
    assert isinstance(path, Path), "Should find ffmpeg binary"
