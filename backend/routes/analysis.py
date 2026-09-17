"""
Medical report analysis API endpoints.
"""

from pathlib import Path

from fastapi import APIRouter, HTTPException

from backend.schemas.report import AnalysisResponse
from backend.services.report_service import ReportService


router = APIRouter(
    prefix="/api/v1/reports",
    tags=["Analysis"],
)

report_service = ReportService()


@router.post(
    "/{document_id}/analyze",
    response_model=AnalysisResponse,
)
def analyze_report(
    document_id: str,
) -> AnalysisResponse:
    """
    Analyze a previously uploaded medical report.

    The document ID is currently mapped to the local upload directory.
    Persistent metadata storage will be introduced later.
    """

    from backend.config import UPLOAD_DIR

    matching_files = list(
        UPLOAD_DIR.glob("*")
    )

    if not matching_files:
        raise HTTPException(
            status_code=404,
            detail="No uploaded documents found.",
        )

    # Temporary MVP mapping.
    #
    # A database-backed document repository will replace this
    # mechanism in a later milestone.
    file_path: Path | None = None

    for candidate in matching_files:
        if candidate.is_file():
            file_path = candidate
            break

    if file_path is None:
        raise HTTPException(
            status_code=404,
            detail="Uploaded document could not be found.",
        )

    try:
        return report_service.analyze_report(
            file_path=file_path,
            document_id=document_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc