"""
JWT Authentication utilities (simplified version)
Using Python's built-in hashlib for password hashing
"""

from datetime import datetime, timedelta
from typing import Optional
import hashlib
import os
import secrets

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY environment variable is required")

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .db import get_db
from .models import User


# ============= Configuration =============

# JWT configuration
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

# HTTP Bearer authentication
security = HTTPBearer()


# ============= Password hashing/verification (using hashlib) =============


def hash_password(password: str) -> str:
    """
    Encrypt password using SHA-256 + salt

    Args:
        password: plain password

    Returns:
        Encrypted password hash (format: salt$hash)
    """
    # Generate random salt
    salt = secrets.token_hex(16)

    # Use SHA-256 hashing
    pwd_hash = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()

    # Return format: salt$hash
    return f"{salt}${pwd_hash}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password

    Args:
        plain_password: plain password
        hashed_password: encrypted password hash (format: salt$hash)

    Returns:
        Whether the password matches
    """
    try:
        # Split salt and hash
        salt, stored_hash = hashed_password.split("$")

        # Recompute hash using same salt
        pwd_hash = hashlib.sha256((salt + plain_password).encode("utf-8")).hexdigest()

        # Compare hashes
        return pwd_hash == stored_hash
    except Exception as e:
        print(f"Password verification error: {e}")
        return False


# ============= JWT Token Operations =============


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token

    Args:
        data: data to encode into the token (usually contains user_id)
        expires_delta: token expiration time (default 7 days)

    Returns:
        JWT token string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire, "iat": datetime.utcnow()})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Decode and validate JWT token

    Args:
        token: JWT token string

    Returns:
        Decoded payload data

    Raises:
        HTTPException: token invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ============= Dependency Injection - Get Current User =============


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """
    Extract current user ID from JWT token

    Used as dependency injection for routes, automatically validating the token in Authorization header

    Args:
        credentials: HTTP Bearer token

    Returns:
        User ID

    Raises:
        HTTPException: token invalid or missing
    """
    token = credentials.credentials

    try:
        payload = decode_access_token(token)
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
            )

        return user_id

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


def get_current_user(
    user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)
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
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


# ============= Optional Authentication (for mixed public/private endpoints) =============


def get_optional_user_id(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    ),
) -> Optional[str]:
    """
    Optional user authentication

    If a valid token is provided, return user ID; otherwise return None.
    Used for endpoints that support both public and private access.

    Args:
        credentials: optional HTTP Bearer token

    Returns:
        User ID or None
    """
    if not credentials:
        return None

    try:
        payload = decode_access_token(credentials.credentials)
        return payload.get("sub")
    except:
        return None
