"""
Validation layer for extracted medical test results.
"""

import math

from .schema import ExtractedTestResult


def validate_extracted_result(
    result: ExtractedTestResult,
) -> ExtractedTestResult:
    """
    Validate basic structural properties of an extracted result.

    This does not determine clinical significance.
    """

    if result.value is not None:
        if not math.isfinite(result.value):
            result.needs_verification = True

    if not 0.0 <= result.confidence <= 1.0:
        result.confidence = max(0.0, min(result.confidence, 1.0))
        result.needs_verification = True

    if result.confidence < 0.75:
        result.needs_verification = True

    if not result.test_name.strip():
        result.needs_verification = True

    return result