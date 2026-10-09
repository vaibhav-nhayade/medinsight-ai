
"""
Medical report upload endpoints.
"""

from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.config import MAX_UPLOAD_SIZE
from backend.models.document import DocumentRecord
from backend.schemas.report import UploadResponse
from backend.services.document_service import document_service
from backend.services.file_storage import FileStorageService


router = APIRouter(
    prefix="/api/v1/reports",
    tags=["Reports"],
)

storage = FileStorageService()


@router.post(
    "/upload",
    response_model=UploadResponse,
)
async def upload_report(
    file: UploadFile = File(...),
) -> UploadResponse:
    """Validate and store an uploaded medical report."""

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    # Read at most one byte beyond the limit to detect oversized uploads.
    content = await file.read(MAX_UPLOAD_SIZE + 1)

    try:
        extension = storage.validate_file(
            filename=file.filename,
            file_size=len(content),
        )

        
        stored_path = storage.save_file(
            content=content,
            extension=extension,
        )

        try:
            document_id = str(uuid4())

            document = DocumentRecord(
                document_id=document_id,
                original_filename=file.filename,
                file_type=extension.lstrip("."),
                size_bytes=len(content),
                storage_path=stored_path,
            )

            document_service.register(document)

        except Exception:
            # Remove the saved file if document registration fails.
            try:
                stored_path.unlink(missing_ok=True)
            except OSError:
                # Preserve the original registration error.
                pass
            raise


    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return UploadResponse(
        document_id=document_id,
        filename=file.filename,
        file_type=extension.lstrip("."),
        size_bytes=len(content),
        status=document.status,
    )
