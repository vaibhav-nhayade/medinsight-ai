"""
Structured representation of an analyzed medical test result.
"""

from dataclasses import dataclass
from typing import Optional

from ai.analysis.classification import ResultStatus
from ai.extraction.schema import ExtractedTestResult


@dataclass
class AnalyzedTestResult:
    """Medical test result after deterministic range analysis."""

    test_name: str
    value: Optional[float]
    unit: Optional[str]
    reference_minimum: Optional[float]
    reference_maximum: Optional[float]
    status: ResultStatus
    confidence: float
    needs_verification: bool
    source_page: Optional[int]
    source_text: Optional[str]


def build_analyzed_result(
    result: ExtractedTestResult,
    status: ResultStatus,
) -> AnalyzedTestResult:
    """Convert an extracted result into an analyzed result."""

    return AnalyzedTestResult(
        test_name=result.test_name,
        value=result.value,
        unit=result.unit,
        reference_minimum=result.reference_range.minimum,
        reference_maximum=result.reference_range.maximum,
        status=status,
        confidence=result.confidence,
        needs_verification=result.needs_verification,
        source_page=result.source.page,
        source_text=result.source.text,
    )