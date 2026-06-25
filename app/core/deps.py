"""FastAPI dependency helpers for authentication and database sessions."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.database.session import get_db
from app.models.user import User
from app.repositories.users import get_user_by_id

_bearer = HTTPBearer(auto_error=True)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    db: Session = Depends(get_db),
) -> User:
    """Validate the Bearer JWT and return the authenticated User."""
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        subject: str | None = payload.get("sub")
        token_type: str | None = payload.get("type")
        if subject is None or token_type != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_id(db, int(subject))
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return user


def get_refresh_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    db: Session = Depends(get_db),
) -> User:
    """Validate the refresh-token Bearer JWT and return the User."""
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        subject: str | None = payload.get("sub")
        token_type: str | None = payload.get("type")
        if subject is None or token_type != "refresh":
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_id(db, int(subject))
    if user is None or not user.is_active:
        raise credentials_exception
    return user
