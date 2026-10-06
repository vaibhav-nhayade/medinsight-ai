"""
Application service for medical report processing.
"""

from pathlib import Path

from ai.analysis.orchestrator import AnalysisOrchestrator

from backend.schemas.report import (
    AnalysisResponse,
    AnalysisSummaryResponse,
    FindingResponse,
    ReportResultResponse,
)


class ReportService:
    """Coordinate medical report analysis for the backend API."""

    def __init__(self) -> None:
        self.analysis_orchestrator = AnalysisOrchestrator()

    def analyze_report(
        self,
        file_path: str | Path,
        document_id: str,
    ) -> AnalysisResponse:
        """Analyze a stored medical report and build the API response."""

        analysis = self.analysis_orchestrator.analyze(
            file_path=file_path,
            document_id=document_id,
        )

        result_responses = [
            ReportResultResponse(
                test_name=result.test_name,
                value=result.value,
                unit=result.unit,
                reference_minimum=result.reference_minimum,
                reference_maximum=result.reference_maximum,
                status=result.status.value,
                confidence=result.confidence,
                needs_verification=result.needs_verification,
                source_page=result.source_page,
            )
            for result in analysis.results
        ]

        finding_responses = [
            FindingResponse(
                test_name=finding.test_name,
                status=finding.status.value,
                value=finding.value,
                unit=finding.unit,
                title=finding.title,
                description=finding.description,
                severity=finding.severity,
                source_page=finding.source_page,
                needs_verification=finding.needs_verification,
            )
            for finding in analysis.findings
        ]

        summary = analysis.summary

        return AnalysisResponse(
            document_id=analysis.document_id,
            filename=analysis.filename,
            results=result_responses,
            findings=finding_responses,
            summary=AnalysisSummaryResponse(
                total_results=summary.total_results,
                normal_results=summary.normal_results,
                low_results=summary.low_results,
                high_results=summary.high_results,
                unknown_results=summary.unknown_results,
                findings_count=summary.findings_count,
                verification_required=summary.verification_required,
            ),
        )