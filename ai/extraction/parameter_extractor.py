"""
Medical parameter extraction from normalized document text.
"""

from dataclasses import dataclass
from typing import Optional

from .parameter_patterns import TEST_PATTERNS
from .schema import ExtractedTestResult, ReferenceRange, SourceLocation


@dataclass
class ExtractionCandidate:
    """Intermediate extraction result before final validation."""

    test_name: str
    value: float
    unit: Optional[str]
    source_text: str


class MedicalParameterExtractor:
    """Extract structured medical test results from text."""

    def extract(
        self,
        text: str,
        page_number: Optional[int] = None,
    ) -> list[ExtractedTestResult]:
        results: list[ExtractedTestResult] = []

        for test_name, pattern in TEST_PATTERNS.items():
            matches = pattern.finditer(text)

            for match in matches:
                value = float(match.group(1))
                unit = match.group(2)

                source_text = match.group(0).strip()

                results.append(
                    ExtractedTestResult(
                        test_name=test_name,
                        value=value,
                        unit=unit,
                        reference_range=ReferenceRange(),
                        confidence=0.90,
                        source=SourceLocation(
                            page=page_number,
                            text=source_text,
                        ),
                        needs_verification=False,
                    )
                )

        return results