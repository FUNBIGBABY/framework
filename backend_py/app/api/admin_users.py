from datetime import datetime
import os

from fastapi import APIRouter, Depends, HTTPException, status
from nanoid import generate
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy.orm import Session

from ..auth import get_current_user, hash_password
from ..db import get_db
from ..models import User


router = APIRouter(prefix="/api/admin", tags=["admin"])


class AdminUserResponse(BaseModel):
    id: str
    email: str
    username: str
    created_at: datetime | None
    last_login: datetime | None
    is_disabled: bool
    disabled_at: datetime | None
    is_super_admin: bool


class AdminUserCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    password: str = Field(min_length=6)
    username: str | None = Field(default=None, min_length=3, max_length=30)


def _super_admin_email() -> str | None:
    value = os.getenv("SUPER_ADMIN_EMAIL")
    if not value:
        return None
    return value.strip().lower()


def _normalize_email(email: str) -> str:
    return str(email).strip().lower()


def _is_super_admin(user: User) -> bool:
    super_admin_email = _super_admin_email()
    if not super_admin_email:
        return False
    return _normalize_email(user.email) == super_admin_email


def require_super_admin(current_user: User = Depends(get_current_user)) -> User:
    if not _is_super_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


def _default_username(email: str) -> str:
    local_part = email.split("@", 1)[0]
    safe = "".join(ch if ch.isalnum() or ch in {"_", "-"} else "_" for ch in local_part)
    if len(safe) < 3:
        return "user"
    return safe[:30]


def _validate_username(username: str) -> str:
    value = username.strip()
    if len(value) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username must be at least 3 characters long",
        )
    if len(value) > 30:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username must be less than 30 characters",
        )
    if not value.replace("_", "").replace("-", "").isalnum():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username can only contain letters, numbers, hyphens and underscores",
        )
    return value


def _admin_user_response(user: User) -> AdminUserResponse:
    return AdminUserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        created_at=user.created_at,
        last_login=user.last_login,
        is_disabled=bool(getattr(user, "is_disabled", False)),
        disabled_at=user.disabled_at,
        is_super_admin=_is_super_admin(user),
    )


def _create_username(request: AdminUserCreateRequest, email: str, db: Session) -> str:
    if request.username is not None:
        username = _validate_username(request.username)
        existing = db.query(User).filter(User.username == username).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )
        return username

    username = _default_username(email)
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        username = f"user_{generate(size=8)}"
    return username


@router.get("/users", response_model=list[AdminUserResponse])
def list_admin_users(
    _admin: User = Depends(require_super_admin),
    db: Session = Depends(get_db),
):
    users = db.query(User).order_by(User.created_at.desc(), User.id.desc()).all()
    return [_admin_user_response(user) for user in users]


@router.post(
    "/users",
    response_model=AdminUserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_admin_user(
    request: AdminUserCreateRequest,
    _admin: User = Depends(require_super_admin),
    db: Session = Depends(get_db),
):
    normalized_email = _normalize_email(request.email)
    existing_user = db.query(User).filter(User.email == normalized_email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    username = _create_username(request, normalized_email, db)
    user = User(
        id=f"user_{generate(size=12)}",
        email=normalized_email,
        username=username,
        password_hash=hash_password(request.password),
        is_disabled=False,
        disabled_at=None,
        created_at=datetime.utcnow(),
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return _admin_user_response(user)


@router.post("/users/{user_id}/disable", response_model=AdminUserResponse)
def disable_admin_user(
    user_id: str,
    current_admin: User = Depends(require_super_admin),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if user.id == current_admin.id or _is_super_admin(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot disable the configured super-admin",
        )

    if not user.is_disabled:
        user.is_disabled = True
        user.disabled_at = datetime.utcnow()
        db.commit()
        db.refresh(user)

    return _admin_user_response(user)


@router.post("/users/{user_id}/enable", response_model=AdminUserResponse)
def enable_admin_user(
    user_id: str,
    _admin: User = Depends(require_super_admin),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user.is_disabled or user.disabled_at is not None:
        user.is_disabled = False
        user.disabled_at = None
        db.commit()
        db.refresh(user)

    return _admin_user_response(user)
