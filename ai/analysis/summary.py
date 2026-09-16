"""
High-level summary of deterministic report analysis.
"""

from dataclasses import dataclass

from .classification import ResultStatus
from .finding import MedicalFinding
from ai.extraction.schema import ExtractedTestResult


@dataclass
class AnalysisSummary:
    """Aggregate statistics for a processed report."""

    total_results: int
    normal_results: int
    low_results: int
    high_results: int
    unknown_results: int
    findings_count: int
    verification_required: int


def build_analysis_summary(
    results: list[ExtractedTestResult],
    findings: list[MedicalFinding],
) -> AnalysisSummary:

    normal = 0
    low = 0
    high = 0
    unknown = 0
    verification_required = 0

    for result in results:
        status = (
            ResultStatus.NORMAL
            if (
                result.reference_range.minimum is not None
                or result.reference_range.maximum is not None
            )
            and result.value is not None
            and (
                (
                    result.reference_range.minimum is None
                    or result.value >= result.reference_range.minimum
                )
                and (
                    result.reference_range.maximum is None
                    or result.value <= result.reference_range.maximum
                )
            )
            else None
        )

        if status == ResultStatus.NORMAL:
            normal += 1
        else:
            # The definitive classification is performed by the finding
            # service. Unknown is used here when a result cannot be
            # classified from the available report information.
            minimum = result.reference_range.minimum
            maximum = result.reference_range.maximum

            if result.value is None or (
                minimum is None and maximum is None
            ):
                unknown += 1
            elif minimum is not None and result.value < minimum:
                low += 1
            elif maximum is not None and result.value > maximum:
                high += 1

        if result.needs_verification:
            verification_required += 1

    return AnalysisSummary(
        total_results=len(results),
        normal_results=normal,
        low_results=low,
        high_results=high,
        unknown_results=unknown,
        findings_count=len(findings),
        verification_required=verification_required,
    )