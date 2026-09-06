from pathlib import Path


class OCRProcessor:
    """Interface for OCR processing.

    A concrete OCR provider will be implemented later.
    """

    def extract_text(self, file_path: str | Path) -> str:
        """Extract text from an image-based document."""
        raise NotImplementedError(
            "OCR provider has not been configured yet."
        )