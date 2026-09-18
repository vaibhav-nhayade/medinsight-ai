"""
Medical report upload endpoints.
"""

from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.models.document import DocumentRecord
from backend.repositories.document_repository import (
    DocumentRepository,
)
from backend.schemas.report import UploadResponse
from backend.services.file_storage import FileStorageService


router = APIRouter(
    prefix="/api/v1/reports",
    tags=["Reports"],
)

storage = FileStorageService()
document_repository = DocumentRepository()


@router.post(
    "/upload",
    response_model=UploadResponse,
)
async def upload_report(
    file: UploadFile = File(...),
) -> UploadResponse:

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    content = await file.read()

    try:
        extension = storage.validate_file(
            filename=file.filename,
            file_size=len(content),
        )

        stored_path = storage.save_file(
            content=content,
            extension=extension,
        )

        document_id = str(uuid4())

        document = DocumentRecord(
            document_id=document_id,
            original_filename=file.filename,
            file_type=extension.lstrip("."),
            size_bytes=len(content),
            storage_path=stored_path,
        )

        document_repository.create(document)

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