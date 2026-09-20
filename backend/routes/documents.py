"""
Document metadata API endpoints.
"""

from fastapi import APIRouter, HTTPException

from backend.schemas.document import DocumentStatusResponse
from backend.services.document_service import document_service


router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Documents"],
)


@router.get(
    "/{document_id}",
    response_model=DocumentStatusResponse,
)
def get_document(
    document_id: str,
) -> DocumentStatusResponse:
    """Return metadata and processing status for a document."""

    document = document_service.get(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    return DocumentStatusResponse(
        document_id=document.document_id,
        filename=document.original_filename,
        file_type=document.file_type,
        size_bytes=document.size_bytes,
        status=document.status,
        created_at=document.created_at,
    )