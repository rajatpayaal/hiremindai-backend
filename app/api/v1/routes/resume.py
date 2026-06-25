from fastapi import APIRouter, Depends, HTTPException, status

from app.agents.registry import get_agent
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.public import PublicPayload, PublicResponse, ResumeParsePayload
from app.services.public_store import create_record, delete_record, get_record, list_records, update_record

router = APIRouter()


@router.post("/upload", response_model=PublicResponse, status_code=status.HTTP_201_CREATED)
def upload_resume(
    payload: PublicPayload,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """Store raw resume text/data and return a resumeId."""
    record = create_record(
        "resumes",
        {"resume": payload.payload, "owner_id": current_user.id},
    )
    return PublicResponse(id=record["id"], data=record)


@router.post("/parse", response_model=PublicResponse)
async def parse_resume(
    payload: ResumeParsePayload,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """Parse resume text with the AI Resume Parser agent and return structured data."""
    result = await get_agent("resume_parser").run(payload.model_dump())
    # Persist the parsed result
    record = create_record("resumes", {**result, "owner_id": current_user.id, "parsed": True})
    return PublicResponse(id=record["id"], data=result)


@router.get("/{resume_id}", response_model=PublicResponse)
def get_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """Retrieve a stored resume by its ID."""
    record = get_record("resumes", resume_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    return PublicResponse(id=resume_id, data=record)


@router.put("/{resume_id}", response_model=PublicResponse)
def update_resume(
    resume_id: str,
    payload: PublicPayload,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """Update a stored resume's data."""
    record = update_record("resumes", resume_id, payload.payload)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    return PublicResponse(id=resume_id, data=record)


@router.delete("/{resume_id}", response_model=PublicResponse)
def delete_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """Delete a stored resume."""
    if not delete_record("resumes", resume_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    return PublicResponse(id=resume_id, data={"deleted": True})


@router.get("", response_model=PublicResponse)
def list_resumes(current_user: User = Depends(get_current_user)) -> PublicResponse:
    """List all resumes belonging to the authenticated user."""
    all_resumes = list_records("resumes")
    user_resumes = [r for r in all_resumes if r.get("owner_id") == current_user.id]
    return PublicResponse(data={"resumes": user_resumes, "total": len(user_resumes)})
