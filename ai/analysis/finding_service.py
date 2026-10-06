"""
Service for generating structured medical findings.
"""

from ai.extraction.schema import ExtractedTestResult

from .classification import classify_result
from .finding import MedicalFinding
from .finding_rules import (
    build_finding_description,
    build_finding_title,
)
from .result import AnalyzedTestResult


class FindingService:
    """
    Convert analyzed medical results into neutral findings.

    The service accepts both ExtractedTestResult and AnalyzedTestResult
    so existing extraction-level callers remain compatible while the
    analysis orchestrator can use the already-computed classification.
    """

    def generate_findings(
        self,
        results: list[ExtractedTestResult | AnalyzedTestResult],
    ) -> list[MedicalFinding]:
        findings: list[MedicalFinding] = []

        for result in results:
            if isinstance(result, AnalyzedTestResult):
                status = result.status
                test_name = result.test_name
                value = result.value
                unit = result.unit
                minimum = result.reference_minimum
                maximum = result.reference_maximum
                source_page = result.source_page
                needs_verification = result.needs_verification
            else:
                status = classify_result(
                    value=result.value,
                    reference_range=result.reference_range,
                )
                test_name = result.test_name
                value = result.value
                unit = result.unit
                minimum = result.reference_range.minimum
                maximum = result.reference_range.maximum
                source_page = result.source.page
                needs_verification = result.needs_verification

            # Normal results remain available to the system but are not
            # treated as notable findings.
            if status.value == "normal":
                continue

            title = build_finding_title(
                test_name=test_name,
                status=status,
            )

            description = build_finding_description(
                test_name=test_name,
                status=status,
                value=value,
                unit=unit,
                minimum=minimum,
                maximum=maximum,
            )

            severity = self._determine_severity(status)

            findings.append(
                MedicalFinding(
                    test_name=test_name,
                    status=status,
                    value=value,
                    unit=unit,
                    reference_minimum=minimum,
                    reference_maximum=maximum,
                    title=title,
                    description=description,
                    severity=severity,
                    source_page=source_page,
                    needs_verification=needs_verification,
                )
            )

        return findings

    @staticmethod
    def _determine_severity(status) -> str:
        """
        Assign an application-level severity.

        This is NOT clinical severity.
        """
        if status.value in {"high", "low"}:
            return "attention"

        if status.value == "unknown":
            return "verification"

        return "none"