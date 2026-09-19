"""
Medical report analysis API endpoints.
"""

from fastapi import APIRouter, HTTPException

from backend.schemas.report import AnalysisResponse
from backend.services.document_service import document_service
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
    """Analyze the exact uploaded document identified by document_id."""

    document = document_service.get(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    try:
        document_service.mark_processing(document_id)

        analysis = report_service.analyze_report(
            file_path=document.storage_path,
            document_id=document.document_id,
        )

        document_service.mark_processed(document_id)

        return analysis

    except ValueError as exc:
        document_service.mark_failed(document_id)

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except FileNotFoundError as exc:
        document_service.mark_failed(document_id)

        raise HTTPException(
            status_code=404,
            detail="Stored document could not be found.",
        ) from exc

    except Exception:
        document_service.mark_failed(document_id)

        raise HTTPException(
            status_code=500,
            detail="Document analysis failed.",
        )