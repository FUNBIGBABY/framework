import os


os.environ.setdefault("JWT_SECRET_KEY", "test-secret-for-backend-tests-32-chars")
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+psycopg://test:test@localhost:5432/test",
)
