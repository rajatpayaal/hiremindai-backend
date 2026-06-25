from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.public import PublicResponse
from app.services.public_store import list_records

router = APIRouter()


@router.get("", response_model=PublicResponse)
def dashboard(current_user: User = Depends(get_current_user)) -> PublicResponse:
    """
    Return a summary dashboard for the authenticated user.

    Includes counts of files, resumes, jobs, companies, and history entries.
    """
    uid = current_user.id

    def _count(bucket: str) -> int:
        return sum(1 for r in list_records(bucket) if r.get("owner_id") == uid)

    return PublicResponse(
        data={
            "user": {
                "id": uid,
                "email": current_user.email,
                "full_name": current_user.full_name,
            },
            "stats": {
                "files": _count("files"),
                "resumes": _count("resumes"),
                "jobs": _count("jobs"),
                "companies": _count("companies"),
                "history": _count("history"),
            },
        }
    )
