"""module."""

from pathlib import Path

from winipedia_utils.testing.assertions import assert_with_msg

from video_vault.externals.ffmpeg import get_ffmpeg_path


def test_get_ffmpeg_path() -> None:
    """Test func for get_ffmpeg_path."""
    path = get_ffmpeg_path()
    assert_with_msg(isinstance(path, Path), "Should find ffmpeg binary")
