"""module."""

import tempfile
from pathlib import Path

from pytest_mock import MockerFixture
from winipedia_utils.testing.assertions import assert_with_msg

from video_vault.externals.ffmpegs.ffmpeg import get_ffmpeg_path


def test_get_ffmpeg_path(mocker: MockerFixture) -> None:
    """Test func for get_ffmpeg_path."""
    # Test successful case - Windows
    mock_platform_system = mocker.patch(
        "video_vault.externals.ffmpegs.ffmpeg.platform.system"
    )
    mock_platform_system.return_value = "Windows"

    # Create a temporary directory structure
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Mock the ffmpegs package path
        mock_ffmpegs_package = mocker.patch(
            "video_vault.externals.ffmpegs.ffmpeg.ffmpegs"
        )
        mock_ffmpegs_package.__file__ = str(temp_path / "ffmpegs_package.py")

        # Create the expected directory structure
        windows_dir = temp_path / "windows"
        windows_dir.mkdir(parents=True)

        # Create the ffmpeg.exe binary
        ffmpeg_binary = windows_dir / "bin" / "ffmpeg.exe"
        ffmpeg_binary.parent.mkdir(parents=True)
        ffmpeg_binary.write_text("fake ffmpeg binary")

        # Test the function
        result = get_ffmpeg_path()

        # Verify the result
        assert_with_msg(result is not None, "Should find ffmpeg binary")
        if result is not None:  # Type narrowing for mypy
            assert_with_msg(
                result == ffmpeg_binary, "Should return correct path to ffmpeg.exe"
            )
            assert_with_msg(result.exists(), "Returned path should exist")
            assert_with_msg(result.is_file(), "Returned path should be a file")


def test_get_ffmpeg_path_linux(mocker: MockerFixture) -> None:
    """Test func for get_ffmpeg_path on Linux."""
    # Test successful case - Linux
    mock_platform_system = mocker.patch(
        "video_vault.externals.ffmpegs.ffmpeg.platform.system"
    )
    mock_platform_system.return_value = "Linux"

    # Create a temporary directory structure
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Mock the ffmpegs package path
        mock_ffmpegs_package = mocker.patch(
            "video_vault.externals.ffmpegs.ffmpeg.ffmpegs"
        )
        mock_ffmpegs_package.__file__ = str(temp_path / "ffmpegs_package.py")

        # Create the expected directory structure
        linux_dir = temp_path / "linux"
        linux_dir.mkdir(parents=True)

        # Create the ffmpeg binary (no .exe extension on Linux)
        ffmpeg_binary = linux_dir / "bin" / "ffmpeg"
        ffmpeg_binary.parent.mkdir(parents=True)
        ffmpeg_binary.write_text("fake ffmpeg binary")

        # Test the function
        result = get_ffmpeg_path()

        # Verify the result
        assert_with_msg(result is not None, "Should find ffmpeg binary")
        if result is not None:  # Type narrowing for mypy
            assert_with_msg(
                result == ffmpeg_binary, "Should return correct path to ffmpeg"
            )
            assert_with_msg(result.exists(), "Returned path should exist")
            assert_with_msg(result.is_file(), "Returned path should be a file")


def test_get_ffmpeg_path_folder_not_exists(mocker: MockerFixture) -> None:
    """Test func for get_ffmpeg_path when OS folder doesn't exist."""
    mock_platform_system = mocker.patch(
        "video_vault.externals.ffmpegs.ffmpeg.platform.system"
    )
    mock_platform_system.return_value = "Windows"

    # Create a temporary directory structure without the windows folder
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Mock the ffmpegs package path
        mock_ffmpegs_package = mocker.patch(
            "video_vault.externals.ffmpegs.ffmpeg.ffmpegs"
        )
        mock_ffmpegs_package.__file__ = str(temp_path / "ffmpegs_package.py")

        # Don't create the windows directory

        # Test the function
        result = get_ffmpeg_path()

        # Verify the result
        assert_with_msg(
            result is None, "Should return None when OS folder doesn't exist"
        )


def test_get_ffmpeg_path_binary_not_found(mocker: MockerFixture) -> None:
    """Test func for get_ffmpeg_path when binary is not found."""
    mock_platform_system = mocker.patch(
        "video_vault.externals.ffmpegs.ffmpeg.platform.system"
    )
    mock_platform_system.return_value = "Windows"

    # Create a temporary directory structure
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Mock the ffmpegs package path
        mock_ffmpegs_package = mocker.patch(
            "video_vault.externals.ffmpegs.ffmpeg.ffmpegs"
        )
        mock_ffmpegs_package.__file__ = str(temp_path / "ffmpegs_package.py")

        # Create the expected directory structure but no binary
        windows_dir = temp_path / "windows"
        windows_dir.mkdir(parents=True)

        # Create some other files but not ffmpeg.exe
        (windows_dir / "other_file.txt").write_text("not ffmpeg")

        # Test the function
        result = get_ffmpeg_path()

        # Verify the result
        assert_with_msg(result is None, "Should return None when binary is not found")
