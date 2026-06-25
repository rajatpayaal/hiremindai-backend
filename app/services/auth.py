from sqlalchemy.orm import Session

from app.core.security import create_access_token, create_refresh_token, hash_password, verify_password
from app.models.user import User
from app.repositories.users import create_user, get_user_by_email
from app.schemas.auth import AccessToken, Token, UserCreate, UserLogin


def register_user(db: Session, payload: UserCreate) -> User:
    return create_user(
        db,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
    )


def authenticate_user(db: Session, payload: UserLogin) -> User | None:
    user = get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        return None
    return user


def issue_token(user: User) -> Token:
    return Token(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )


def issue_access_token(user: User) -> AccessToken:
    return AccessToken(access_token=create_access_token(str(user.id)))
