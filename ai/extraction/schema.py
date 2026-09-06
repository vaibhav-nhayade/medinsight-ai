from dataclasses import dataclass
from typing import Optional


@dataclass
class ReferenceRange:
    """Reference range provided by the medical report."""

    minimum: Optional[float] = None
    maximum: Optional[float] = None


@dataclass
class SourceLocation:
    """Location of extracted information in the source document."""

    page: Optional[int] = None
    text: Optional[str] = None


@dataclass
class ExtractedTestResult:
    """Structured representation of an extracted medical test result."""

    test_name: str
    value: Optional[float]
    unit: Optional[str]
    reference_range: ReferenceRange
    confidence: float
    source: SourceLocation
    needs_verification: bool = False