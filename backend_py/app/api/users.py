"""
User Authentication API
Handles user registration, login and other authentication-related operations
"""

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, validator
from nanoid import generate
from datetime import datetime
import os

from ..db import get_db
from ..models import User
from ..auth import (
    hash_password,
    verify_password_with_rehash,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    get_current_user,
    _get_active_user,
    ACCESS_COOKIE_NAME,
    REFRESH_COOKIE_NAME,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)


router = APIRouter(prefix="/api/users", tags=["users"])


# ============= Request/Response Models =============


class UserRegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: str

    @validator("username")
    def username_validation(cls, v):
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters long")
        if len(v) > 30:
            raise ValueError("Username must be less than 30 characters")
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError(
                "Username can only contain letters, numbers, hyphens and underscores"
            )
        return v

    @validator("password")
    def password_validation(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    created_at: datetime
    is_super_admin: bool = False

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    success: bool
    message: str
    user: UserResponse


# ============= API Endpoints =============


def _public_registration_enabled() -> bool:
    return os.getenv("ENABLE_PUBLIC_REGISTER", "false").strip().lower() == "true"


def _allowed_emails() -> set[str]:
    raw = os.getenv("ALLOWED_EMAILS", "")
    return {
        email.strip().lower()
        for email in raw.split(",")
        if email.strip()
    }


def _email_is_allowed(email: str) -> bool:
    return email.strip().lower() in _allowed_emails()


def _super_admin_email() -> str:
    return os.getenv("SUPER_ADMIN_EMAIL", "").strip().lower()


def _is_super_admin(user: User) -> bool:
    admin_email = _super_admin_email()
    return bool(admin_email and user.email.strip().lower() == admin_email)


def _user_response(user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        created_at=user.created_at,
        is_super_admin=_is_super_admin(user),
    )


def _refresh_session_version(user: User) -> int:
    return int(getattr(user, "refresh_token_version", 0) or 0)


def _cookie_secure() -> bool:
    env = os.getenv("ENV", os.getenv("APP_ENV", "")).strip().lower()
    if env in {"prod", "production"}:
        return True

    configured = os.getenv("AUTH_COOKIE_SECURE")
    if configured is not None:
        return configured.strip().lower() in {"1", "true", "yes", "on"}
    return False


def _cookie_samesite() -> str:
    value = os.getenv("AUTH_COOKIE_SAMESITE", "lax").strip().lower()
    if value not in {"lax", "strict"}:
        value = "lax"
    return value


def _set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    secure = _cookie_secure()
    samesite = _cookie_samesite()

    response.set_cookie(
        ACCESS_COOKIE_NAME,
        access_token,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True,
        secure=secure,
        samesite=samesite,
        path="/",
    )
    response.set_cookie(
        REFRESH_COOKIE_NAME,
        refresh_token,
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        httponly=True,
        secure=secure,
        samesite=samesite,
        path="/",
    )


def _clear_auth_cookies(response: Response) -> None:
    secure = _cookie_secure()
    samesite = _cookie_samesite()
    response.delete_cookie(ACCESS_COOKIE_NAME, path="/", secure=secure, samesite=samesite)
    response.delete_cookie(
        REFRESH_COOKIE_NAME, path="/", secure=secure, samesite=samesite
    )


def _issue_auth_response(
    *,
    response: Response,
    user: User,
    message: str,
) -> AuthResponse:
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "username": user.username}
    )
    refresh_token = create_refresh_token(
        data={
            "sub": user.id,
            "email": user.email,
            "username": user.username,
            "ver": _refresh_session_version(user),
        }
    )
    _set_auth_cookies(response, access_token, refresh_token)
    return AuthResponse(
        success=True,
        message=message,
        user=_user_response(user),
    )


def _user_from_refresh_cookie(request: Request, db: Session) -> User:
    refresh_token = request.cookies.get(REFRESH_COOKIE_NAME)
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh cookie is missing",
        )

    payload = decode_refresh_token(refresh_token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token payload",
        )

    user = _get_active_user(db, user_id)
    if int(payload.get("ver", -1)) != _refresh_session_version(user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh session expired",
        )
    return user


@router.post(
    "/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED
)
def register_user(
    request: UserRegisterRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    """
    User registration

    Create a new user account and return a JWT token

    **Validation rules:**
    - Email: must be a valid email format
    - Username: 3–30 characters, can only contain letters, numbers, hyphens, underscores
    - Password: at least 6 characters

    **Returns:** Basic user info and sets the browser auth cookies.
    """

    normalized_email = str(request.email).strip().lower()

    if not _public_registration_enabled() or not _email_is_allowed(normalized_email):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Public registration is disabled",
        )

    # Check if email already exists
    existing_user_by_email = db.query(User).filter(User.email == normalized_email).first()
    if existing_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Check if username already exists
    existing_user_by_username = (
        db.query(User).filter(User.username == request.username).first()
    )
    if existing_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
        )

    # Create new user
    user_id = f"user_{generate(size=12)}"
    hashed_password = hash_password(request.password)

    new_user = User(
        id=user_id,
        email=normalized_email,
        username=request.username,
        password_hash=hashed_password,
        created_at=datetime.utcnow(),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return _issue_auth_response(
        response=response,
        user=new_user,
        message="User registered successfully",
    )


@router.post("/login", response_model=AuthResponse)
def login_user(
    request: UserLoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    """
    User login

    Validate user credentials and set the browser auth cookies.

    **Parameters:**
    - email: email used during registration
    - password: password

    **Returns:** Basic user info.
    """

    # Find user
    normalized_email = str(request.email).strip().lower()
    user = db.query(User).filter(User.email == normalized_email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    # Verify password
    valid_password, needs_rehash = verify_password_with_rehash(
        request.password, user.password_hash
    )
    if not valid_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    if getattr(user, "is_disabled", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled",
        )

    if needs_rehash:
        user.password_hash = hash_password(request.password)

    # Update last login time
    user.last_login = datetime.utcnow()
    db.commit()

    return _issue_auth_response(response=response, user=user, message="Login successful")


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current logged-in user's information

    **Requires Authentication:** A valid access cookie

    **Returns:** Basic information of the current user
    """

    return _user_response(current_user)


@router.post("/refresh", response_model=AuthResponse)
def refresh_user_session(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    user = _user_from_refresh_cookie(request, db)
    return _issue_auth_response(
        response=response,
        user=user,
        message="Session refreshed",
    )


@router.get("/check-email/{email}")
def check_email_availability(
    email: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Check if email is available (used for frontend real-time validation)

    **Returns:**
    - available: true/false
    """

    normalized_email = email.strip().lower()
    existing = db.query(User).filter(User.email == normalized_email).first()

    return {"email": normalized_email, "available": existing is None}


@router.get("/check-username/{username}")
def check_username_availability(
    username: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Check if username is available (used for frontend real-time validation)

    **Returns:**
    - available: true/false
    """

    existing = db.query(User).filter(User.username == username).first()

    return {"username": username, "available": existing is None}


@router.post("/logout")
def logout_user(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    """
    User logout

    Clears auth cookies and revokes the current refresh session when the
    refresh cookie is valid.
    """

    refresh_token = request.cookies.get(REFRESH_COOKIE_NAME)
    if refresh_token:
        try:
            user = _user_from_refresh_cookie(request, db)
            user.refresh_token_version = _refresh_session_version(user) + 1
            db.commit()
            print(f"User {user.id} logged out")
        except HTTPException:
            pass

    _clear_auth_cookies(response)

    return {"success": True, "message": "Logged out successfully"}
