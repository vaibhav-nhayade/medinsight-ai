"""
Medical report upload endpoints.
"""

from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.services.file_storage import FileStorageService


router = APIRouter(
    prefix="/api/v1/reports",
    tags=["Reports"],
)

storage = FileStorageService()


@router.post("/upload")
async def upload_report(
    file: UploadFile = File(...),
) -> dict:

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

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    document_id = str(uuid4())

    return {
        "document_id": document_id,
        "filename": file.filename,
        "file_type": extension.lstrip("."),
        "size_bytes": len(content),
        "status": "uploaded",
        "storage_path": str(stored_path),
    }