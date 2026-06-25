import os
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

from app.core.config import settings
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.public import PublicResponse
from app.services.public_store import create_record, delete_record, get_record, list_records

router = APIRouter()

ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
}


@router.post("/upload", response_model=PublicResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """Upload a file (PDF, DOCX, or TXT). Returns a fileId for later use."""
    # Validate content type
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type '{file.content_type}'. "
            "Allowed: PDF, DOCX, DOC, TXT.",
        )

    # Read and validate size
    content = await file.read()
    if len(content) > settings.max_upload_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds maximum allowed size of {settings.max_upload_size_bytes} bytes.",
        )

    # Persist to local storage
    storage_dir = Path(settings.local_storage_path) / "uploads" / str(current_user.id)
    storage_dir.mkdir(parents=True, exist_ok=True)

    file_id = uuid.uuid4().hex
    extension = Path(file.filename or "upload").suffix or ".bin"
    dest = storage_dir / f"{file_id}{extension}"
    dest.write_bytes(content)

    record = create_record(
        "files",
        {
            "id": file_id,
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(content),
            "path": str(dest),
            "owner_id": current_user.id,
        },
    )
    # Override the auto-generated id with our own file_id
    record["id"] = file_id
    return PublicResponse(id=file_id, data=record)


@router.get("/{file_id}", response_model=PublicResponse)
def get_file(
    file_id: str,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """Retrieve file metadata by fileId."""
    record = get_record("files", file_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return PublicResponse(id=file_id, data=record)


@router.delete("/{file_id}", response_model=PublicResponse)
def delete_file(
    file_id: str,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """Delete a file record and its stored bytes."""
    record = get_record("files", file_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    # Remove physical file if present
    path = record.get("path")
    if path and os.path.exists(path):
        os.remove(path)

    delete_record("files", file_id)
    return PublicResponse(id=file_id, data={"deleted": True})


@router.get("", response_model=PublicResponse)
def list_files(current_user: User = Depends(get_current_user)) -> PublicResponse:
    """List all files uploaded by the authenticated user."""
    all_files = list_records("files")
    user_files = [f for f in all_files if f.get("owner_id") == current_user.id]
    return PublicResponse(data={"files": user_files, "total": len(user_files)})
