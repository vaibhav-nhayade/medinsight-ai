"""
Patterns for extracting reference ranges from medical reports.
"""

import re

NUMBER = r"[-+]?\d+(?:\.\d+)?"

REFERENCE_RANGE_PATTERN = re.compile(
    rf"(?:reference\s*range|normal\s*range|ref(?:erence)?\.?)"
    rf"\s*[:\-]?\s*"
    rf"({NUMBER})"
    rf"\s*(?:-|–|to)\s*"
    rf"({NUMBER})",
    re.IGNORECASE,
)

RANGE_ONLY_PATTERN = re.compile(
    rf"\b({NUMBER})\s*(?:-|–|to)\s*({NUMBER})\b"
)