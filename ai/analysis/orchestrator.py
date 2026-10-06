"""
High-level orchestration of the MedInsight analysis pipeline.
"""

from dataclasses import dataclass
from pathlib import Path

from ai.analysis.finding import MedicalFinding
from ai.analysis.finding_service import FindingService
from ai.analysis.result import AnalyzedTestResult
from ai.analysis.service import ResultAnalysisService
from ai.analysis.summary import AnalysisSummary, build_analysis_summary
from ai.extraction.report_parser import MedicalReportParser


@dataclass
class ReportAnalysis:
    """Complete deterministic analysis of a medical report."""

    document_id: str
    filename: str
    results: list[AnalyzedTestResult]
    findings: list[MedicalFinding]
    summary: AnalysisSummary


class AnalysisOrchestrator:
    """
    Coordinates document parsing, result analysis, finding generation,
    and summary creation.
    """

    def __init__(self) -> None:
        self.report_parser = MedicalReportParser()
        self.result_analysis_service = ResultAnalysisService()
        self.finding_service = FindingService()

    def analyze(
        self,
        file_path: str | Path,
        document_id: str,
    ) -> ReportAnalysis:

        document, extracted_results = self.report_parser.parse(
            file_path=file_path,
            document_id=document_id,
        )

        analyzed_results = self.result_analysis_service.analyze(
            extracted_results
        )

        findings = self.finding_service.generate_findings(
            analyzed_results
        )

        summary = build_analysis_summary(
            results=analyzed_results,
            findings=findings,
        )

        return ReportAnalysis(
            document_id=document.document_id,
            filename=document.filename,
            results=analyzed_results,
            findings=findings,
            summary=summary,
        )