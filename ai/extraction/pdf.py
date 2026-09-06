from pathlib import Path

from pypdf import PdfReader


class PDFTextExtractor:
    """Extract text from text-based PDF documents."""

    def extract_text(self, file_path: str | Path) -> list[str]:
        """Return extracted text for each PDF page."""

        reader = PdfReader(str(file_path))

        pages = []

        for page in reader.pages:
            pages.append(page.extract_text() or "")

        return pages