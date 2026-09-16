from dataclasses import dataclass
from typing import Optional

from .classification import ResultStatus


@dataclass
class MedicalFinding:
    """
    Structured representation of a potentially notable test result.

    A finding is an observation, not a diagnosis.
    """

    test_name: str
    status: ResultStatus
    value: Optional[float]
    unit: Optional[str]
    reference_minimum: Optional[float]
    reference_maximum: Optional[float]
    title: str
    description: str
    severity: str
    source_page: Optional[int] = None
    needs_verification: bool = False