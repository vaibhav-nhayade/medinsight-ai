"""
Reference range extraction from medical report text.
"""

from typing import Optional

from .reference_patterns import (
    RANGE_ONLY_PATTERN,
    REFERENCE_RANGE_PATTERN,
)
from .schema import ReferenceRange


class ReferenceRangeExtractor:
    """Extract reference ranges from report text."""

    def extract(self, text: str) -> Optional[ReferenceRange]:
        """
        Extract the first explicitly labelled reference range.

        Example:
            Reference Range: 12.0 - 16.0
        """

        match = REFERENCE_RANGE_PATTERN.search(text)

        if not match:
            return None

        minimum = float(match.group(1))
        maximum = float(match.group(2))

        return ReferenceRange(
            minimum=minimum,
            maximum=maximum,
        )

    def extract_range_from_text(
        self,
        text: str,
    ) -> Optional[ReferenceRange]:
        """Extract a generic numeric range when appropriate."""

        match = RANGE_ONLY_PATTERN.search(text)

        if not match:
            return None

        return ReferenceRange(
            minimum=float(match.group(1)),
            maximum=float(match.group(2)),
        )