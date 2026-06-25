from fastapi import APIRouter, Depends, HTTPException, status

from app.agents.registry import get_agent
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.public import JobParsePayload, PublicPayload, PublicResponse
from app.services.public_store import create_record, delete_record, get_record, list_records

router = APIRouter()


@router.post("/upload", response_model=PublicResponse, status_code=status.HTTP_201_CREATED)
def upload_job(
    payload: PublicPayload,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """Store raw job description data and return a jobId."""
    record = create_record("jobs", {"job": payload.payload, "owner_id": current_user.id})
    return PublicResponse(id=record["id"], data=record)


@router.post("/parse", response_model=PublicResponse)
async def parse_job(
    payload: JobParsePayload,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """Parse a job description with the AI JD Parser agent and return structured data."""
    result = await get_agent("jd_parser").run(payload.model_dump())
    record = create_record("jobs", {**result, "owner_id": current_user.id, "parsed": True})
    return PublicResponse(id=record["id"], data=result)


@router.get("/{job_id}", response_model=PublicResponse)
def get_job(
    job_id: str,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """Retrieve a stored job description by its ID."""
    record = get_record("jobs", job_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return PublicResponse(id=job_id, data=record)


@router.delete("/{job_id}", response_model=PublicResponse)
def delete_job(
    job_id: str,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """Delete a stored job description."""
    if not delete_record("jobs", job_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return PublicResponse(id=job_id, data={"deleted": True})


@router.get("", response_model=PublicResponse)
def list_jobs(current_user: User = Depends(get_current_user)) -> PublicResponse:
    """List all job descriptions belonging to the authenticated user."""
    all_jobs = list_records("jobs")
    user_jobs = [j for j in all_jobs if j.get("owner_id") == current_user.id]
    return PublicResponse(data={"jobs": user_jobs, "total": len(user_jobs)})
