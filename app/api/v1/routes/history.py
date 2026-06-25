from fastapi import APIRouter, Depends, HTTPException, status

from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.public import PublicResponse
from app.services.public_store import delete_record, get_record, list_records

router = APIRouter()


@router.get("", response_model=PublicResponse)
def list_history(current_user: User = Depends(get_current_user)) -> PublicResponse:
    """List all history entries belonging to the authenticated user."""
    all_history = list_records("history")
    user_history = [h for h in all_history if h.get("owner_id") == current_user.id]
    return PublicResponse(
        data={"history": user_history, "total": len(user_history)}
    )


@router.get("/{history_id}", response_model=PublicResponse)
def get_history(
    history_id: str,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """Retrieve a single history entry by its ID."""
    record = get_record("history", history_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="History item not found")
    return PublicResponse(id=history_id, data=record)


@router.delete("/{history_id}", response_model=PublicResponse)
def delete_history(
    history_id: str,
    current_user: User = Depends(get_current_user),
) -> PublicResponse:
    """Delete a history entry by its ID."""
    if not delete_record("history", history_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="History item not found")
    return PublicResponse(id=history_id, data={"deleted": True})
