"""
High-level orchestration of the MedInsight analysis pipeline.
"""

from pathlib import Path
from dataclasses import dataclass

from ai.analysis.finding import MedicalFinding
from ai.analysis.finding_service import FindingService
from ai.analysis.summary import AnalysisSummary, build_analysis_summary
from ai.extraction.report_parser import MedicalReportParser
from ai.extraction.schema import ExtractedTestResult


@dataclass
class ReportAnalysis:
    """Complete deterministic analysis of a medical report."""

    document_id: str
    filename: str
    results: list[ExtractedTestResult]
    findings: list[MedicalFinding]
    summary: AnalysisSummary


class AnalysisOrchestrator:
    """
    Coordinates document parsing, result analysis, finding generation,
    and summary creation.
    """

    def __init__(self) -> None:
        self.report_parser = MedicalReportParser()
        self.finding_service = FindingService()

    def analyze(
        self,
        file_path: str | Path,
        document_id: str,
    ) -> ReportAnalysis:

        document, results = self.report_parser.parse(
            file_path=file_path,
            document_id=document_id,
        )

        findings = self.finding_service.generate_findings(
            results
        )

        summary = build_analysis_summary(
            results=results,
            findings=findings,
        )

        return ReportAnalysis(
            document_id=document.document_id,
            filename=document.filename,
            results=results,
            findings=findings,
            summary=summary,
        )