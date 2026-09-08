"""
High-level parser for medical reports.
"""

from pathlib import Path

from .document import ProcessedDocument
from .pipeline import DocumentProcessingPipeline
from .result_parser import MedicalResultParser
from .schema import ExtractedTestResult


class MedicalReportParser:
    """Convert a medical document into structured test results."""

    def __init__(self) -> None:
        self.document_pipeline = DocumentProcessingPipeline()
        self.result_parser = MedicalResultParser()

    def parse(
        self,
        file_path: str | Path,
        document_id: str,
    ) -> tuple[ProcessedDocument, list[ExtractedTestResult]]:

        document = self.document_pipeline.process(
            file_path=file_path,
            document_id=document_id,
        )

        results: list[ExtractedTestResult] = []

        for page in document.pages:
            page_results = self.result_parser.parse(
                text=page.text,
                page_number=page.page_number,
            )

            results.extend(page_results)

        return document, results