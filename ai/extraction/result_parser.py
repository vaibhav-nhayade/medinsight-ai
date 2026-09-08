"""
Parser for associating test results with nearby reference ranges.
"""

import re

from .parameter_extractor import MedicalParameterExtractor
from .reference_extractor import ReferenceRangeExtractor
from .schema import ExtractedTestResult


class MedicalResultParser:
    """
    Parse medical test values and their associated reference ranges.
    """

    def __init__(self) -> None:
        self.parameter_extractor = MedicalParameterExtractor()
        self.reference_extractor = ReferenceRangeExtractor()

    def parse(
        self,
        text: str,
        page_number: int | None = None,
    ) -> list[ExtractedTestResult]:

        results = self.parameter_extractor.extract(
            text=text,
            page_number=page_number,
        )

        for result in results:
            reference_range = self._find_nearby_reference_range(
                text=text,
                test_name=result.test_name,
            )

            if reference_range is not None:
                result.reference_range = reference_range

        return results

    def _find_nearby_reference_range(
        self,
        text: str,
        test_name: str,
    ):
        """
        Attempt to find a reference range near a test name.

        This is intentionally conservative. If no reliable range is
        found, None is returned rather than guessing.
        """

        pattern = re.compile(
            rf"{re.escape(test_name.replace('_', ' '))}"
            rf".{{0,150}}?"
            rf"(?:reference\s*range|normal\s*range|ref\.?)"
            rf"\s*[:\-]?\s*"
            rf"([-+]?\d+(?:\.\d+)?)"
            rf"\s*(?:-|–|to)\s*"
            rf"([-+]?\d+(?:\.\d+)?)",
            re.IGNORECASE | re.DOTALL,
        )

        match = pattern.search(text)

        if not match:
            return None

        from .schema import ReferenceRange

        return ReferenceRange(
            minimum=float(match.group(1)),
            maximum=float(match.group(2)),
        )