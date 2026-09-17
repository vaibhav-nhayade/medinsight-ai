"""
Backend application configuration.
"""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

UPLOAD_DIR = PROJECT_ROOT / "data" / "uploads"

ALLOWED_FILE_TYPES = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
}

MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB


def ensure_storage_directories() -> None:
    """Create required local storage directories."""

    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )