"""
JWT authentication utilities.

Password hashes are Argon2id for all new credentials. Legacy SHA-256+salt
hashes remain verifiable so old accounts can be rehashed after a successful
login.
"""

from datetime import datetime, timedelta
from typing import Optional
import hashlib
import os
import secrets

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError
from argon2.low_level import Type
from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .db import get_db
from .models import User


# ============= Configuration =============

# JWT configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY environment variable is required")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 30
ACCESS_COOKIE_NAME = "access_token"
REFRESH_COOKIE_NAME = "refresh_token"

# Argon2id password hashing
password_hasher = PasswordHasher(type=Type.ID)
ARGON2ID_PREFIX = "$argon2id$"


# ============= Password hashing/verification =============


def hash_password(password: str) -> str:
    """Hash a plaintext password with Argon2id."""
    return password_hasher.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against Argon2id or the legacy SHA-256+salt format."""
    valid, _needs_rehash = verify_password_with_rehash(
        plain_password, hashed_password
    )
    return valid


def verify_password_with_rehash(
    plain_password: str, hashed_password: str
) -> tuple[bool, bool]:
    """Return (valid, needs_rehash) for Argon2id or legacy SHA-256+salt hashes."""
    if not hashed_password:
        return False, False

    if hashed_password.startswith(ARGON2ID_PREFIX):
        try:
            valid = password_hasher.verify(hashed_password, plain_password)
        except (VerifyMismatchError, InvalidHashError, VerificationError, TypeError):
            return False, False

        if not valid:
            return False, False

        try:
            return True, password_hasher.check_needs_rehash(hashed_password)
        except (InvalidHashError, VerificationError, TypeError):
            return True, False

    if _verify_legacy_sha256_password(plain_password, hashed_password):
        return True, True

    return False, False


def _verify_legacy_sha256_password(
    plain_password: str, hashed_password: str
) -> bool:
    """Verify the old salt$sha256(salt + password) format."""
    try:
        salt, stored_hash = hashed_password.split("$", 1)
        if not salt or len(stored_hash) != 64:
            return False
        pwd_hash = hashlib.sha256((salt + plain_password).encode("utf-8")).hexdigest()
        return secrets.compare_digest(pwd_hash, stored_hash)
    except (AttributeError, ValueError, TypeError):
        return False


# ============= JWT Token Operations =============


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token

    Args:
        data: data to encode into the token (usually contains user_id)
        expires_delta: token expiration time (default 1 hour)

    Returns:
        JWT token string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "iat": datetime.utcnow(), "typ": "access"})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT refresh token for the httpOnly refresh cookie."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire, "iat": datetime.utcnow(), "typ": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def _decode_token_payload(token: str) -> dict:
    """
    Decode and validate JWT signature and expiry.

    Args:
        token: JWT token string

    Returns:
        Decoded payload data

    Raises:
        HTTPException: token invalid or expired
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


def decode_access_token(token: str) -> dict:
    """
    Decode and validate a JWT access token.

    Protected endpoints must never accept refresh tokens as credentials.
    """
    payload = _decode_token_payload(token)
    if payload.get("typ") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )
    return payload


def decode_refresh_token(token: str) -> dict:
    """Decode and validate a refresh token payload."""
    payload = _decode_token_payload(token)
    if payload.get("typ") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    return payload


# ============= Dependency Injection - Get Current User =============


def _extract_access_token(request: Request) -> str:
    cookie_token = request.cookies.get(ACCESS_COOKIE_NAME)
    if cookie_token:
        return cookie_token

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
    )


def _decode_user_id_from_request(
    token: str = Depends(_extract_access_token),
) -> str:
    payload = decode_access_token(token)
    user_id: str = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
        )

    return user_id


def _get_active_user(db: Session, user_id: str) -> User:
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if getattr(user, "is_disabled", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled",
        )

    return user


def get_current_user_id(
    user_id: str = Depends(_decode_user_id_from_request),
    db: Session = Depends(get_db),
) -> str:
    """
    Extract the current user ID from a JWT and verify the user is active.

    Routes that only need the ID still perform a database status check, so an
    already-issued token stops working as soon as the account is disabled.
    """
    return _get_active_user(db, user_id).id


def get_current_user(
    user_id: str = Depends(_decode_user_id_from_request),
    db: Session = Depends(get_db),
) -> User:
    """
    Get full information of the current logged-in user

    Used for routes that need full user objects

    Args:
        user_id: user ID extracted from token
        db: database session

    Returns:
        User object

    Raises:
        HTTPException: user does not exist
    """
    return _get_active_user(db, user_id)


# ============= Optional Authentication (for mixed public/private endpoints) =============


def get_optional_user_id(request: Request) -> Optional[str]:
    """
    Optional user authentication

    If a valid access cookie is provided, return user ID; otherwise return None.
    Used for endpoints that support both public and private access.

    Returns:
        User ID or None
    """
    token = request.cookies.get(ACCESS_COOKIE_NAME)

    if not token:
        return None

    try:
        payload = decode_access_token(token)
        return payload.get("sub")
    except:
        return None
