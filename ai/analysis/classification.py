"""
Deterministic classification of medical test results.

This module does not diagnose conditions.
It only compares a measured value with a supplied reference range.
"""

from enum import Enum
from typing import Optional

from ai.extraction.schema import ReferenceRange


class ResultStatus(str, Enum):
    NORMAL = "normal"
    LOW = "low"
    HIGH = "high"
    UNKNOWN = "unknown"


def classify_result(
    value: Optional[float],
    reference_range: ReferenceRange,
) -> ResultStatus:
    """
    Classify a result using the reference range provided by the report.
    """

    if value is None:
        return ResultStatus.UNKNOWN

    minimum = reference_range.minimum
    maximum = reference_range.maximum

    if minimum is None and maximum is None:
        return ResultStatus.UNKNOWN

    if minimum is not None and value < minimum:
        return ResultStatus.LOW

    if maximum is not None and value > maximum:
        return ResultStatus.HIGH

    return ResultStatus.NORMAL