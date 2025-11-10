"""Models for the database."""

from pathlib import Path
from typing import Any

from django.core.files.base import ContentFile
from django.db import models
from winipedia_django.utils.db.models import BaseModel
from winipedia_pyside.utils.core.py_qiodevice import EncryptedPyQFile

from video_vault.core.security import get_or_create_app_aes_gcm


class File(BaseModel):
    """File model."""

    UPLOAD_TO = "downloads"

    file = models.FileField(upload_to=UPLOAD_TO)
    last_position: models.BigIntegerField[int, int] = models.BigIntegerField(default=0)

    def delete_file(self, *args: Any, **kwargs: Any) -> tuple[int, dict[str, int]]:
        """Delete a file."""
        # delete the file from the filesystem
        self.file.delete(save=False)
        # delete the file from the database
        return self.delete(*args, **kwargs)

    @classmethod
    def create_encrypted(cls, path: Path, **kwargs: Any) -> "File":
        """Create a file."""
        aes_gcm = get_or_create_app_aes_gcm()

        decrypted_data = path.read_bytes()

        encrypted_data = EncryptedPyQFile.encrypt_data_static(decrypted_data, aes_gcm)

        return cls.objects.create(file=ContentFile(encrypted_data, path.name), **kwargs)

    @property
    def display_name(self) -> str:
        """Get the display name."""
        return Path(self.file.name).with_suffix("").name
