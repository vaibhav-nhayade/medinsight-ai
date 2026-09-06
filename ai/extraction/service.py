"""
High-level medical parameter extraction service.
"""

from pathlib import Path

from .parameter_extractor import MedicalParameterExtractor
from .pipeline import DocumentProcessingPipeline
from .schema import ExtractedTestResult
from .validator import validate_extracted_result


class MedicalExtractionService:
    """
    Coordinates document processing and medical parameter extraction.
    """

    def __init__(self) -> None:
        self.document_pipeline = DocumentProcessingPipeline()
        self.parameter_extractor = MedicalParameterExtractor()

    def extract_from_document(
        self,
        file_path: str | Path,
        document_id: str,
    ) -> list[ExtractedTestResult]:

        document = self.document_pipeline.process(
            file_path=file_path,
            document_id=document_id,
        )

        results: list[ExtractedTestResult] = []

        for page in document.pages:
            page_results = self.parameter_extractor.extract(
                text=page.text,
                page_number=page.page_number,
            )

            for result in page_results:
                results.append(
                    validate_extracted_result(result)
                )

        return results