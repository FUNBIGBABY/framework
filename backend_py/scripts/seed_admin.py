"""
Seed the personal super-admin account.

Required env:
- SUPER_ADMIN_EMAIL
- SUPER_ADMIN_PASSWORD
- JWT_SECRET_KEY
- SEED_ADMIN_RESET_PASSWORD=true to reset an existing admin password

The current User model has no is_admin column. Until the database migration phase,
the configured SUPER_ADMIN_EMAIL is the admin identity boundary.
"""

from pathlib import Path
import os
import sys
from datetime import datetime

from nanoid import generate

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.auth import hash_password, verify_password_with_rehash  # noqa: E402
from app.db import SessionLocal  # noqa: E402
from app.models import User  # noqa: E402


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} environment variable is required")
    return value.strip()


def _env_enabled(name: str) -> bool:
    return os.getenv(name, "false").strip().lower() == "true"


def _default_username(email: str) -> str:
    local_part = email.split("@", 1)[0]
    safe = "".join(ch if ch.isalnum() or ch in {"_", "-"} else "_" for ch in local_part)
    return safe[:30] or "super_admin"


def main() -> None:
    email = _required_env("SUPER_ADMIN_EMAIL").lower()
    password = _required_env("SUPER_ADMIN_PASSWORD")
    username = os.getenv("SUPER_ADMIN_USERNAME", _default_username(email)).strip()

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user:
            valid_password, needs_rehash = verify_password_with_rehash(
                password, user.password_hash
            )
            if valid_password:
                if needs_rehash:
                    user.password_hash = hash_password(password)
                    db.commit()
                    print(f"Existing admin password hash upgraded for {email}")
                else:
                    print(f"Admin user already exists and password verified: {email}")
                return

            if not _env_enabled("SEED_ADMIN_RESET_PASSWORD"):
                raise RuntimeError(
                    "Admin user already exists but SUPER_ADMIN_PASSWORD does not match. "
                    "Set SEED_ADMIN_RESET_PASSWORD=true to reset it."
                )

            user.password_hash = hash_password(password)
            db.commit()
            print(f"Existing admin password reset for {email}")
            return

        existing_username = db.query(User).filter(User.username == username).first()
        if existing_username:
            username = f"admin_{generate(size=8)}"

        user = User(
            id=f"user_{generate(size=12)}",
            email=email,
            username=username,
            password_hash=hash_password(password),
            created_at=datetime.utcnow(),
        )
        db.add(user)
        db.commit()
        print(f"Created admin user: {email}")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
