"""Security module.

This module contains functions to encrypt and decrypt data.
"""

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from winipedia_utils.utils.security.keyring import get_key_as_str, get_or_create_aes_gcm

from video_vault.app.core.consts import APP_NAME, AUTHOR


def get_or_create_app_aes_gcm() -> AESGCM:
    """Get the app secret using keyring.

    If it does not exist, create it with a AESGCM.
    """
    return get_or_create_aes_gcm(APP_NAME, AUTHOR)[0]


def get_app_key_as_str() -> str:
    """Get the key as a string."""
    get_or_create_aes_gcm(APP_NAME, AUTHOR)
    key = get_key_as_str(APP_NAME, AUTHOR, key_class=AESGCM)
    if key is None:
        msg = "Key not found"
        raise ValueError(msg)
    return key
