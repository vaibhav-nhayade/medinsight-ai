"""
Plain-language explanation layer.

This first version intentionally uses deterministic templates.
LLM-generated explanations will be introduced later with
evidence grounding and safety validation.
"""

from .finding import MedicalFinding


def explain_finding(
    finding: MedicalFinding,
) -> str:
    """
    Produce a simple educational explanation.

    This function does not diagnose a condition or recommend treatment.
    """

    if finding.status.value == "high":
        return (
            f"The reported {finding.test_name.replace('_', ' ')} "
            f"is higher than the reference range shown in the report. "
            f"The result should be interpreted together with the "
            f"person's clinical context by a qualified healthcare "
            f"professional."
        )

    if finding.status.value == "low":
        return (
            f"The reported {finding.test_name.replace('_', ' ')} "
            f"is lower than the reference range shown in the report. "
            f"The result should be interpreted together with the "
            f"person's clinical context by a qualified healthcare "
            f"professional."
        )

    if finding.status.value == "unknown":
        return (
            f"The reported {finding.test_name.replace('_', ' ')} "
            f"could not be compared with a reference range from "
            f"the available report information."
        )

    return (
        f"The reported {finding.test_name.replace('_', ' ')} "
        f"is within the reference range shown in the report."
    )