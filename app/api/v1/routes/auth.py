from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_refresh_user
from app.database.session import get_db
from app.models.user import User
from app.repositories.users import get_user_by_email
from app.schemas.auth import AccessToken, Token, UserCreate, UserLogin, UserRead
from app.services.auth import authenticate_user, issue_access_token, issue_token, register_user

router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> User:
    """Register a new user account."""
    if get_user_by_email(db, payload.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    return register_user(db, payload)


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)) -> Token:
    """Login with email/password. Returns access + refresh tokens."""
    user = authenticate_user(db, payload)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return issue_token(user)


@router.post("/refresh", response_model=AccessToken)
def refresh_token(current_user: User = Depends(get_refresh_user)) -> AccessToken:
    """Exchange a valid refresh token (Bearer) for a new access token."""
    return issue_access_token(current_user)


@router.post("/logout")
def logout() -> dict[str, str]:
    """
    Logout the current user.

    Stateless JWT — client must discard the token locally.
    For server-side revocation add a token blocklist (Redis etc.).
    """
    return {"status": "logged_out", "detail": "Discard your tokens client-side."}


@router.get("/profile", response_model=UserRead)
def profile(current_user: User = Depends(get_current_user)) -> User:
    """Return the profile of the currently authenticated user."""
    return current_user
