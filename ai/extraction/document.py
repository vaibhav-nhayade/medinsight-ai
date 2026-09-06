from dataclasses import dataclass
from typing import Optional


@dataclass
class DocumentPage:
    """Represents one page of a medical document."""

    page_number: int
    text: str = ""
    image_path: Optional[str] = None


@dataclass
class ProcessedDocument:
    """Normalized representation of a processed medical document."""

    document_id: str
    filename: str
    file_type: str
    pages: list[DocumentPage]
    extraction_method: str
    confidence: float = 1.0