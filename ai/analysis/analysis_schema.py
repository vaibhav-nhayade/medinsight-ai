"""
Stable schema for the report-analysis layer.

This schema acts as a boundary between the AI pipeline and
the future backend/API layer.
"""

from dataclasses import dataclass
from typing import Optional

from .classification import ResultStatus


@dataclass
class AnalysisResultItem:
    """API-friendly representation of one analyzed test."""

    test_name: str
    value: Optional[float]
    unit: Optional[str]
    status: ResultStatus
    reference_minimum: Optional[float]
    reference_maximum: Optional[float]
    confidence: float
    needs_verification: bool
    source_page: Optional[int]


@dataclass
class AnalysisReport:
    """Stable top-level analysis response."""

    document_id: str
    filename: str
    results: list[AnalysisResultItem]
    finding_count: int
    verification_required: int