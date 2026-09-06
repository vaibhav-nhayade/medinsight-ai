from pathlib import Path

from .document import DocumentPage, ProcessedDocument
from .normalizer import normalize_text
from .pdf import PDFTextExtractor


class DocumentProcessingPipeline:
    """Coordinates document text extraction and normalization."""

    def __init__(self) -> None:
        self.pdf_extractor = PDFTextExtractor()

    def process(
        self,
        file_path: str | Path,
        document_id: str,
    ) -> ProcessedDocument:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Document not found: {path}")

        suffix = path.suffix.lower()

        if suffix == ".pdf":
            raw_pages = self.pdf_extractor.extract_text(path)

            pages = [
                DocumentPage(
                    page_number=index + 1,
                    text=normalize_text(text),
                )
                for index, text in enumerate(raw_pages)
            ]

            return ProcessedDocument(
                document_id=document_id,
                filename=path.name,
                file_type="pdf",
                pages=pages,
                extraction_method="pdf_text",
            )

        raise ValueError(
            f"Unsupported document type: {suffix}"
        )