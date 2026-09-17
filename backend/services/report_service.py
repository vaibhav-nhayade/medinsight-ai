"""
Application service for medical report processing.
"""

from pathlib import Path

from ai.analysis.classification import classify_result
from ai.analysis.finding_service import FindingService
from ai.analysis.summary import build_analysis_summary
from ai.extraction.report_parser import MedicalReportParser

from backend.schemas.report import (
    AnalysisResponse,
    AnalysisSummaryResponse,
    FindingResponse,
    ReportResultResponse,
)


class ReportService:
    """Coordinate medical report parsing and analysis."""

    def __init__(self) -> None:
        self.parser = MedicalReportParser()
        self.finding_service = FindingService()

    def analyze_report(
        self,
        file_path: str | Path,
        document_id: str,
    ) -> AnalysisResponse:

        document, results = self.parser.parse(
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

        result_responses = []

        for result in results:
            status = classify_result(
                value=result.value,
                reference_range=result.reference_range,
            )

            result_responses.append(
                ReportResultResponse(
                    test_name=result.test_name,
                    value=result.value,
                    unit=result.unit,
                    reference_minimum=(
                        result.reference_range.minimum
                    ),
                    reference_maximum=(
                        result.reference_range.maximum
                    ),
                    status=status.value,
                    confidence=result.confidence,
                    needs_verification=result.needs_verification,
                    source_page=result.source.page,
                )
            )

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
            for finding in findings
        ]

        return AnalysisResponse(
            document_id=document.document_id,
            filename=document.filename,
            results=result_responses,
            findings=finding_responses,
            summary=AnalysisSummaryResponse(
                total_results=summary.total_results,
                normal_results=summary.normal_results,
                low_results=summary.low_results,
                high_results=summary.high_results,
                unknown_results=summary.unknown_results,
                findings_count=summary.findings_count,
                verification_required=(
                    summary.verification_required
                ),
            ),
        )