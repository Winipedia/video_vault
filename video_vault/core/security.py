"""Security module.

This module contains functions to encrypt and decrypt data.
"""

import keyring
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from winipedia_utils.security.keyring import get_or_create_aes_gcm

from video_vault.core.consts import APP_NAME, AUTHOR


def get_or_create_app_aes_gcm() -> AESGCM:
    """Get the app secret using keyring.

    If it does not exist, create it with a AESGCM.
    """
    return get_or_create_aes_gcm(APP_NAME, AUTHOR)


def get_app_key_as_str() -> str:
    """Get the key as a string."""
    get_or_create_app_aes_gcm()
    key = keyring.get_password(APP_NAME, AUTHOR)
    if key is None:
        msg = "Key not found"
        raise ValueError(msg)
    return key
