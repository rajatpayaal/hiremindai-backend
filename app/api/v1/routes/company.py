from fastapi import APIRouter, Depends, HTTPException, status

from app.agents.registry import get_agent
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.public import PublicPayload, PublicResponse
from app.services.public_store import create_record, get_record

router = APIRouter()


@router.post("/analyze", response_model=PublicResponse, status_code=status.HTTP_201_CREATED)
async def analyze_company(
    payload: PublicPayload,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """
    Run the Company Intelligence agent to gather insights about a target company.

    Expected payload keys: `company_name`, `job_description` (optional).
    """
    result = await get_agent("company_intelligence").run(payload.payload)
    record = create_record("companies", {**result, "owner_id": current_user.id})
    return PublicResponse(id=record["id"], data=record)


@router.get("/{company_id}", response_model=PublicResponse)
def get_company(
    company_id: str,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """Retrieve stored company intelligence by companyId."""
    record = get_record("companies", company_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return PublicResponse(id=company_id, data=record)
