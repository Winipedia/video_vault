"""module."""

import pytest
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pytest_mock import MockerFixture
from winipedia_utils.testing.assertions import assert_with_msg

from video_vault.core.consts import APP_NAME, AUTHOR
from video_vault.core.security import get_app_key_as_str, get_or_create_app_aes_gcm


def test_get_or_create_app_aes_gcm(mocker: MockerFixture) -> None:
    """Test func for get_or_create_app_aes_gcm."""
    # Mock the winipedia_utils function
    mock_get_or_create_aes_gcm = mocker.patch(
        "video_vault.core.security.get_or_create_aes_gcm"
    )
    mock_aes_gcm = mocker.Mock(spec=AESGCM)
    mock_get_or_create_aes_gcm.return_value = mock_aes_gcm

    # Test the function
    result = get_or_create_app_aes_gcm()

    # Verify it calls the utility function with correct parameters
    mock_get_or_create_aes_gcm.assert_called_once_with(APP_NAME, AUTHOR)

    # Verify it returns the AESGCM instance
    assert_with_msg(result is mock_aes_gcm, "Should return the AESGCM instance")


def test_get_app_key_as_str(mocker: MockerFixture) -> None:
    """Test func for get_app_key_as_str."""
    # Mock dependencies
    mock_get_or_create_app_aes_gcm = mocker.patch(
        "video_vault.core.security.get_or_create_app_aes_gcm"
    )
    mock_keyring_get_password = mocker.patch(
        "video_vault.core.security.keyring.get_password"
    )

    # Test successful case
    expected_key = "test_key_string"
    mock_keyring_get_password.return_value = expected_key

    result = get_app_key_as_str()

    # Verify it calls get_or_create_app_aes_gcm first
    mock_get_or_create_app_aes_gcm.assert_called_once()

    # Verify it calls keyring.get_password with correct parameters
    mock_keyring_get_password.assert_called_once_with(APP_NAME, AUTHOR)

    # Verify it returns the key
    assert_with_msg(result == expected_key, f"Should return key={expected_key}")

    # Test error case when key is None
    mock_keyring_get_password.return_value = None
    mock_get_or_create_app_aes_gcm.reset_mock()

    with pytest.raises(ValueError, match="Key not found"):
        get_app_key_as_str()

    # Verify it still called the functions
    mock_get_or_create_app_aes_gcm.assert_called_once()
    expected_call_count = 2
    assert_with_msg(
        mock_keyring_get_password.call_count == expected_call_count,
        f"Should call keyring.get_password {expected_call_count} times",
    )
