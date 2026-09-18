"""
Secure local file storage service.
"""

from pathlib import Path
from uuid import uuid4

from backend.config import (
    ALLOWED_FILE_TYPES,
    MAX_UPLOAD_SIZE,
    UPLOAD_DIR,
)


class FileStorageService:
    """Handle validation and storage of uploaded documents."""

    def __init__(self) -> None:
        UPLOAD_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

    def validate_file(
        self,
        filename: str,
        file_size: int,
    ) -> str:
        """Validate filename and size."""

        extension = Path(filename).suffix.lower()

        if extension not in ALLOWED_FILE_TYPES:
            raise ValueError(
                f"Unsupported file type: {extension or 'unknown'}"
            )

        if file_size <= 0:
            raise ValueError(
                "Uploaded file is empty."
            )

        if file_size > MAX_UPLOAD_SIZE:
            raise ValueError(
                "Uploaded file exceeds the 10 MB size limit."
            )

        return extension

    def generate_file_path(
        self,
        extension: str,
    ) -> Path:
        """Generate a unique storage path."""

        filename = f"{uuid4().hex}{extension}"

        return UPLOAD_DIR / filename

    def save_file(
        self,
        content: bytes,
        extension: str,
    ) -> Path:
        """Persist validated file content."""

        file_path = self.generate_file_path(
            extension
        )

        file_path.write_bytes(content)

        return file_path