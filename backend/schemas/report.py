"""
Pydantic schemas for medical report APIs.
"""

from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    """Response returned after successful report upload."""

    document_id: str
    filename: str
    file_type: str
    size_bytes: int = Field(ge=1)
    status: str


class ReportResultResponse(BaseModel):
    """Structured representation of one analyzed test result."""

    test_name: str
    value: float | None
    unit: str | None

    reference_minimum: float | None
    reference_maximum: float | None

    status: str

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

    needs_verification: bool
    source_page: int | None


class FindingResponse(BaseModel):
    """Neutral finding generated from a report result."""

    test_name: str
    status: str
    value: float | None
    unit: str | None

    title: str
    description: str
    severity: str

    source_page: int | None
    needs_verification: bool


class AnalysisSummaryResponse(BaseModel):
    """Summary statistics for a report."""

    total_results: int
    normal_results: int
    low_results: int
    high_results: int
    unknown_results: int

    findings_count: int
    verification_required: int


class AnalysisResponse(BaseModel):
    """Complete report-analysis API response."""

    document_id: str
    filename: str

    results: list[ReportResultResponse]
    findings: list[FindingResponse]

    summary: AnalysisSummaryResponse