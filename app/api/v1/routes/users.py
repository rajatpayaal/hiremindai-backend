from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.repositories.users import deactivate_user, update_user
from app.schemas.auth import UserRead, UserUpdate

router = APIRouter()


@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)) -> User:
    """Return the authenticated user's profile."""
    return current_user


@router.put("/me", response_model=UserRead)
def update_me(
    payload: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """Update the authenticated user's profile fields."""
    return update_user(db, current_user, full_name=payload.full_name, email=payload.email)


@router.delete("/me", status_code=status.HTTP_200_OK)
def delete_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, str | int]:
    """Soft-delete (deactivate) the authenticated user's account."""
    deactivate_user(db, current_user)
    return {"status": "deactivated", "user_id": current_user.id}
