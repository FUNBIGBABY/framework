"""
User Authentication API
Handles user registration, login and other authentication-related operations
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, validator
from nanoid import generate
from datetime import datetime

from ..db import get_db
from ..models import User
from ..auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user_id,
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

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    success: bool
    message: str
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ============= API Endpoints =============


@router.post(
    "/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED
)
def register_user(request: UserRegisterRequest, db: Session = Depends(get_db)):
    """
    User registration

    Create a new user account and return a JWT token

    **Validation rules:**
    - Email: must be a valid email format
    - Username: 3–30 characters, can only contain letters, numbers, hyphens, underscores
    - Password: at least 6 characters

    **Returns:**
    - access_token: JWT token (used for subsequent API calls)
    - user: basic user info
    """

    # Check if email already exists
    existing_user_by_email = db.query(User).filter(User.email == request.email).first()
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
        email=request.email,
        username=request.username,
        password_hash=hashed_password,
        created_at=datetime.utcnow(),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate JWT token
    access_token = create_access_token(
        data={
            "sub": new_user.id,
            "email": new_user.email,
            "username": new_user.username,
        }
    )

    return AuthResponse(
        success=True,
        message="User registered successfully",
        access_token=access_token,
        user=UserResponse.from_orm(new_user),
    )


@router.post("/login", response_model=AuthResponse)
def login_user(request: UserLoginRequest, db: Session = Depends(get_db)):
    """
    User login

    Validate user credentials and return a JWT token

    **Parameters:**
    - email: email used during registration
    - password: password

    **Returns:**
    - access_token: JWT token (valid for 7 days)
    - user: basic user info
    """

    # Find user
    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    # Update last login time
    user.last_login = datetime.utcnow()
    db.commit()

    # Generate JWT token
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "username": user.username}
    )

    return AuthResponse(
        success=True,
        message="Login successful",
        access_token=access_token,
        user=UserResponse.from_orm(user),
    )


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)
):
    """
    Get current logged-in user's information

    **Requires Authentication:** A valid JWT token must be provided in Authorization header

    **Returns:** Basic information of the current user
    """

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return UserResponse.from_orm(user)


@router.get("/check-email/{email}")
def check_email_availability(email: str, db: Session = Depends(get_db)):
    """
    Check if email is available (used for frontend real-time validation)

    **Returns:**
    - available: true/false
    """

    existing = db.query(User).filter(User.email == email).first()

    return {"email": email, "available": existing is None}


@router.get("/check-username/{username}")
def check_username_availability(username: str, db: Session = Depends(get_db)):
    """
    Check if username is available (used for frontend real-time validation)

    **Returns:**
    - available: true/false
    """

    existing = db.query(User).filter(User.username == username).first()

    return {"username": username, "available": existing is None}


@router.post("/logout")
def logout_user(user_id: str = Depends(get_current_user_id)):
    """
    User logout

    Note: Since JWT is stateless, logout is handled on the frontend (token deletion)
    This endpoint is mainly for logging or performing cleanup actions

    **Requires Authentication**
    """

    # You may record logout logs here
    print(f"User {user_id} logged out")

    return {"success": True, "message": "Logged out successfully"}
