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


class FindingService:
    """
    Convert extracted medical results into neutral findings.
    """

    def generate_findings(
        self,
        results: list[ExtractedTestResult],
    ) -> list[MedicalFinding]:

        findings: list[MedicalFinding] = []

        for result in results:
            status = classify_result(
                value=result.value,
                reference_range=result.reference_range,
            )

            # Normal results remain available to the system but are not
            # treated as notable findings.
            if status.value == "normal":
                continue

            title = build_finding_title(
                test_name=result.test_name,
                status=status,
            )

            description = build_finding_description(
                test_name=result.test_name,
                status=status,
                value=result.value,
                unit=result.unit,
                minimum=result.reference_range.minimum,
                maximum=result.reference_range.maximum,
            )

            severity = self._determine_severity(status)

            findings.append(
                MedicalFinding(
                    test_name=result.test_name,
                    status=status,
                    value=result.value,
                    unit=result.unit,
                    reference_minimum=result.reference_range.minimum,
                    reference_maximum=result.reference_range.maximum,
                    title=title,
                    description=description,
                    severity=severity,
                    source_page=result.source.page,
                    needs_verification=result.needs_verification,
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