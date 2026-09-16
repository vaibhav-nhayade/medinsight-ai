"""
Deterministic rules for converting result classifications into findings.

These rules do not diagnose medical conditions.
"""

from .classification import ResultStatus


def build_finding_title(
    test_name: str,
    status: ResultStatus,
) -> str:
    """Generate a neutral finding title."""

    readable_name = test_name.replace("_", " ").title()

    if status == ResultStatus.HIGH:
        return f"{readable_name} is above the reported range"

    if status == ResultStatus.LOW:
        return f"{readable_name} is below the reported range"

    if status == ResultStatus.UNKNOWN:
        return f"{readable_name} could not be classified"

    return f"{readable_name} is within the reported range"


def build_finding_description(
    test_name: str,
    status: ResultStatus,
    value: float | None,
    unit: str | None,
    minimum: float | None,
    maximum: float | None,
) -> str:
    """Create a neutral, report-grounded explanation."""

    readable_name = test_name.replace("_", " ").title()

    value_text = (
        f"{value:g} {unit}".strip()
        if value is not None
        else "an unavailable value"
    )

    if minimum is not None and maximum is not None:
        range_text = f"{minimum:g}–{maximum:g} {unit or ''}".strip()
    elif minimum is not None:
        range_text = f">= {minimum:g} {unit or ''}".strip()
    elif maximum is not None:
        range_text = f"<= {maximum:g} {unit or ''}".strip()
    else:
        range_text = "no reference range was available"

    if status == ResultStatus.HIGH:
        return (
            f"{readable_name} was reported as {value_text}. "
            f"This is above the reference range reported in the document "
            f"({range_text})."
        )

    if status == ResultStatus.LOW:
        return (
            f"{readable_name} was reported as {value_text}. "
            f"This is below the reference range reported in the document "
            f"({range_text})."
        )

    if status == ResultStatus.NORMAL:
        return (
            f"{readable_name} was reported as {value_text}. "
            f"This falls within the reference range reported in the "
            f"document ({range_text})."
        )

    return (
        f"{readable_name} was reported as {value_text}, but the document "
        f"does not provide enough reference-range information to classify "
        f"the result."
    )