"""
High-level summary of deterministic report analysis.
"""

from dataclasses import dataclass

from .finding import MedicalFinding
from .result import AnalyzedTestResult


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
    results: list[AnalyzedTestResult],
    findings: list[MedicalFinding],
) -> AnalysisSummary:
    """
    Build summary statistics from already-analyzed results.

    Classification is intentionally not repeated here.
    ResultAnalysisService is the single source of truth for status.
    """
    normal = 0
    low = 0
    high = 0
    unknown = 0
    verification_required = 0

    for result in results:
        if result.status.value == "normal":
            normal += 1
        elif result.status.value == "low":
            low += 1
        elif result.status.value == "high":
            high += 1
        elif result.status.value == "unknown":
            unknown += 1

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