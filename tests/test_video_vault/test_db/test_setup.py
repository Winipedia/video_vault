"""module."""

import tempfile
from pathlib import Path

from pytest_mock import MockerFixture
from winipedia_utils.testing.assertions import assert_with_msg

from video_vault.db.setup import setup_django


def test_setup_django(mocker: MockerFixture) -> None:
    """Test func for setup_django."""
    # Mock external dependencies
    mock_user_data_dir = mocker.patch("video_vault.db.setup.user_data_dir")
    mock_get_app_key = mocker.patch("video_vault.db.setup.get_app_key_as_str")
    mock_django_setup = mocker.patch("video_vault.db.setup.django.setup")
    mock_call_command = mocker.patch("video_vault.db.setup.call_command")

    # Mock settings to avoid "already configured" error
    mock_settings = mocker.patch("video_vault.db.setup.settings")
    mock_settings.configured = False  # Pretend settings aren't configured yet

    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        mock_user_data_dir.return_value = temp_path
        mock_get_app_key.return_value = "test_secret_key"

        # Run the function
        setup_django()

        # Verify user_data_dir was called correctly
        mock_user_data_dir.assert_called_once_with(
            "VideoVault", "Winipedia", ensure_exists=True
        )

        # Verify directories were created
        media_root = temp_path / "media"
        db_dir = temp_path / "db"
        assert_with_msg(media_root.exists(), "Media root directory should be created")
        assert_with_msg(db_dir.exists(), "Database directory should be created")

        # Verify Django settings were configured
        mock_settings.configure.assert_called_once()
        call_args = mock_settings.configure.call_args[1]

        # Check database configuration
        assert_with_msg("DATABASES" in call_args, "DATABASES should be configured")
        db_config = call_args["DATABASES"]["default"]
        assert_with_msg(
            db_config["ENGINE"] == "django.db.backends.sqlite3",
            "Should use SQLite engine",
        )
        assert_with_msg(
            str(temp_path / "db" / "db.sqlite3") in db_config["NAME"],
            "Database path should be correct",
        )

        # Check installed apps
        assert_with_msg(
            "INSTALLED_APPS" in call_args, "INSTALLED_APPS should be configured"
        )
        installed_apps = call_args["INSTALLED_APPS"]
        expected_apps = [
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "video_vault.db",
        ]
        for app in expected_apps:
            assert_with_msg(
                app in installed_apps, f"App {app} should be in INSTALLED_APPS"
            )

        # Check media configuration
        assert_with_msg(
            call_args["MEDIA_ROOT"] == media_root, "MEDIA_ROOT should be set correctly"
        )
        assert_with_msg(
            call_args["MEDIA_URL"] == "/media/", "MEDIA_URL should be set correctly"
        )

        # Check secret key
        assert_with_msg(
            call_args["SECRET_KEY"] == "test_secret_key",  # noqa: S105
            "SECRET_KEY should be set correctly",
        )

        # Verify Django setup was called
        mock_django_setup.assert_called_once()

        # Verify migration was called (since db doesn't exist)
        mock_call_command.assert_called_once_with("migrate")
