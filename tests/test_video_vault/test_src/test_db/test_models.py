"""module."""

from pathlib import Path

from pyrig.src.testing.assertions import assert_with_msg

from video_vault.src.db.models import File


class TestFile:
    """Test class for File."""

    def test_delete_file(self, tmp_path: Path) -> None:
        """Test method for delete_file."""
        # Create a test file
        test_file = tmp_path / "test_video.mp4"
        test_content = b"fake video content for testing"
        test_file.write_bytes(test_content)

        # Create a File instance
        file_instance = File.create_encrypted(test_file)
        file_path = file_instance.file.path
        file_id = file_instance.pk

        # Verify file exists in filesystem and database
        assert_with_msg(Path(file_path).exists(), "File should exist in filesystem")
        assert_with_msg(
            File.objects.filter(pk=file_id).exists(), "File should exist in database"
        )

        # Delete the file
        result = file_instance.delete_file()

        # Verify file is deleted from both filesystem and database
        assert_with_msg(
            not Path(file_path).exists(), "File should be deleted from filesystem"
        )
        assert_with_msg(
            not File.objects.filter(pk=file_id).exists(),
            "File should be deleted from database",
        )
        assert_with_msg(result[0] == 1, "Should delete exactly one record")

    def test_create_encrypted(self, tmp_path: Path) -> None:
        """Test method for create_encrypted."""
        # Create a test file
        test_file = tmp_path / "test_video.mp4"
        test_content = b"fake video content for testing"
        test_file.write_bytes(test_content)

        # Create encrypted file
        result = File.create_encrypted(test_file)

        # Verify the file was created
        assert_with_msg(result.file.name != "", "File should have a name")
        assert_with_msg(result.file.size > 0, "File should have content")
        assert_with_msg(result.last_position == 0, "Default last_position should be 0")

        # Verify file exists in database
        assert_with_msg(
            File.objects.filter(pk=result.pk).exists(), "File should exist in database"
        )

        # Verify the file is encrypted (content should be different from original)
        encrypted_content = result.file.read()
        assert_with_msg(
            encrypted_content != test_content, "File content should be encrypted"
        )

    def test_display_name(self, tmp_path: Path) -> None:
        """Test method for display_name."""
        # Create a test file with extension
        test_file = tmp_path / "my_test_video.mp4"
        test_content = b"fake video content for testing"
        test_file.write_bytes(test_content)

        # Create File instance
        file_instance = File.create_encrypted(test_file)

        # Test display_name property
        display_name = file_instance.display_name
        assert_with_msg(display_name != "", "Display name should not be empty")
        assert_with_msg(
            ".mp4" not in display_name, "Display name should not contain file extension"
        )
        # The display name should be based on the filename without extension
        assert_with_msg(
            "my_test_video" in display_name,
            "Display name should contain the base filename",
        )
